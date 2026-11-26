"""Pure coordinate and highlight helpers for the Pygame lesson window.

No pygame/tkinter imports, so the logic can be unit-tested headless.

Marks are stored relative to an *anchor* (an image, a block, a child column or
the page) instead of raw window pixels, so they stay aligned after zoom,
scroll or text re-wrap:

* ``norm`` anchors (images): ``(u, v)`` are fractions of the anchor rect.
* ``flow`` anchors (text areas): ``u`` is a fraction of the anchor width and
  ``v`` is a vertical offset in zoom-1 pixels from the anchor top.

Highlights are stored as character ranges in the source text of a field, so
re-wrapping the text at another zoom still highlights the same characters.
"""

NORM = 'norm'
FLOW = 'flow'


def encode(kind, rect, zoom, point):
    """Window/document point -> anchor-relative ``(u, v)``."""
    x, y, w, h = rect
    zoom = float(zoom) or 1.0
    if kind == NORM:
        return ((point[0] - x) / max(1.0, w), (point[1] - y) / max(1.0, h))
    return ((point[0] - x) / max(1.0, w), (point[1] - y) / zoom)


def decode(kind, rect, zoom, uv):
    """Anchor-relative ``(u, v)`` -> document point for the current layout."""
    x, y, w, h = rect
    zoom = float(zoom) or 1.0
    if kind == NORM:
        return (x + uv[0] * w, y + uv[1] * h)
    return (x + uv[0] * w, y + uv[1] * zoom)


def locate_fragment(text, fragment, cursor):
    """Find ``fragment`` in the source ``text`` at/after ``cursor``.

    Fragments are drawn in reading order, so a running cursor maps wrapped
    lines (or justified words) back to source offsets.
    Returns ``(start, new_cursor)``.
    """
    start = str(text).find(fragment, cursor) if fragment else -1
    if start < 0:
        start = min(cursor, len(text))
    return start, start + len(fragment)


def selection_ranges(hits, a, b, texts=None):
    """Convert a drag selection into source ranges.

    ``hits`` rows are ``(text, font, x, doc_y, line_h, key, src_start)``;
    ``a`` and ``b`` are ordered ``(hit_index, char_offset)`` pairs.
    ``texts`` maps field key -> full source text. When given, rows that are
    followed by more selected rows are extended over the whitespace at the
    line break, so a later re-wrap leaves no unhighlighted gap.
    """
    out = []
    last = min(b[0], len(hits) - 1)
    for i in range(a[0], last + 1):
        text, key, src_start = hits[i][0], hits[i][5], hits[i][6]
        left = a[1] if i == a[0] else 0
        right = b[1] if i == b[0] else len(text)
        if key is None or right <= left:
            continue
        end = src_start + right
        if i < last and texts and key in texts and right >= len(text):
            source = texts[key]
            while end < len(source) and source[end].isspace():
                end += 1
        out.append((key, src_start + left, end))
    return out


def merge_ranges(ranges):
    """Merge overlapping/touching ``(key, start, end)`` ranges per key."""
    grouped = {}
    for key, start, end in ranges:
        if end > start:
            grouped.setdefault(key, []).append((start, end))
    merged = []
    for key, items in grouped.items():
        items.sort()
        cur = None
        for start, end in items:
            if cur is not None and start <= cur[1]:
                cur[1] = max(cur[1], end)
            else:
                if cur is not None:
                    merged.append((key, cur[0], cur[1]))
                cur = [start, end]
        merged.append((key, cur[0], cur[1]))
    return merged


def clip_range(highlight, key, frag_start, frag_len):
    """Part of a highlight covering a drawn fragment, in fragment offsets."""
    h_key, start, end = highlight
    if h_key != key:
        return None
    left = max(start, frag_start) - frag_start
    right = min(end, frag_start + frag_len) - frag_start
    return (left, right) if right > left else None


def near_any(points, target, radius):
    """True when any stored point lies within ``radius`` px of ``target``."""
    return any(abs(p[0] - target[0]) < radius and abs(p[1] - target[1]) < radius
               for p in points)
