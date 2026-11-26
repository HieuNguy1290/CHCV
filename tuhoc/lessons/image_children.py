"""Data model for the ``image_children`` ("Hình + nội dung") block layout.

One row of ``level_blocks.json`` stays one big block. This layout adds a stable
``block_id`` and an ordered ``children`` list::

    {"theme": ..., "level": ..., "lesson": ..., "order": 1,
     "layout": "image_children", "block_id": "blk-1a2b3c4d5e",
     "title": "Phép cộng có nhớ", "image": "media/que_tinh.png",
     "children": [{"id": "ch-...", "title": "...", "content": "...",
                   "format": {"font": "", "bold": false,
                              "italic": false, "underline": false}}]}

Pure Python: no tkinter/pygame, so it is unit-testable headless.
"""
import copy
import re
from uuid import uuid4

LAYOUT = 'image_children'
FONT_CHOICES = ('', 'Segoe UI', 'Arial', 'Tahoma', 'Verdana', 'Times New Roman')


def new_id(prefix):
    return f'{prefix}-{uuid4().hex[:10]}'


def is_image_children(block):
    return str((block or {}).get('layout') or '') == LAYOUT


def _clean_size(value):
    """Font size in px; 0 means "use the default size"."""
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return 0
    return 0 if number <= 0 else max(8, min(96, number))


def _clean_color(value):
    value = str(value or '').strip()
    return value.lower() if re.fullmatch(r'#[0-9a-fA-F]{6}', value) else ''


def parse_color(value):
    """'#rrggbb' -> (r, g, b), or None for the default colour."""
    value = _clean_color(value)
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5)) if value else None


def clean_format(fmt):
    fmt = fmt if isinstance(fmt, dict) else {}
    return {'font': str(fmt.get('font') or ''),
            'size': _clean_size(fmt.get('size')),
            'color': _clean_color(fmt.get('color')),
            'bold': bool(fmt.get('bold')),
            'italic': bool(fmt.get('italic')),
            'underline': bool(fmt.get('underline'))}


def make_child(title='', content='', fmt=None, taken=()):
    """New child with an id that is not in ``taken``."""
    child_id = new_id('ch')
    while child_id in taken:
        child_id = new_id('ch')
    return {'id': child_id, 'title': str(title), 'content': str(content),
            'format': clean_format(fmt)}


def normalize_children(block):
    """Return a clean copy of ``block['children']``.

    Keeps existing ids and order; assigns an id only to children that have none
    or whose id repeats. Never reorders.
    """
    seen, out = set(), []
    for raw in (block or {}).get('children') or []:
        raw = raw if isinstance(raw, dict) else {}
        child = copy.deepcopy(raw)
        child_id = str(child.get('id') or '')
        if not child_id or child_id in seen:
            child_id = make_child(taken=seen)['id']
        seen.add(child_id)
        child['id'] = child_id
        child['title'] = str(child.get('title') or '')
        child['content'] = str(child.get('content') or '')
        child['format'] = clean_format(child.get('format'))
        out.append(child)
    return out


def ensure_block_id(block):
    if not block.get('block_id'):
        block['block_id'] = new_id('blk')
    return block['block_id']


def migrate_legacy_block(block):
    """Switch a legacy block to ``image_children`` on request.

    Keeps the image and block title; the old description becomes the first
    child. Returns a new dict (the input is not modified).
    """
    new = copy.deepcopy(block)
    if is_image_children(new):
        new['children'] = normalize_children(new) or [make_child()]
        ensure_block_id(new)
        return new
    description = str(new.get('content') or '')
    new['layout'] = LAYOUT
    new['children'] = [make_child(content=description)]
    new['content'] = ''
    ensure_block_id(new)
    return new


def flatten_for_legacy(block):
    """Plain block for old viewers (Tk lesson page): children as text."""
    if not is_image_children(block):
        return block
    flat = copy.deepcopy(block)
    parts = []
    for child in normalize_children(block):
        head = child['title'].strip()
        body = child['content'].strip()
        parts.append('\n'.join(x for x in (head, body) if x))
    flat['content'] = '\n\n'.join(parts)
    flat['layout'] = 'auto'
    return flat


def duplicate_child(children, index):
    """Insert a clone (fresh id) right after ``index``; returns new list."""
    clone = copy.deepcopy(children[index])
    clone['id'] = make_child(taken={c['id'] for c in children})['id']
    return [*children[:index + 1], clone, *children[index + 1:]]


def move_child(children, src, dst):
    """Reorder only; ids and content are untouched."""
    if not (0 <= src < len(children)):
        return list(children)
    dst = max(0, min(len(children) - 1, dst))
    items = list(children)
    items.insert(dst, items.pop(src))
    return items


def validate_block(block):
    """List of problems that would stop saving an image_children block."""
    if not is_image_children(block):
        return []
    problems = []
    children = block.get('children') or []
    if not children:
        problems.append('Cần ít nhất một mục.')
    ids = [str(c.get('id') or '') for c in children if isinstance(c, dict)]
    if len(ids) != len(set(ids)) or '' in ids:
        problems.append('Mã mục bị trùng hoặc trống.')
    return problems


class ChildHistory:
    """Undo stack of children snapshots (drag / delete / duplicate)."""

    def __init__(self, limit=50):
        self._stack, self._limit = [], limit

    def push(self, children):
        self._stack.append(copy.deepcopy(children))
        del self._stack[:-self._limit]

    def undo(self):
        return self._stack.pop() if self._stack else None

    def clear(self):
        self._stack.clear()

    def __len__(self):
        return len(self._stack)


class Pager:
    """Which big block and which child the viewer is showing.

    Moving to a block never seen before starts at its first child; returning
    to a block resumes the child last viewed there.
    """

    def __init__(self, blocks):
        self.blocks = list(blocks)
        self.block = 0
        self._child = {}

    def child_count(self, index=None):
        block = self.blocks[self.block if index is None else index]
        return len(block.get('children') or []) if is_image_children(block) else 0

    @property
    def child(self):
        count = self.child_count()
        return max(0, min(count - 1, self._child.get(self.block, 0))) if count else 0

    def set_child(self, index):
        count = self.child_count()
        if count:
            self._child[self.block] = max(0, min(count - 1, int(index)))

    def step_block(self, delta):
        target = self.block + delta
        if 0 <= target < len(self.blocks):
            self.block = target
            return True
        return False

    def can_step(self, delta):
        return 0 <= self.block + delta < len(self.blocks)
