import math
import unittest

from tuhoc.lessons.flashcard_logic import Deck, FlipAnim, clean_word, wrap_words


class FlipTests(unittest.TestCase):
    def test_flip_swaps_face_at_half_and_is_edge_on_there(self):
        anim = FlipAnim(400)
        anim.flip(1000)
        self.assertFalse(FlipAnim.showing_back(anim.value(1000)))
        self.assertAlmostEqual(anim.value(1200), 0.5, places=6)
        self.assertLess(FlipAnim.width_scale(anim.value(1200)), 0.05)
        self.assertTrue(FlipAnim.showing_back(anim.value(1400)))
        self.assertEqual(anim.value(2000), 1.0)
        self.assertAlmostEqual(FlipAnim.width_scale(1.0), 1.0)

    def test_flip_back_and_midway_reversal(self):
        anim = FlipAnim(400)
        anim.flip(0)
        anim.flip(100)                      # reversed before finishing
        self.assertEqual(anim.target, 0.0)
        self.assertGreater(anim.value(100), 0.0)
        self.assertEqual(anim.value(1000), 0.0)

    def test_height_hint_is_small(self):
        self.assertGreaterEqual(FlipAnim.height_scale(0.5), 0.9)
        self.assertEqual(FlipAnim.height_scale(0.0), 1.0)


class DeckTests(unittest.TestCase):
    def cards(self):
        return [{'id': i, 'word': f'w{i}'} for i in (1, 2, 3)]

    def test_again_returns_once_then_done(self):
        deck = Deck(self.cards())
        self.assertEqual(deck.rate('again')[0]['id'], 1)
        self.assertEqual([c['id'] for c in deck.queue], [2, 3, 1])
        deck.rate('good'); deck.rate('good')
        self.assertEqual(deck.current['id'], 1)
        deck.rate('again')                  # second 'again': no more repeats
        self.assertTrue(deck.finished)
        self.assertEqual(deck.done, 3)
        self.assertEqual(deck.counts, {'again': 2, 'hard': 0, 'good': 2})

    def test_skip_and_invalid_rating(self):
        deck = Deck(self.cards())
        deck.skip()
        self.assertEqual(deck.current['id'], 2)
        self.assertIsNone(deck.rate('maybe'))
        self.assertEqual(len(deck.queue), 3)
        self.assertIsNone(Deck([]).rate('good'))


class TextTests(unittest.TestCase):
    def test_wrap_and_blank_lines(self):
        measure = lambda s: len(s) * 10
        self.assertEqual(wrap_words('aa bb cc dd', measure, 55), ['aa bb', 'cc dd'])
        self.assertEqual(wrap_words('a\n\nb', measure, 100), ['a', '', 'b'])
        self.assertEqual(wrap_words('averyveryverylongword x', measure, 50), ['averyveryverylongword', 'x'])

    def test_clean_word(self):
        self.assertEqual(clean_word('[VI] xin chào'), 'xin chào')
        self.assertEqual(clean_word('hello'), 'hello')


if __name__ == '__main__':
    unittest.main()
