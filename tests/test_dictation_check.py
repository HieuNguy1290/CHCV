"""Chấm chép chính tả và kiểm tra đáp án nhập tay (không cần tkinter/pygame)."""
import sys
import types
import unittest


def _stub_modules():
    if 'tkinter' not in sys.modules:
        tk = types.ModuleType('tkinter')
        tk.Canvas = type('Canvas', (), {})
        tk.Frame = object
        tk.filedialog = types.ModuleType('tkinter.filedialog')
        tk.messagebox = types.ModuleType('tkinter.messagebox')
        sys.modules.update({'tkinter': tk, 'tkinter.filedialog': tk.filedialog,
                            'tkinter.messagebox': tk.messagebox})
    if 'pygame' not in sys.modules:
        sys.modules['pygame'] = types.ModuleType('pygame')


_stub_modules()
from tuhoc.lessons.dictation_vi import check_dictation, text_tokens  # noqa: E402
from tuhoc.exercises.image_write_extension import correct  # noqa: E402


class DictationCheck(unittest.TestCase):
    def passed(self, expected, given, *args):
        return check_dictation(expected, given, *args)['passed']

    def test_case_and_punctuation_ignored(self):
        self.assertTrue(self.passed('Sáng nay, má dẫn em ra chợ.', 'sáng nay má dẫn em ra chợ'))

    def test_missing_tone_marks_fail(self):
        self.assertFalse(self.passed('Má dẫn em', 'Ma dan em'))

    def test_old_and_new_tone_placement_equal(self):
        for new, old in [('hòa bình', 'hoà bình'), ('khỏe', 'khoẻ'), ('thủy', 'thuỷ'),
                         ('tòa lòe', 'toà loè'), ('họa sĩ', 'hoạ sĩ')]:
            self.assertTrue(self.passed(new, old), (new, old))

    def test_tone_placement_rule_leaves_other_words_alone(self):
        for word in ['quý', 'quỳ', 'hoài', 'hoàn', 'toán', 'loạn', 'huỳnh', 'thuyền', 'mùa',
                     'của', 'hoằng', 'hoặc', 'xoắn', 'khuyên', 'hoạt', 'tuổi']:
            import unicodedata
            self.assertEqual(text_tokens(word), [unicodedata.normalize('NFC', word)], word)

    def test_different_words_still_differ(self):
        self.assertFalse(self.passed('hòa bình', 'hỏa bình'))

    def test_extra_words_do_not_score_100(self):
        result = check_dictation('Em đi học.', 'Em đi học nè')
        self.assertFalse(result['passed'])
        self.assertEqual(result['score'], 75.0)

    def test_missing_words_score(self):
        self.assertEqual(check_dictation('Em đi học.', 'Em đi')['score'], 66.7)

    def test_whole_answer_variants(self):
        self.assertTrue(self.passed('hòa bình', 'Hoà bình!', ['hòa bình ơi']))


class ImageWriteCorrect(unittest.TestCase):
    def test_accepted_answers_string_is_split_not_exploded(self):
        q = {'answer': 'Con mèo', 'accepted_answers': 'mèo | con mèo con'}
        self.assertTrue(correct(q, 'MÈO'))
        self.assertTrue(correct(q, '  con   mèo con '))
        self.assertFalse(correct(q, 'm'))

    def test_blank_never_correct(self):
        self.assertFalse(correct({'answer': 'a'}, '   '))


if __name__ == '__main__':
    unittest.main()
