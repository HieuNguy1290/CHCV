"""Annotation tools for the Pygame exercise windows.

Tools: pen, highlighter, frame (rect), note (text), strike-through line,
eraser, undo/redo, clear, colour palette and a draggable scratch pad.

Two layers, so the logic can be tested without a display:

* AnnotationStore  - pure Python. Strokes live in DOCUMENT coordinates (the
  same space as the scrollable question surface), with undo/redo.
* ExerciseTools    - pygame glue: collapsible dock, event routing and drawing.

Rules that keep it from fighting the exercise itself:

* Default tool is 'select' (= no tool). Clicks reach the answers untouched.
* Only the viewport (VIEW_TOP..VIEW_BOTTOM) is drawable, so the header and
  the fixed 'Hoan thanh' footer are never covered or clicked through.
* Keyboard uses Alt+letter / Ctrl+Z / Ctrl+Y only. Plain letters and 1-8
  stay free for typing and answer selection.
* ESC first returns to 'select'; only the next ESC reaches the exit dialog.
* Wheel scrolling is never consumed.
"""
from __future__ import annotations

import math

VIEW_TOP, VIEW_BOTTOM, VIEW_RIGHT = 90, 565, 934   # matches the click guard in pygame_exercises
WIDTH, HEIGHT = 960, 640

PALETTE = [(230, 50, 70), (255, 211, 35), (65, 155, 255), (65, 205, 145),
           (175, 105, 245), (20, 20, 20), (255, 140, 40)]
DEFAULT_COLORS = {'pen': (230, 50, 70), 'highlight': (255, 211, 35), 'rect': (65, 155, 255),
                  'text': (30, 70, 170), 'strike': (90, 90, 105)}
COLORABLE = ('pen', 'highlight', 'rect', 'text')
MAX_TEXT = 80
AA = 3                     # supersampling factor for anti-aliased drawing
LIVE_CHUNK = 80            # while drawing, finished pen segments of this many points are cached
WIDTHS = {'pen': 4, 'highlight': 18, 'rect': 3, 'strike': 5, 'text': 20}
HIGHLIGHT_ALPHA = 105
ERASER_RADIUS = 14
MIN_POINT_GAP = 2.0
MAX_POINTS = 4000          # per stroke; a runaway drag cannot grow without bound
MAX_STROKES = 400


# --------------------------------------------------------------------------
# Pure logic
# --------------------------------------------------------------------------
def _seg_distance(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(p[0] - ax, p[1] - ay)
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))


def stroke_hit(stroke, point, radius):
    """True when `point` (document coords) touches the stroke within `radius`."""
    pts = stroke['pts']
    if stroke['tool'] == 'text':
        w, h = stroke.get('box') or (len(stroke.get('text', '')) * 11 + 10, 26)
        x, y = pts[0]
        return x - radius <= point[0] <= x + w + radius and y - radius <= point[1] <= y + h + radius
    reach = radius + stroke['width'] / 2.0
    if len(pts) == 1:
        return math.hypot(point[0] - pts[0][0], point[1] - pts[0][1]) <= reach
    return any(_seg_distance(point, pts[i], pts[i + 1]) <= reach for i in range(len(pts) - 1))


def new_stroke(tool, color, point):
    stroke = {'tool': tool, 'color': tuple(color), 'width': WIDTHS[tool],
              'pts': [(float(point[0]), float(point[1]))]}
    if tool in ('rect', 'strike'):
        stroke['anchor'] = stroke['pts'][0]
    if tool == 'text':
        stroke['text'] = ''
    return stroke


def _rect_points(a, b):
    x1, y1, x2, y2 = min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]


def extend_stroke(stroke, point):
    """Update a stroke while dragging. Returns True when it changed."""
    tool = stroke['tool']
    if tool == 'rect':
        stroke['pts'] = _rect_points(stroke['anchor'], point)
        return True
    if tool == 'strike':
        ax, ay = stroke['anchor']
        y = ay if abs(point[1] - ay) <= 12 else float(point[1])     # snap to a level strike-through
        stroke['pts'] = [(ax, ay), (float(point[0]), y)]
        return True
    if len(stroke['pts']) >= MAX_POINTS:
        return False
    lx, ly = stroke['pts'][-1]
    if math.hypot(point[0] - lx, point[1] - ly) < MIN_POINT_GAP:
        return False
    stroke['pts'].append((float(point[0]), float(point[1])))
    return True


def stroke_ok(stroke):
    """Reject accidental clicks that would leave an invisible rectangle/line."""
    pts = stroke['pts']
    if stroke['tool'] == 'rect':
        return len(pts) == 5 and (abs(pts[2][0] - pts[0][0]) >= 6 or abs(pts[2][1] - pts[0][1]) >= 6)
    if stroke['tool'] == 'strike':
        return len(pts) == 2 and math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]) >= 8
    if stroke['tool'] == 'text':
        return bool(stroke.get('text', '').strip())
    return True


def smooth_points(pts, iterations=2, max_points=6000):
    """Chaikin corner cutting: turns the coarse polyline of mouse samples into a smooth curve.

    Endpoints are kept. Stops early so a very long stroke cannot explode in size.
    """
    pts = list(pts)
    for _ in range(iterations):
        if len(pts) < 3 or len(pts) * 2 > max_points:
            break
        out = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        out.append(pts[-1])
        pts = out
    return pts


