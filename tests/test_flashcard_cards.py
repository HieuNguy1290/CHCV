import random
import tempfile
import unittest
from pathlib import Path

from tuhoc.lessons import card_media
from tuhoc.lessons.flashcard_logic import assign_directions, can_reverse, face_content, fit_lines
from tuhoc.lessons.flashcard_themes import PRESETS, resolve_theme, tint_for_image


class DirectionTests(unittest.TestCase):
    def cards(self):
        return [{'id': 1, 'word': 'cat', 'meaning': 'mèo'},
                {'id': 2, 'word': 'dog', 'meaning': ''},                        # no meaning at all
                {'id': 3, 'word': 'sun', 'meaning': '', 'meaning_image': 'sun.png'}]   # picture-only meaning

    def test_forward_reverse_and_cards_without_meaning(self):
        forward = assign_directions(self.cards(), 'forward')
        self.assertEqual({c['direction'] for c in forward}, {'forward'})
        reverse = assign_directions(self.cards(), 'reverse')
        self.assertEqual([c['direction'] for c in reverse], ['reverse', 'forward', 'reverse'])
        self.assertFalse(can_reverse({'word': 'x'}))
        self.assertTrue(can_reverse({'word': 'x', 'meaning_image': 'a.png'}))

    def test_shuffle_mixes_but_never_reverses_empty_meaning(self):
        rng = random.Random(7)
        directions = set()
        for _ in range(40):
            cards = assign_directions(self.cards(), 'shuffle', rng)
            directions.add(cards[0]['direction'])
            self.assertEqual(cards[1]['direction'], 'forward')
        self.assertEqual(directions, {'forward', 'reverse'})

    def test_face_content_follows_direction(self):
        card = {'word': 'cat', 'meaning': 'mèo', 'word_image': 'w.png', 'meaning_image': 'm.png', 'direction': 'forward'}
        self.assertEqual(face_content(card, 'front'), ('cat', 'w.png'))
        self.assertEqual(face_content(card, 'back'), ('mèo', 'm.png'))
        card['direction'] = 'reverse'
        self.assertEqual(face_content(card, 'front'), ('mèo', 'm.png'))
        self.assertEqual(face_content(card, 'back'), ('cat', 'w.png'))
        self.assertEqual(face_content({'word': 'a'}, 'back'), ('', ''))


class FitTests(unittest.TestCase):
    measure = staticmethod(lambda size, s: len(s) * size // 2)
    height = staticmethod(lambda size: size + 4)

    def test_short_text_gets_biggest_size(self):
        size, lines = fit_lines('cat', (60, 40, 20), self.measure, self.height, 400, 200)
        self.assertEqual((size, lines), (60, ['cat']))

    def test_long_text_shrinks_and_wraps(self):
        text = 'one two three four five six seven eight nine ten'
        size, lines = fit_lines(text, (60, 40, 20), self.measure, self.height, 300, 120)
        self.assertLess(size, 60)
        self.assertLessEqual(len(lines) * self.height(size), 120)
        self.assertEqual(' '.join(lines), text)

    def test_overflow_is_cut_with_ellipsis(self):
        size, lines = fit_lines('word ' * 200, (20,), self.measure, self.height, 100, 48)
        self.assertEqual(size, 20)
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[-1].endswith('…'))


class ThemeTests(unittest.TestCase):
    def test_fallbacks_and_presets(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(resolve_theme(None, folder)['id'], 'classic')
            self.assertEqual(resolve_theme({'id': 'nope'}, folder)['id'], 'classic')
            self.assertEqual(resolve_theme({'id': 'navy'}, folder)['kind'], 'color')
            self.assertEqual(resolve_theme({'id': 'custom', 'image': 'missing.png'}, folder)['id'], 'classic')
            self.assertEqual(len({p['id'] for p in PRESETS}), len(PRESETS))

    def test_custom_image_is_resolved_inside_folder_only(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'bg.png').write_bytes(b'x')
            theme = resolve_theme({'id': 'custom', 'image': 'bg.png'}, folder)
            self.assertEqual((theme['kind'], Path(theme['image_path']).name), ('image', 'bg.png'))
            escaped = resolve_theme({'id': 'custom', 'image': '../../etc/passwd'}, folder)
            self.assertEqual(escaped['id'], 'classic')

    def test_tint_keeps_text_readable(self):
        self.assertEqual(tint_for_image((250, 250, 250))[2], (35, 52, 94))      # bright picture -> dark text
        self.assertEqual(tint_for_image((10, 10, 10))[2], (255, 255, 255))      # dark picture -> light text


class MediaTests(unittest.TestCase):
    def make_png(self, path, size=(3000, 2000), mode='RGB'):
        from PIL import Image
        Image.new(mode, size, (200, 30, 30) if mode == 'RGB' else (200, 30, 30, 128)).save(path)

    def test_import_shrinks_and_copies(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'big.png'
            self.make_png(source)
            name = card_media.import_image(source, Path(tmp) / 'store', max_side=1200)
            stored = card_media.image_path(Path(tmp) / 'store', name)
            self.assertIsNotNone(stored)
            with Image.open(stored) as img:
                self.assertEqual(max(img.size), 1200)
            source.unlink()                                                  # original may disappear
            self.assertTrue(stored.is_file())

    def test_alpha_png_stays_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'a.png'
            self.make_png(source, (50, 50), 'RGBA')
            self.assertTrue(card_media.import_image(source, Path(tmp) / 's').endswith('.png'))

    def test_rejects_bad_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'x.txt'
            bad.write_text('hi')
            fake = Path(tmp) / 'fake.png'
            fake.write_text('not an image')
            for path in (bad, fake, Path(tmp) / 'missing.png'):
                with self.assertRaises(ValueError):
                    card_media.import_image(path, Path(tmp) / 's')

    def test_remove_if_unused_and_path_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / 's'
            store.mkdir()
            (store / 'a.png').write_bytes(b'x')
            card_media.remove_if_unused(store, 'a.png', in_use=True)
            self.assertTrue((store / 'a.png').exists())
            card_media.remove_if_unused(store, 'a.png', in_use=False)
            self.assertFalse((store / 'a.png').exists())
            self.assertIsNone(card_media.image_path(store, '../outside.png'))
            self.assertIsNone(card_media.image_path(store, ''))


if __name__ == '__main__':
    unittest.main()
