import copy
import unittest

from tuhoc.lessons import image_children as ic
from tuhoc.lessons.lesson_canvas_math import (clip_range, decode, encode, locate_fragment,
                                              merge_ranges, near_any, selection_ranges)


def wrap_words(text, per_line):
    """Fake wrapper: fixed words per line, like a re-wrap after zoom."""
    words = text.split()
    return [' '.join(words[i:i + per_line]) for i in range(0, len(words), per_line)]


def make_hits(text, per_line, key='f'):
    hits, cursor = [], 0
    for line in wrap_words(text, per_line):
        start, cursor = locate_fragment(text, line, cursor)
        hits.append((line, None, 0, 0, 0, key, start))
    return hits


class CoordinateTests(unittest.TestCase):
    def test_norm_anchor_follows_image_across_zoom(self):
        uv = encode('norm', (100, 50, 200, 100), 1.0, (150, 75))
        self.assertEqual(uv, (0.25, 0.25))
        # zoom 2: image is twice as big and moved
        self.assertEqual(decode('norm', (40, 200, 400, 200), 2.0, uv), (140.0, 250.0))

    def test_flow_anchor_scales_vertical_offset_with_zoom(self):
        uv = encode('flow', (10, 100, 300, 500), 1.0, (160, 130))
        self.assertEqual(uv, (0.5, 30.0))
        x, y = decode('flow', (20, 400, 600, 900), 2.0, uv)
        self.assertEqual((x, y), (320.0, 460.0))

    def test_roundtrip_same_layout(self):
        for kind in ('norm', 'flow'):
            rect, pt = (13, 77, 321, 199), (200.5, 140.25)
            back = decode(kind, rect, 1.3, encode(kind, rect, 1.3, pt))
            self.assertAlmostEqual(back[0], pt[0])
            self.assertAlmostEqual(back[1], pt[1])

    def test_eraser_uses_decoded_points(self):
        self.assertTrue(near_any([(100, 100)], (110, 95), 19))
        self.assertFalse(near_any([(100, 100)], (130, 100), 19))


class HighlightTests(unittest.TestCase):
    TEXT = 'Gom mười que lẻ thành một bó chục còn hai que lẻ'

    def test_range_survives_rewrap(self):
        hits_wide = make_hits(self.TEXT, 6)
        # select line 0 char 4 .. line 1 char 3 on the wide wrapping
        ranges = selection_ranges(hits_wide, (0, 4), (1, 3), {'f': self.TEXT})
        merged = merge_ranges(ranges)
        self.assertEqual(len(merged), 1)
        key, start, end = merged[0]
        selected = self.TEXT[start:end]
        # re-wrap narrower: the same characters must be covered
        hits_narrow = make_hits(self.TEXT, 3)
        covered = ''
        for text, _f, _x, _y, _h, k, s in hits_narrow:
            part = clip_range(merged[0], k, s, len(text))
            if part:
                covered += text[part[0]:part[1]]
        self.assertEqual(covered.replace(' ', ''), selected.replace(' ', ''))

    def test_merge_overlap_and_separate_keys(self):
        merged = merge_ranges([('a', 0, 5), ('a', 3, 9), ('a', 20, 25), ('b', 1, 2), ('a', 4, 4)])
        self.assertIn(('a', 0, 9), merged)
        self.assertIn(('a', 20, 25), merged)
        self.assertIn(('b', 1, 2), merged)
        self.assertEqual(len(merged), 3)

    def test_highlight_only_matches_its_own_field(self):
        self.assertIsNone(clip_range(('child1:content', 0, 9), 'child2:content', 0, 9))

    def test_locate_fragment_repeated_words(self):
        text = 'que lẻ que lẻ'
        s1, c = locate_fragment(text, 'que', 0)
        s2, c = locate_fragment(text, 'que', c)
        self.assertEqual((s1, s2), (0, 7))