class AnnotationStore:
    """Strokes plus undo/redo. Operations: add, erase (grouped per drag), clear."""

    def __init__(self):
        self.items = []
        self._undo = []
        self._redo = []
        self._pending = None          # strokes removed during the current erase drag

    # -- queries
    @property
    def can_undo(self):
        return bool(self._undo)

    @property
    def can_redo(self):
        return bool(self._redo)

    # -- edits
    def add(self, stroke):
        if len(self.items) >= MAX_STROKES:
            # Drop the oldest silently rather than refuse the user's drawing.
            self.items.pop(0)
            self._undo.clear()
        self.items.append(stroke)
        self._undo.append(('add', stroke))
        self._redo.clear()

    def begin_erase(self):
        self._pending = list(self.items)          # snapshot: indices stay stable across the drag

    def erase_at(self, point, radius=ERASER_RADIUS):
        """Remove every stroke touched by `point`. Returns how many were removed."""
        if self._pending is None:
            self.begin_erase()
        hits = [s for s in self.items if stroke_hit(s, point, radius)]
        if hits:
            ids = {id(s) for s in hits}
            self.items[:] = [s for s in self.items if id(s) not in ids]
        return len(hits)

    def end_erase(self):
        snapshot, self._pending = self._pending, None
        if not snapshot:
            return
        alive = {id(s) for s in self.items}
        removed = [(i, s) for i, s in enumerate(snapshot) if id(s) not in alive]
        if removed:
            self._undo.append(('del', removed))   # ascending original indices
            self._redo.clear()

    def clear(self):
        if self.items:
            self._undo.append(('clear', list(self.items)))
            self._redo.clear()
            self.items.clear()

    # -- history
    def undo(self):
        if not self._undo:
            return False
        op = self._undo.pop()
        kind, data = op
        if kind == 'add':
            self.items[:] = [x for x in self.items if x is not data]
        elif kind == 'del':
            for index, stroke in data:                 # ascending, so indices stay valid
                self.items.insert(min(index, len(self.items)), stroke)
        elif kind == 'clear':
            self.items[:] = data
        self._redo.append(op)
        return True

    def redo(self):
        if not self._redo:
            return False
        op = self._redo.pop()
        kind, data = op
        if kind == 'add':
            self.items.append(data)
        elif kind == 'del':
            gone = {id(stroke) for _, stroke in data}
            self.items[:] = [x for x in self.items if id(x) not in gone]
        elif kind == 'clear':
            self.items.clear()
        self._undo.append(op)
        return True


# --------------------------------------------------------------------------
# pygame glue
# --------------------------------------------------------------------------
# Bottom-to-top order of the vertical dock (index 0 sits at the bottom-left).
BUTTONS = ('toggle', 'pen', 'highlight', 'rect', 'text', 'strike', 'eraser',
           'undo', 'redo', 'clear', 'color', 'scratch')
TOOL_BUTTONS = ('pen', 'highlight', 'rect', 'text', 'strike', 'eraser')
TIPS = {'toggle': 'Công cụ', 'pen': 'Bút (Alt+P)', 'highlight': 'Highlight (Alt+H)',
        'rect': 'Khung (Alt+R)', 'text': 'Ghi chú (Alt+T)', 'strike': 'Gạch đáp án (Alt+X)',
        'eraser': 'Tẩy (Alt+E)', 'undo': 'Hoàn tác (Ctrl+Z)', 'redo': 'Làm lại (Ctrl+Y)',
        'clear': 'Xóa hết ghi chú', 'color': 'Màu', 'scratch': 'Giấy nháp (Alt+N)'}
ALT_KEYS = {'p': 'pen', 'h': 'highlight', 'r': 'rect', 't': 'text', 'x': 'strike', 'e': 'eraser'}
PANEL, PANEL_EDGE = (33, 52, 79), (60, 84, 118)
ACTIVE, HOVER, INK, DIM = (30, 146, 110), (58, 84, 120), (255, 255, 255), (120, 136, 160)
BTN, STEP, DOCK_X, DOCK_Y = 36, 38, 22, 582        # DOCK_Y = top of the bottom (toggle) button
SCRATCH_HEADER = 34
SCRATCH_DEFAULT = (490, 104, 440, 380)
SCRATCH_PEN = (30, 30, 70)

# The runtime that owns the current question publishes its tools here, so the
# shared Page / present_frame helpers can reach them without extra plumbing.
ACTIVE_TOOLS = None


def get_tools(question):
    """Tools for this question, or None (previews, disabled in settings, no pygame)."""
    if not question.get('_tools_enabled') or question.get('_studio_scene'):
        return None
    tools = question.get('_tools')
    if tools is None:
        try:
            import pygame
        except ImportError:
            return None
        tools = question['_tools'] = ExerciseTools(pygame)
    return tools


def begin(question):
    global ACTIVE_TOOLS
    ACTIVE_TOOLS = get_tools(question)
    return ACTIVE_TOOLS


def end():
    global ACTIVE_TOOLS
    ACTIVE_TOOLS = None


def filter_events(events, scroll):
    """Yield only the events the tools did not consume (for loops using pygame.event.get())."""
    tools = ACTIVE_TOOLS
    for ev in events:
        if tools is not None and tools.handle_event(ev, scroll):
            continue
        yield ev


