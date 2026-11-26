"""Pure logic for the Pygame flashcard window (no pygame/tkinter imports)."""
import math
import random

RATINGS = ('again', 'hard', 'good')


def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


class FlipAnim:
    """2D flip: width follows |cos(angle)|; the face swaps at the halfway point."""

    def __init__(self, duration_ms=380):
        self.duration = duration_ms
        self.start_value = 0.0      # 0 = front, 1 = back
        self.target = 0.0
        self.started_at = 0

    def value(self, now):
        if self.duration <= 0:
            return self.target
        progress = max(0.0, min(1.0, (now - self.started_at) / self.duration))
        eased = ease_in_out(progress)
        return self.start_value + (self.target - self.start_value) * eased

    def flip(self, now):
        self.start_value = self.value(now)
        self.target = 1.0 - round(self.target)
        self.started_at = now

    def reset(self, now=0):
        self.start_value = self.target = 0.0
        self.started_at = now

    def busy(self, now):
        return now - self.started_at < self.duration and self.start_value != self.target

    @staticmethod
    def showing_back(value):
        return value >= 0.5

    @staticmethod
    def width_scale(value):
        """1.0 face-on, ~0 edge-on at the middle of the flip."""
        return max(0.02, abs(math.cos(value * math.pi)))

    @staticmethod
    def height_scale(value):
        """Slight shrink while turning, to hint at perspective."""
        return 1.0 - 0.06 * math.sin(value * math.pi)


class Deck:
    """Review queue. 'again' cards come back once at the end of the session."""

    def __init__(self, cards, max_repeats=1):
        self.queue = [dict(card) for card in cards]
        self.total = len(self.queue)
        self.max_repeats = max_repeats
        self._repeats = {}
        self.counts = {rating: 0 for rating in RATINGS}
        self.done = 0

    @property
    def current(self):
        return self.queue[0] if self.queue else None

    @property
    def finished(self):
        return not self.queue

    def rate(self, rating):
        """Record a rating; returns ``(card, rating)`` or None when finished."""
        if rating not in RATINGS or not self.queue:
            return None
        card = self.queue.pop(0)
        self.counts[rating] += 1
        key = card.get('id')
        if rating == 'again' and self._repeats.get(key, 0) < self.max_repeats:
            self._repeats[key] = self._repeats.get(key, 0) + 1
            self.queue.append(card)
        else:
            self.done += 1
        return card, rating

    def skip(self):
        if len(self.queue) > 1:
            self.queue.append(self.queue.pop(0))


def wrap_words(text, measure, width):
    """Greedy word wrap; ``measure(str) -> pixel width``. Keeps blank lines."""
    lines = []
    for paragraph in str(text).split('\n'):
        words, line = paragraph.split(), ''
        if not words:
            lines.append('')
            continue
        for word in words:
            trial = f'{line} {word}'.strip()
            if line and measure(trial) > width:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
    return lines


def clean_word(raw):
    return str(raw or '').removeprefix('[VI] ')


# --- review direction ---------------------------------------------------------------------------
MODES = ('forward', 'reverse', 'shuffle')      # Từ→Nghĩa, Nghĩa→Từ, Shuffle (mixed)


def can_reverse(card):
    """A card can show the meaning first only when it has a meaning (text or picture)."""
    return bool(str(card.get('meaning') or '').strip() or card.get('meaning_image'))


def assign_directions(cards, mode, rng=None):
    """Set ``card['direction']``. Cards without a meaning always stay Từ→Nghĩa."""
    rng = rng or random
    for card in cards:
        if mode == 'reverse' and can_reverse(card):
            card['direction'] = 'reverse'
        elif mode == 'shuffle' and can_reverse(card):
            card['direction'] = rng.choice(('forward', 'reverse'))
        else:
            card['direction'] = 'forward'
    return cards


def face_content(card, side):
    """``(text, image_path)`` shown on 'front' or 'back' for the card's direction."""
    word = (str(card.get('word') or ''), card.get('word_image') or '')
    meaning = (str(card.get('meaning') or ''), card.get('meaning_image') or '')
    first, second = (meaning, word) if card.get('direction') == 'reverse' else (word, meaning)
    return first if side == 'front' else second


def fit_lines(text, sizes, measure, line_height, max_w, max_h, max_lines=8):
    """Largest size whose wrapped text fits the box -> ``(size, lines)``.

    ``measure(size, s)`` gives pixel width, ``line_height(size)`` the row height.
    When even the smallest size overflows, rows are cut and the last one ends with an ellipsis.
    """
    for size in sizes:
        lines = wrap_words(text, lambda s, z=size: measure(z, s), max_w)
        if (len(lines) <= max_lines and len(lines) * line_height(size) <= max_h
                and all(measure(size, line) <= max_w for line in lines)):
            return size, lines
    size = sizes[-1]
    lines = wrap_words(text, lambda s: measure(size, s), max_w)
    room = max(1, min(max_lines, int(max_h // max(1, line_height(size)))))
    if len(lines) > room:
        lines = lines[:room]
        lines[-1] = lines[-1].rstrip() + '…'
    return size, lines