class ChildModelTests(unittest.TestCase):
    def block(self):
        return {'theme': 'math', 'level': 1, 'lesson': 1, 'order': 1,
                'title': 'Phép cộng có nhớ', 'image': 'media/a.png', 'content': 'Mô tả cũ'}

    def test_migrate_keeps_image_and_moves_description(self):
        old = self.block()
        new = ic.migrate_legacy_block(old)
        self.assertEqual(old, self.block(), 'input must not be modified')
        self.assertEqual(new['layout'], 'image_children')
        self.assertEqual(new['image'], 'media/a.png')
        self.assertEqual(new['children'][0]['content'], 'Mô tả cũ')
        self.assertTrue(new['block_id'].startswith('blk-'))
        self.assertEqual(ic.validate_block(new), [])

    def test_normalize_keeps_ids_and_order_fixes_duplicates(self):
        block = {'layout': 'image_children', 'children': [
            {'id': 'x', 'title': 'A'}, {'id': 'x', 'title': 'B'}, {'title': 'C'}]}
        kids = ic.normalize_children(block)
        self.assertEqual([k['title'] for k in kids], ['A', 'B', 'C'])
        self.assertEqual(kids[0]['id'], 'x')
        self.assertEqual(len({k['id'] for k in kids}), 3)
        self.assertEqual(kids[2]['format'], ic.clean_format(None))

    def test_duplicate_gets_new_id_move_keeps_ids(self):
        kids = [ic.make_child('A'), ic.make_child('B')]
        ids = [k['id'] for k in kids]
        dup = ic.duplicate_child(kids, 0)
        self.assertEqual([k['title'] for k in dup], ['A', 'A', 'B'])
        self.assertNotEqual(dup[0]['id'], dup[1]['id'])
        moved = ic.move_child(dup, 2, 0)
        self.assertEqual([k['title'] for k in moved], ['B', 'A', 'A'])
        self.assertEqual({k['id'] for k in moved}, {k['id'] for k in dup})
        self.assertEqual(dup[0]['id'], ids[0])

    def test_history_undo_restores_order(self):
        kids = [ic.make_child('A'), ic.make_child('B'), ic.make_child('C')]
        history = ic.ChildHistory()
        history.push(kids)
        after = ic.move_child(kids, 0, 2)
        self.assertNotEqual([k['id'] for k in after], [k['id'] for k in kids])
        self.assertEqual(history.undo(), kids)
        self.assertIsNone(history.undo())

    def test_flatten_for_legacy(self):
        block = {'layout': 'image_children', 'title': 'T', 'children': [
            {'id': 'a', 'title': 'Mục 1', 'content': 'x'}, {'id': 'b', 'title': '', 'content': 'y'}]}
        flat = ic.flatten_for_legacy(block)
        self.assertEqual(flat['content'], 'Mục 1\nx\n\ny')
        self.assertEqual(flat['layout'], 'auto')
        self.assertEqual(block['layout'], 'image_children')

    def test_validate_catches_empty_and_duplicate(self):
        self.assertTrue(ic.validate_block({'layout': 'image_children', 'children': []}))
        self.assertTrue(ic.validate_block({'layout': 'image_children',
                                           'children': [{'id': 'a'}, {'id': 'a'}]}))
        self.assertEqual(ic.validate_block({'layout': 'auto'}), [])


class FormatTests(unittest.TestCase):
    def test_size_and_color_cleaned(self):
        fmt = ic.clean_format({'size': '24', 'color': '#FF0000'})
        self.assertEqual((fmt['size'], fmt['color']), (24, '#ff0000'))
        self.assertEqual(ic.parse_color(fmt['color']), (255, 0, 0))
        bad = ic.clean_format({'size': 'abc', 'color': 'red'})
        self.assertEqual((bad['size'], bad['color']), (0, ''))
        self.assertIsNone(ic.parse_color(''))
        self.assertEqual(ic.clean_format({'size': 2})['size'], 8)


class JsonRoundTripTests(unittest.TestCase):
    def test_save_and_reopen_keeps_order_ids_and_unrelated_rows(self):
        import json
        legacy = {'theme': 'vi', 'level': 1, 'lesson': 1, 'order': 1, 'title': 'Cũ', 'content': 'x'}
        block = ic.migrate_legacy_block({'theme': 'math', 'level': 1, 'lesson': 1, 'order': 2,
                                         'title': 'Cộng', 'image': 'media/a.png', 'content': 'mô tả'})
        block['children'].append(ic.make_child('Mục 2', 'nội dung', {'bold': True}))
        block['children'] = ic.move_child(block['children'], 1, 0)
        rows = [legacy, block]
        saved = json.loads(json.dumps(rows, ensure_ascii=False))
        self.assertEqual(saved[0], legacy)
        reopened = saved[1]
        self.assertEqual([c['id'] for c in reopened['children']], [c['id'] for c in block['children']])
        self.assertEqual(reopened['children'][0]['title'], 'Mục 2')
        self.assertEqual(ic.normalize_children(reopened), reopened['children'])
        self.assertEqual(ic.validate_block(reopened), [])


class PagerTests(unittest.TestCase):
    def test_resume_child_when_returning_and_start_at_first_for_new(self):
        a = {'layout': 'image_children', 'children': [{}, {}, {}]}
        legacy = {'layout': 'auto'}
        b = {'layout': 'image_children', 'children': [{}, {}]}
        pager = ic.Pager([a, legacy, b])
        pager.set_child(2)
        self.assertTrue(pager.step_block(1))
        self.assertEqual(pager.child, 0)
        self.assertTrue(pager.step_block(1))
        self.assertEqual(pager.child, 0)
        pager.set_child(1)
        pager.step_block(-1); pager.step_block(-1)
        self.assertEqual(pager.child, 2)
        pager.step_block(2)
        self.assertEqual(pager.child, 1)

    def test_bounds(self):
        pager = ic.Pager([{'layout': 'image_children', 'children': [{}]}])
        self.assertFalse(pager.step_block(1))
        self.assertFalse(pager.can_step(-1))
        pager.set_child(99)
        self.assertEqual(pager.child, 0)


if __name__ == '__main__':
    unittest.main()