class _Scaled:
    """pygame.draw proxy: multiplies every coordinate and width by k (for supersampling)."""

    def __init__(self, pg, k):
        self.pg, self.k = pg, k

    def _pt(self, p):
        return (p[0] * self.k, p[1] * self.k)

    def _w(self, w):
        return 0 if not w else max(1, int(round(w * self.k)))

    def line(self, s, c, a, b, w=1):
        self.pg.draw.line(s, c, self._pt(a), self._pt(b), self._w(w) or 1)

    def lines(self, s, c, closed, pts, w=1):
        self.pg.draw.lines(s, c, closed, [self._pt(p) for p in pts], self._w(w) or 1)

    def polygon(self, s, c, pts, w=0):
        self.pg.draw.polygon(s, c, [self._pt(p) for p in pts], self._w(w))

    def circle(self, s, c, center, r, w=0):
        self.pg.draw.circle(s, c, self._pt(center), r * self.k, self._w(w))

    def rect(self, s, c, rect, w=0, radius=0):
        x, y, rw, rh = rect
        k = self.k
        self.pg.draw.rect(s, c, self.pg.Rect(round(x * k), round(y * k), round(rw * k), round(rh * k)),
                          self._w(w), border_radius=int(round(radius * k)))


class ExerciseTools:
    def __init__(self, pygame_module):
        self.pg = pygame_module
        self.store = AnnotationStore()
        self.scratch = AnnotationStore()
        self.tool = 'select'
        self.expanded = False
        self.external_draw = False      # True when the runtime draws the dock itself
        self.screen_space = False       # True when only part of the page scrolls: strokes then stay on screen
        self.colors = dict(DEFAULT_COLORS)
        self.color_open = False
        self.scratch_open = False
        self.scratch_rect = pygame_module.Rect(SCRATCH_DEFAULT)
        self.scratch_tool = 'pen'
        self._drawing = None
        self._erasing = False
        self._editing = None
        self._pressed = None
        self._s_drawing = None
        self._s_erasing = False
        self._s_drag = None
        self._s_pressed = None
        self._font = None
        self._note_font = None
        self._aa = {}                   # stroke id -> cached anti-aliased surface
        self._tiles = {}                # cached anti-aliased dock/panel/icon tiles
        self._chunks = {}               # finished segments of the stroke being drawn
        pg = self.pg
        self.rects = {name: pg.Rect(DOCK_X, DOCK_Y - i * STEP, BTN, BTN) for i, name in enumerate(BUTTONS)}
        self.palette_rects = []

    # ------------------------------------------------------------- helpers
    def _visible_buttons(self):
        return BUTTONS if self.expanded else ('toggle',)

    def _dock_rect(self):
        names = self._visible_buttons()
        r = self.rects[names[0]].unionall([self.rects[n] for n in names])
        return r.inflate(10, 10)

    def _palette_layout(self):
        """Swatches in a row to the right of the colour button."""
        anchor = self.rects['color']
        x = anchor.right + 16
        rects = []
        for color in PALETTE:
            rects.append((self.pg.Rect(x, anchor.y + 3, 30, 30), color))
            x += 34
        return rects

    def _palette_panel(self):
        rects = self._palette_layout()
        return rects[0][0].union(rects[-1][0]).inflate(14, 12)

    def _color_tool(self):
        return self.tool if self.tool in COLORABLE else 'pen'

    def _in_viewport(self, pos):
        return VIEW_TOP <= pos[1] < VIEW_BOTTOM and pos[0] < VIEW_RIGHT

    def _button_at(self, pos):
        for name in self._visible_buttons():
            if self.rects[name].collidepoint(pos):
                return name
        return None

    def _commit_note(self):
        note, self._editing = self._editing, None
        if note is not None and stroke_ok(note):
            note['text'] = note['text'].rstrip()
            self.store.add(note)

    def _finish_stroke(self):
        self._commit_note()
        if self._drawing is not None:
            stroke, self._drawing = self._drawing, None
            if stroke_ok(stroke):
                self.store.add(stroke)
        if self._erasing:
            self.store.end_erase()
            self._erasing = False

    def _set_tool(self, name):
        self._finish_stroke()
        self.tool = 'select' if self.tool == name else name
        self.color_open = False

    def _collapse(self):
        self._finish_stroke()
        self.expanded = False
        self.tool = 'select'
        self.color_open = False

    def _toggle_scratch(self):
        self._finish_scratch()
        self.scratch_open = not self.scratch_open
        self.color_open = False

    def _finish_scratch(self):
        if self._s_drawing is not None:
            self.scratch.add(self._s_drawing)
            self._s_drawing = None
        if self._s_erasing:
            self.scratch.end_erase()
            self._s_erasing = False
        self._s_drag = None
        self._s_pressed = None

    def _press_button(self, name):
        if name == 'toggle':
            if self.expanded:
                self._collapse()
            else:
                self.expanded = True
        elif name in TOOL_BUTTONS:
            self._set_tool(name)
        elif name == 'undo':
            self._finish_stroke()
            self.store.undo()
        elif name == 'redo':
            self._finish_stroke()
            self.store.redo()
        elif name == 'clear':
            self._finish_stroke()
            self.store.clear()
        elif name == 'color':
            self.color_open = not self.color_open
        elif name == 'scratch':
            self._toggle_scratch()

    # ------------------------------------------------------- scratch pad
    def _scratch_body(self):
        r = self.scratch_rect
        return self.pg.Rect(r.x, r.y + SCRATCH_HEADER, r.w, r.h - SCRATCH_HEADER)

    def _scratch_buttons(self):
        r = self.scratch_rect
        pg = self.pg
        out, x = {}, r.x + 8
        for name, w in (('pen', 44), ('eraser', 44), ('undo', 80), ('clear', 50)):
            out[name] = pg.Rect(x, r.y + 5, w, 24)
            x += w + 4
        out['close'] = pg.Rect(r.right - 32, r.y + 5, 24, 24)
        return out

    def _scratch_local(self, pos):
        b = self._scratch_body()
        x = max(b.x, min(b.right, pos[0]))
        y = max(b.y, min(b.bottom, pos[1]))
        return (x - self.scratch_rect.x, y - self.scratch_rect.y)

    def _scratch_event(self, ev):
        """Handle the scratch pad. Returns True when consumed."""
        pg = self.pg
        if ev.type == pg.MOUSEWHEEL:
            return self.scratch_rect.collidepoint(pg.mouse.get_pos())
        if ev.type == pg.MOUSEBUTTONDOWN:
            if not self.scratch_rect.collidepoint(ev.pos):
                return False
            if ev.button != 1:
                return True
            for name, rect in self._scratch_buttons().items():
                if rect.collidepoint(ev.pos):
                    self._s_pressed = name
                    return True
            if ev.pos[1] < self.scratch_rect.y + SCRATCH_HEADER:
                self._s_drag = (ev.pos[0] - self.scratch_rect.x, ev.pos[1] - self.scratch_rect.y)
                return True
            local = self._scratch_local(ev.pos)
            if self.scratch_tool == 'eraser':
                self._s_erasing = True
                self.scratch.begin_erase()
                self.scratch.erase_at(local)
            else:
                stroke = new_stroke('pen', SCRATCH_PEN, local)
                stroke['width'] = 3
                self._s_drawing = stroke
            return True
        if ev.type == pg.MOUSEMOTION:
            if self._s_drag is not None:
                x = max(0, min(WIDTH - self.scratch_rect.w, ev.pos[0] - self._s_drag[0]))
                y = max(0, min(HEIGHT - SCRATCH_HEADER, ev.pos[1] - self._s_drag[1]))
                self.scratch_rect.topleft = (x, y)
                return True
            if self._s_drawing is not None:
                extend_stroke(self._s_drawing, self._scratch_local(ev.pos))
                return True
            if self._s_erasing:
                self.scratch.erase_at(self._scratch_local(ev.pos))
                return True
            return False
        if ev.type == pg.MOUSEBUTTONUP and ev.button == 1:
            busy = self._s_drawing is not None or self._s_erasing or self._s_drag is not None
            pressed, self._s_pressed = self._s_pressed, None
            if busy:
                self._finish_scratch()
                return True
            if pressed is not None:
                if self._scratch_buttons()[pressed].collidepoint(ev.pos):
                    if pressed in ('pen', 'eraser'):
                        self.scratch_tool = pressed
                    elif pressed == 'undo':
                        self.scratch.undo()
                    elif pressed == 'clear':
                        self.scratch.clear()
                    elif pressed == 'close':
                        self._toggle_scratch()
                return True
        return False

    # -------------------------------------------------------------- events
    def handle_event(self, ev, scroll):
        """Return True when the event was consumed (the caller must `continue`)."""
        pg = self.pg
        if self.screen_space:
            scroll = 0
        if self.scratch_open and self._scratch_event(ev):
            return True
        if self._editing is not None:
            if ev.type == pg.TEXTINPUT:
                if len(self._editing['text']) < MAX_TEXT:
                    self._editing['text'] = (self._editing['text'] + ev.text)[:MAX_TEXT]
                return True
            if ev.type == pg.KEYDOWN:
                if ev.key in (pg.K_RETURN, pg.K_KP_ENTER, pg.K_ESCAPE):
                    self._commit_note()
                elif ev.key == pg.K_BACKSPACE:
                    self._editing['text'] = self._editing['text'][:-1]
                return True                              # typing must never reach the answer
        if ev.type == pg.KEYDOWN:
            return self._on_key(ev)
        if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
            return self._on_down(ev.pos, scroll)
        if ev.type == pg.MOUSEMOTION:
            return self._on_move(ev.pos, scroll)
        if ev.type == pg.MOUSEBUTTONUP and ev.button == 1:
            return self._on_up(ev.pos)
        return False

    def _on_key(self, ev):
        pg = self.pg
        mod = ev.mod
        if ev.key == pg.K_ESCAPE:
            if self.color_open or self.tool != 'select' or self._drawing is not None:
                self._finish_stroke()
                self.tool = 'select'
                self.color_open = False
                return True
            if self.scratch_open:
                self._toggle_scratch()
                return True
            return False
        if mod & pg.KMOD_CTRL and ev.key == pg.K_z:
            return self.store.redo() if mod & pg.KMOD_SHIFT else self.store.undo()
        if mod & pg.KMOD_CTRL and ev.key == pg.K_y:
            return self.store.redo()
        if mod & pg.KMOD_ALT and not mod & pg.KMOD_CTRL:
            name = ALT_KEYS.get(pg.key.name(ev.key))
            if name:
                self.expanded = True
                self._set_tool(name)
                return True
            if ev.key == pg.K_n:
                self.expanded = True
                self._toggle_scratch()
                return True
            if ev.key == pg.K_v:
                self._finish_stroke()
                self.tool = 'select'
                self.color_open = False
                return True
        return False

    def _on_down(self, pos, scroll):
        self._commit_note()
        button = self._button_at(pos)
        if button is not None:
            self._pressed = button
            return True
        if self.expanded and self._dock_rect().collidepoint(pos):
            return True                                  # dock padding: do not click through
        if self.color_open:
            if self._palette_panel().collidepoint(pos):
                for rect, color in self._palette_layout():
                    if rect.collidepoint(pos):
                        self.colors[self._color_tool()] = color
                        if self.tool not in COLORABLE:
                            self.tool = 'pen'
                        self.color_open = False
                        break
                return True
            self.color_open = False                       # click elsewhere closes the palette
        if self.tool == 'select' or not self._in_viewport(pos):
            return False
        doc = (pos[0], pos[1] + scroll)
        if self.tool == 'eraser':
            self._erasing = True
            self.store.begin_erase()
            self.store.erase_at(doc)
        elif self.tool == 'text':
            self._editing = new_stroke('text', self.colors['text'], (doc[0], doc[1] - 12))
            try:
                self.pg.key.start_text_input()
            except Exception:
                pass
        else:
            self._drawing = new_stroke(self.tool, self.colors[self.tool], doc)
        return True

    def _on_move(self, pos, scroll):
        if self._drawing is not None:
            extend_stroke(self._drawing, (pos[0], max(VIEW_TOP, min(VIEW_BOTTOM, pos[1])) + scroll))
            return True
        if self._erasing:
            self.store.erase_at((pos[0], pos[1] + scroll))
            return True
        return False

    def _on_up(self, pos):
        if self._drawing is not None or self._erasing:
            self._finish_stroke()
            return True
        if self._pressed is not None:
            pressed, self._pressed = self._pressed, None
            if self._button_at(pos) == pressed:
                self._press_button(pressed)
            return True
        return False

    # ------------------------------------------------------------- drawing
    # Why everything goes through _aa_*: the exercise window is SCALED and usually
    # maximised, so the 960x640 logical surface is stretched to the screen. pygame.draw
    # has no anti-aliasing for wide lines, circles or rounded rects; stretched, those hard
    # stair-steps turn into blur and broken edges. Shapes are therefore drawn AA times
    # larger and averaged down (smoothscale), which gives real anti-aliased edges.
    def _fonts(self):
        if self._font is None:
            try:
                from tuhoc.exercises.pygame_window_utils import vietnamese_font
                self._font = vietnamese_font(self.pg, 14)
                self._note_font = vietnamese_font(self.pg, 20)
            except Exception:
                self._font = self.pg.font.Font(None, 16)
                self._note_font = self.pg.font.Font(None, 22)

    def _aa_alpha(self, size, color, draw_fn):
        """Single-colour shape on a transparent surface, anti-aliased.

        The big surface is pre-filled with the shape colour at alpha 0, so smoothscale
        cannot bleed black into the edge pixels.
        """
        pg = self.pg
        w, h = max(1, int(size[0])), max(1, int(size[1]))
        big = pg.Surface((w * AA, h * AA), pg.SRCALPHA)
        big.fill((*color[:3], 0))
        draw_fn(_Scaled(pg, AA), big)
        return pg.transform.smoothscale(big, (w, h))

    def _aa_opaque(self, size, bg, draw_fn, key):
        """Opaque anti-aliased tile (icons, palette, tooltips). Cached by `key`."""
        pg = self.pg
        cached = self._tiles.get(key)
        if cached is not None:
            return cached
        w, h = int(size[0]), int(size[1])
        big = pg.Surface((w * AA, h * AA))
        big.fill(bg)
        draw_fn(_Scaled(pg, AA), big)
        tile = pg.transform.smoothscale(big, (w, h))
        if len(self._tiles) > 400:
            self._tiles.clear()
        self._tiles[key] = tile
        return tile

    def _stroke_surface(self, stroke, live=False, cache=True):
        """(surface, ox, oy): the stroke rendered anti-aliased, positioned in its own coords."""
        pg = self.pg
        blink = (pg.time.get_ticks() // 500) % 2 if stroke is self._editing else -1
        pts = stroke['pts']
        # rect/strike are re-shaped as a whole while dragging (a closed rect always ends on its
        # first corner), so their cache key must hold every point; pen strokes only grow at the end.
        shape = tuple(pts) if stroke['tool'] in ('rect', 'strike') else (len(pts), pts[-1])
        sig = (shape, stroke['color'], stroke.get('text'), live, blink)
        hit = self._aa.get(id(stroke)) if cache else None
        if hit is not None and hit[0] == sig:
            return hit[1], hit[2], hit[3]
        tool = stroke['tool']
        w = stroke['width']
        if tool == 'text':
            surf, ox, oy = self._note_surface(stroke)
        else:
            pts = stroke['pts']
            if tool in ('pen', 'highlight') and len(pts) > 2:
                pts = smooth_points(pts, 1 if live and len(pts) > 300 else 2)
            pad = w / 2.0 + 2
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            ox, oy = int(math.floor(min(xs) - pad)), int(math.floor(min(ys) - pad))
            sw, sh = int(math.ceil(max(xs) + pad)) - ox, int(math.ceil(max(ys) + pad)) - oy
            local = [(x - ox, y - oy) for x, y in pts]

            def shape(d, big, local=local, w=w, tool=tool):
                color = big.get_at((0, 0))[:3]
                r = w / 2.0
                if tool == 'rect':
                    if len(local) >= 5:
                        for a, b in zip(local[:4], local[1:5]):
                            d.line(big, color, a, b, w)
                        for p in local[:4]:
                            d.circle(big, color, p, r)       # round joins: no notched corners
                    return
                step = 1 if len(local) < 2500 else 2
                for a, b in zip(local[::step], local[step::step]):
                    d.line(big, color, a, b, w)
                for p in local[::step]:
                    d.circle(big, color, p, r)
                d.circle(big, color, local[-1], r)

            surf = self._aa_alpha((sw, sh), stroke['color'], shape)
            if tool == 'highlight':
                surf.set_alpha(HIGHLIGHT_ALPHA)
            elif tool == 'strike':
                surf.set_alpha(215)
        if cache:
            if len(self._aa) > 600:
                self._aa.clear()
            self._aa[id(stroke)] = (sig, surf, ox, oy)
        return surf, ox, oy

    def _note_surface(self, stroke):
        """Sticky-note box (anti-aliased fill + border) with crisp text on top."""
        pg = self.pg
        text = stroke.get('text', '')
        editing = stroke is self._editing
        label = self._note_font.render(text or ' ', True, stroke['color'])
        bw, bh = label.get_width() + 12 + (2 if editing else 0), label.get_height() + 6
        stroke['box'] = (bw, bh)
        radius = 6

        def fill(d, big):
            d.rect(big, big.get_at((0, 0))[:3], (0, 0, bw, bh), 0, radius)

        def edge(d, big):
            d.rect(big, big.get_at((0, 0))[:3], (0.5, 0.5, bw - 1, bh - 1), 1.4, radius)

        out = pg.Surface((bw, bh), pg.SRCALPHA)
        body = self._aa_alpha((bw, bh), (255, 253, 225), fill)
        body.set_alpha(238)
        out.blit(body, (0, 0))
        out.blit(self._aa_alpha((bw, bh), stroke['color'], edge), (0, 0))
        out.blit(label, (6, 3))
        if editing and (pg.time.get_ticks() // 500) % 2 == 0:
            x = 6 + label.get_width() + 1 if text else 6
            pg.draw.line(out, stroke['color'], (x, 5), (x, bh - 5), 2)
        x, y = stroke['pts'][0]
        return out, int(round(x)), int(round(y))

    def draw(self, surface, scroll):
        pg = self.pg
        self._fonts()
        self._draw_strokes(surface, 0 if self.screen_space else scroll)
        mouse = pg.mouse.get_pos()
        self._draw_cursor(surface, mouse)
        if self.scratch_open:
            self._draw_scratch(surface, mouse)
        self._draw_dock(surface, mouse)

    def _live_parts(self, stroke):
        """Surfaces for a long pen stroke being drawn: cached finished chunks + a small live tail."""
        pts = stroke['pts']
        parts, i = [], 0
        while i + LIVE_CHUNK < len(pts):
            entry = self._chunks.get((id(stroke), i))
            if entry is None:
                part = dict(stroke, pts=pts[i:i + LIVE_CHUNK])
                entry = self._chunks[(id(stroke), i)] = (part,) + self._stroke_surface(part, False, cache=False)
            parts.append(entry[1:])
            i += LIVE_CHUNK - 1                    # chunks share one point so the line stays joined
        parts.append(self._stroke_surface(dict(stroke, pts=pts[i:]), True, cache=False))
        return parts

    def _draw_strokes(self, surface, scroll):
        pg = self.pg
        strokes = list(self.store.items)
        if self._drawing is not None:
            strokes.append(self._drawing)
        if self._editing is not None:
            strokes.append(self._editing)
        if self._drawing is None and self._chunks:
            self._chunks.clear()
        if len(self._aa) > len(strokes) + 80:                 # drop cache entries of erased strokes
            alive = {id(s) for s in strokes}
            self._aa = {k: v for k, v in self._aa.items() if k in alive}
        if not strokes:
            return
        clip = surface.get_clip()
        surface.set_clip(pg.Rect(0, VIEW_TOP, VIEW_RIGHT, VIEW_BOTTOM - VIEW_TOP))
        # Highlighter first so ink and notes are never hidden beneath it.
        for stroke in sorted(strokes, key=lambda s: s['tool'] != 'highlight'):
            live = stroke is self._drawing
            if live and stroke['tool'] == 'pen' and len(stroke['pts']) > LIVE_CHUNK:
                parts = self._live_parts(stroke)
            else:
                parts = [self._stroke_surface(stroke, live)]
            for surf, ox, oy in parts:
                y = oy - scroll
                if y + surf.get_height() < VIEW_TOP or y > VIEW_BOTTOM:
                    continue
                surface.blit(surf, (ox, y))
        surface.set_clip(clip)

    def _over_chrome(self, mouse):
        if self.expanded and self._dock_rect().collidepoint(mouse):
            return True
        if self.color_open and self._palette_panel().collidepoint(mouse):
            return True
        return self.scratch_open and self.scratch_rect.collidepoint(mouse)

    def _draw_cursor(self, surface, mouse):
        pg = self.pg
        if self.tool == 'select' or not self._in_viewport(mouse) or self._over_chrome(mouse):
            return
        if self.tool == 'eraser':
            radius, color, thick = ERASER_RADIUS, (60, 70, 90), 2
        elif self.tool == 'text':
            pg.draw.line(surface, self.colors['text'], (mouse[0], mouse[1] - 10), (mouse[0], mouse[1] + 10), 2)
            return
        elif self.tool in ('rect', 'strike'):
            pg.draw.line(surface, self.colors[self.tool], (mouse[0] - 8, mouse[1]), (mouse[0] + 8, mouse[1]), 2)
            pg.draw.line(surface, self.colors[self.tool], (mouse[0], mouse[1] - 8), (mouse[0], mouse[1] + 8), 2)
            return
        else:
            radius, color, thick = max(3, WIDTHS[self.tool] // 2 + 1), self.colors[self.tool], 2
        key = ('cursor', radius, color, thick)
        size = radius * 2 + 4

        def ring(d, big):
            d.circle(big, color, (size / 2.0, size / 2.0), radius, thick)

        tile = self._aa_alpha((size, size), color, ring) if key not in self._tiles else self._tiles[key]
        self._tiles[key] = tile
        surface.blit(tile, (mouse[0] - size // 2, mouse[1] - size // 2))

    def _panel_tile(self, size, fill, edge, radius):
        key = ('panel', size, fill, edge, radius)
        tile = self._tiles.get(key)
        if tile is None:
            w, h = size
            out = self.pg.Surface((w, h), self.pg.SRCALPHA)
            out.blit(self._aa_alpha(size, fill, lambda d, big: d.rect(big, fill, (0, 0, w, h), 0, radius)), (0, 0))
            out.blit(self._aa_alpha(size, edge, lambda d, big: d.rect(
                big, edge, (0.5, 0.5, w - 1, h - 1), 1.4, radius)), (0, 0))
            tile = self._tiles[key] = out
        return tile

    def _draw_scratch(self, surface, mouse):
        pg = self.pg
        r = self.scratch_rect
        shadow = self._tiles.get(('shadow', r.size))
        if shadow is None:
            shadow = self._aa_alpha((r.w + 12, r.h + 12), (0, 0, 0),
                                    lambda d, big: d.rect(big, (0, 0, 0), (0, 0, r.w + 12, r.h + 12), 0, 16))
            shadow.set_alpha(55)
            self._tiles[('shadow', r.size)] = shadow
        surface.blit(shadow, (r.x - 4, r.y - 2))
        surface.blit(self._panel_tile(r.size, (252, 250, 240), PANEL_EDGE, 12), r.topleft)
        body = self._scratch_body()
        for y in range(body.y + 28, body.bottom - 4, 28):
            pg.draw.line(surface, (226, 232, 240), (body.x + 10, y), (body.right - 10, y), 1)
        clip = surface.get_clip()
        surface.set_clip(body)
        strokes = list(self.scratch.items) + ([self._s_drawing] if self._s_drawing is not None else [])
        for stroke in strokes:
            surf, ox, oy = self._stroke_surface(stroke, stroke is self._s_drawing)
            surface.blit(surf, (r.x + ox, r.y + oy))
        surface.set_clip(clip)
        header = self._panel_tile(r.size, PANEL, PANEL_EDGE, 12)
        surface.blit(header, r.topleft, (0, 0, r.w, SCRATCH_HEADER))
        labels = {'pen': 'Bút', 'eraser': 'Tẩy', 'undo': 'Hoàn tác', 'clear': 'Xóa', 'close': '×'}
        for name, rect in self._scratch_buttons().items():
            on = name == self.scratch_tool
            hot = rect.collidepoint(mouse)
            if on or hot:
                fill = ACTIVE if on else HOVER
                surface.blit(self._panel_tile(rect.size, fill, fill, 7), rect.topleft)
            text = self._font.render(labels[name], True, INK)
            surface.blit(text, text.get_rect(center=rect.center))
        title = self._font.render('Giấy nháp', True, (190, 205, 228))
        surface.blit(title, title.get_rect(midleft=(r.x + 270, r.y + SCRATCH_HEADER // 2)))

    def _draw_dock(self, surface, mouse):
        pg = self.pg
        dock = self._dock_rect()
        surface.blit(self._panel_tile(dock.size, PANEL, PANEL_EDGE, 14), dock.topleft)
        hovered = None
        for name in self._visible_buttons():
            rect = self.rects[name]
            is_hover = rect.collidepoint(mouse)
            active = name == self.tool or (name == 'color' and self.color_open) or (name == 'scratch' and self.scratch_open)
            if name == 'toggle' and not self.expanded:
                active = bool(self.store.items or self.scratch.items)
            enabled = not ((name == 'undo' and not self.store.can_undo)
                           or (name == 'redo' and not self.store.can_redo)
                           or (name == 'clear' and not self.store.items))
            bg = ACTIVE if active else HOVER if (is_hover and enabled) else None
            fg = INK if enabled else DIM
            state = (self.colors['pen'], self.colors['highlight'], self.colors['rect'],
                     self.colors[self._color_tool()], self.expanded) if name in (
                         'toggle', 'pen', 'highlight', 'rect', 'color') else ()
            key = ('icon', name, bg, fg, state)
            surface.blit(self._aa_opaque((BTN, BTN), PANEL, lambda d, big, name=name, bg=bg, fg=fg: (
                bg is not None and d.rect(big, bg, (0, 0, BTN, BTN), 0, 10),
                self._icon(big, name, pg.Rect(0, 0, BTN, BTN), fg, d)), key), rect.topleft)
            if is_hover:
                hovered = name
        if self.color_open:
            panel = self._palette_panel()
            current = self.colors[self._color_tool()]
            layout = self._palette_layout()

            def swatches(d, big):
                for rect, color in layout:
                    c = (rect.centerx - panel.x, rect.centery - panel.y)
                    d.circle(big, color, c, 11)
                    if color == current:
                        d.circle(big, INK, c, 14, 2)

            surface.blit(self._panel_tile(panel.size, PANEL, PANEL_EDGE, 12), panel.topleft)
            surface.blit(self._aa_alpha(panel.size, PANEL, swatches), panel.topleft)
        elif hovered is not None:
            label = self._font.render(TIPS[hovered], True, (33, 52, 79))
            box = label.get_rect(midleft=(self.rects[hovered].right + 18, self.rects[hovered].centery)).inflate(14, 8)
            surface.blit(self._panel_tile(box.size, (255, 255, 255), PANEL_EDGE, 7), box.topleft)
            surface.blit(label, label.get_rect(center=box.center))

    def _icon(self, s, name, r, c, d):
        """Icon drawn through the scaled-draw proxy `d` (coordinates are 1x units)."""
        cx, cy = r.center
        if name == 'toggle':
            if self.expanded:       # chevron: collapse
                d.lines(s, c, False, [(cx + 4, cy - 8), (cx - 4, cy), (cx + 4, cy + 8)], 3)
            else:                   # pencil
                d.polygon(s, c, [(cx - 9, cy + 9), (cx - 9, cy + 3), (cx + 3, cy - 9),
                                 (cx + 9, cy - 3), (cx - 3, cy + 9)])
        elif name == 'pen':
            d.line(s, c, (cx - 8, cy + 8), (cx + 7, cy - 7), 4)
            d.circle(s, self.colors['pen'], (cx - 8, cy + 8), 3)
        elif name == 'highlight':
            d.polygon(s, c, [(cx - 8, cy + 2), (cx + 2, cy - 8), (cx + 8, cy - 2), (cx - 2, cy + 8)])
            d.rect(s, self.colors['highlight'], (cx - 9, cy + 8, 18, 4))
        elif name == 'rect':
            d.rect(s, self.colors['rect'], (cx - 10, cy - 7, 20, 14), 3, 2)
        elif name == 'text':
            d.line(s, c, (cx - 8, cy - 8), (cx + 8, cy - 8), 3)
            d.line(s, c, (cx, cy - 8), (cx, cy + 9), 3)
        elif name == 'strike':
            faint = DIM if c == DIM else (150, 160, 180)
            d.line(s, faint, (cx - 9, cy - 6), (cx + 9, cy - 6), 2)
            d.line(s, c, (cx - 10, cy + 1), (cx + 10, cy + 1), 3)
            d.line(s, faint, (cx - 9, cy + 8), (cx + 9, cy + 8), 2)
        elif name == 'eraser':
            d.polygon(s, c, [(cx - 9, cy + 3), (cx - 1, cy - 8), (cx + 9, cy - 1), (cx + 1, cy + 8)], 2)
            d.line(s, c, (cx - 5, cy - 2), (cx + 5, cy + 5), 2)
        elif name in ('undo', 'redo'):
            k = -1 if name == 'undo' else 1          # arrow points left for undo, right for redo
            d.lines(s, c, False, [(cx - 6 * k, cy + 7), (cx - 6 * k, cy - 2), (cx + 3 * k, cy - 2)], 3)
            d.polygon(s, c, [(cx + 9 * k, cy - 2), (cx + 3 * k, cy - 8), (cx + 3 * k, cy + 4)])
        elif name == 'clear':
            d.lines(s, c, False, [(cx - 7, cy - 7), (cx + 7, cy + 7)], 3)
            d.lines(s, c, False, [(cx + 7, cy - 7), (cx - 7, cy + 7)], 3)
        elif name == 'color':
            d.circle(s, self.colors[self._color_tool()], (cx, cy), 9)
            d.circle(s, c, (cx, cy), 10, 2)
        elif name == 'scratch':
            d.rect(s, c, (cx - 8, cy - 9, 16, 18), 2, 2)
            d.line(s, c, (cx - 4, cy - 3), (cx + 4, cy - 3), 2)
            d.line(s, c, (cx - 4, cy + 3), (cx + 2, cy + 3), 2)
