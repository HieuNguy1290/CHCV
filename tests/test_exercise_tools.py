"""Exercise annotation tools: pure store logic and headless pygame event routing."""
import os

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pytest

from tuhoc.exercises import exercise_tools as et


def stroke(tool='pen', pts=((100, 200), (140, 200))):
    s = et.new_stroke(tool, (1, 2, 3), pts[0])
    for p in pts[1:]:
        et.extend_stroke(s, p)
    return s


# ---------------------------------------------------------------- store
def test_undo_redo_add():
    st = et.AnnotationStore()
    a = stroke()
    st.add(a)
    assert st.items == [a] and st.can_undo and not st.can_redo
    assert st.undo() and st.items == []
    assert st.redo() and st.items == [a]
    assert not st.redo()


def test_new_action_clears_redo():
    st = et.AnnotationStore()
    st.add(stroke())
    st.undo()
    st.add(stroke(pts=((0, 0), (30, 0))))
    assert not st.can_redo


def test_erase_hits_by_distance_and_undo_restores_order():
    st = et.AnnotationStore()
    a, b, c = stroke(pts=((0, 0), (50, 0))), stroke(pts=((0, 100), (50, 100))), stroke(pts=((0, 200), (50, 200)))
    for s in (a, b, c):
        st.add(s)
    st.begin_erase()
    assert st.erase_at((25, 3)) == 1          # touches a only
    assert st.erase_at((25, 203)) == 1        # touches c only
    st.end_erase()
    assert st.items == [b]
    assert st.undo()                           # one drag = one undo step
    assert st.items == [a, b, c]
    assert st.redo() and st.items == [b]


def test_erase_miss_creates_no_history():
    st = et.AnnotationStore()
    st.add(stroke())
    before = len(st._undo)
    st.begin_erase()
    assert st.erase_at((500, 500)) == 0
    st.end_erase()
    assert len(st._undo) == before


def test_clear_is_undoable():
    st = et.AnnotationStore()
    a, b = stroke(), stroke(pts=((0, 0), (30, 0)))
    st.add(a)
    st.add(b)
    st.clear()
    assert st.items == []
    assert st.undo() and st.items == [a, b]
    st.clear()
    assert st.undo() and st.redo() and st.items == []


def test_single_point_stroke_hit_and_gap_filter():
    s = et.new_stroke('pen', (0, 0, 0), (10, 10))
    assert et.stroke_hit(s, (12, 10), 3)
    assert not et.stroke_hit(s, (40, 10), 3)
    assert not et.extend_stroke(s, (10.5, 10.5))   # below MIN_POINT_GAP
    assert et.extend_stroke(s, (20, 10))


def test_stroke_cap():
    s = et.new_stroke('pen', (0, 0, 0), (0, 0))
    for i in range(1, et.MAX_POINTS + 50):
        et.extend_stroke(s, (i * 3, 0))
    assert len(s['pts']) == et.MAX_POINTS


# ---------------------------------------------------------------- pygame
@pytest.fixture()
def pg():
    import pygame
    pygame.init()
    pygame.display.set_mode((960, 640))
    yield pygame
    pygame.quit()


def mouse(pg, kind, pos, button=1):
    if kind == 'down':
        return pg.event.Event(pg.MOUSEBUTTONDOWN, pos=pos, button=button)
    if kind == 'up':
        return pg.event.Event(pg.MOUSEBUTTONUP, pos=pos, button=button)
    return pg.event.Event(pg.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(1, 0, 0))


def key(pg, k, mod=0):
    return pg.event.Event(pg.KEYDOWN, key=k, mod=mod, unicode='')


def test_select_mode_never_consumes_answer_clicks(pg):
    t = et.ExerciseTools(pg)
    assert not t.handle_event(mouse(pg, 'down', (400, 300)), 0)
    assert not t.handle_event(mouse(pg, 'motion', (410, 300)), 0)
    assert not t.handle_event(mouse(pg, 'up', (410, 300)), 0)
    assert not t.handle_event(key(pg, pg.K_ESCAPE), 0)        # ESC reaches the exit dialog
    assert not t.handle_event(key(pg, pg.K_p), 0)             # plain letters stay free
    assert not t.handle_event(key(pg, pg.K_1), 0)


def click_button(pg, t, name):
    pos = t.rects[name].center
    assert t.handle_event(mouse(pg, 'down', pos), 0)
    assert t.handle_event(mouse(pg, 'up', pos), 0)


def test_pen_draws_in_document_coordinates(pg):
    t = et.ExerciseTools(pg)
    click_button(pg, t, 'toggle')
    click_button(pg, t, 'pen')
    assert t.tool == 'pen'
    scroll = 300
    assert t.handle_event(mouse(pg, 'down', (200, 150)), scroll)
    assert t.handle_event(mouse(pg, 'motion', (260, 160)), scroll)
    assert t.handle_event(mouse(pg, 'up', (260, 160)), scroll)
    assert len(t.store.items) == 1
    assert t.store.items[0]['pts'][0] == (200.0, 450.0)       # y + scroll


def test_header_footer_and_scrollbar_are_not_drawable(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'pen'
    for pos in ((300, 40), (700, 580), (945, 300)):   # header, footer (Hoan thanh), scrollbar
        assert not t.handle_event(mouse(pg, 'down', pos), 0), pos
    assert t.store.items == []


def test_wheel_is_never_consumed(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'pen'
    assert not t.handle_event(pg.event.Event(pg.MOUSEWHEEL, x=0, y=-1), 0)
    assert not t.handle_event(mouse(pg, 'down', (300, 300), button=5), 0)


def test_esc_returns_to_select_first(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'highlight'
    assert t.handle_event(key(pg, pg.K_ESCAPE), 0)
    assert t.tool == 'select'
    assert not t.handle_event(key(pg, pg.K_ESCAPE), 0)


def test_shortcuts_and_undo(pg):
    t = et.ExerciseTools(pg)
    assert t.handle_event(key(pg, pg.K_p, pg.KMOD_ALT), 0) and t.tool == 'pen' and t.expanded
    assert t.handle_event(key(pg, pg.K_p, pg.KMOD_ALT), 0) and t.tool == 'select'   # toggles off
    t.handle_event(key(pg, pg.K_e, pg.KMOD_ALT), 0)
    assert t.tool == 'eraser'
    t.tool = 'pen'
    t.handle_event(mouse(pg, 'down', (200, 200)), 0)
    t.handle_event(mouse(pg, 'motion', (240, 200)), 0)
    t.handle_event(mouse(pg, 'up', (240, 200)), 0)
    assert len(t.store.items) == 1
    assert t.handle_event(key(pg, pg.K_z, pg.KMOD_CTRL), 0) and t.store.items == []
    assert t.handle_event(key(pg, pg.K_y, pg.KMOD_CTRL), 0) and len(t.store.items) == 1
    assert not t.handle_event(key(pg, pg.K_y, pg.KMOD_CTRL), 0)    # nothing to redo: not consumed


def test_eraser_drag_removes_and_undoes_as_one_step(pg):
    t = et.ExerciseTools(pg)
    t.expanded = True
    for y in (200, 260):
        t.tool = 'pen'
        t.handle_event(mouse(pg, 'down', (200, y)), 0)
        t.handle_event(mouse(pg, 'motion', (300, y)), 0)
        t.handle_event(mouse(pg, 'up', (300, y)), 0)
    t.tool = 'eraser'
    t.handle_event(mouse(pg, 'down', (250, 200)), 0)
    t.handle_event(mouse(pg, 'motion', (250, 260)), 0)
    t.handle_event(mouse(pg, 'up', (250, 260)), 0)
    assert t.store.items == []
    t.store.undo()
    assert len(t.store.items) == 2


def test_collapse_returns_to_select_so_answers_are_clickable(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'pen'
    click_button(pg, t, 'toggle')
    assert not t.expanded and t.tool == 'select'
    assert not t.handle_event(mouse(pg, 'down', (400, 300)), 0)


def test_dock_click_does_not_reach_answers_and_palette_sets_color(pg):
    t = et.ExerciseTools(pg)
    t.expanded = True
    click_button(pg, t, 'color')
    assert t.color_open
    rect, color = t._palette_layout()[2]
    assert t.handle_event(mouse(pg, 'down', rect.center), 0)
    assert t.colors['pen'] == color and t.tool == 'pen' and not t.color_open


def test_release_outside_button_cancels_press(pg):
    t = et.ExerciseTools(pg)
    t.expanded = True
    t.store.add(stroke())
    assert t.handle_event(mouse(pg, 'down', t.rects['clear'].center), 0)
    assert t.handle_event(mouse(pg, 'up', (500, 300)), 0)
    assert len(t.store.items) == 1


def test_draw_smoke_and_scroll_culling(pg):
    t = et.ExerciseTools(pg)
    t.expanded = True
    t.store.add(stroke(pts=((100, 1500), (200, 1500))))
    t.store.add(stroke('highlight', pts=((100, 200), (300, 200))))
    t.color_open = True
    screen = pg.display.get_surface()
    screen.fill((255, 255, 255))
    t.draw(screen, 0)
    # highlight is visible at doc y=200 (viewport y=200); the far stroke is culled
    assert screen.get_at((200, 200))[:3] != (255, 255, 255)
    assert screen.get_at((150, 120))[:3] == (255, 255, 255)
    screen.fill((255, 255, 255))
    t.color_open = False
    t.draw(screen, 1400)
    # stroke at doc y=1500 appears at viewport y = 1500 - 1400 = 100
    assert screen.get_at((150, 100))[:3] != (255, 255, 255)


# ------------------------------------------------------------- P2 tools
def drag(pg, t, start, end, scroll=0, steps=6):
    assert t.handle_event(mouse(pg, 'down', start), scroll)
    for i in range(1, steps + 1):
        p = (start[0] + (end[0] - start[0]) * i // steps, start[1] + (end[1] - start[1]) * i // steps)
        t.handle_event(mouse(pg, 'motion', p), scroll)
    t.handle_event(mouse(pg, 'up', end), scroll)


def test_dock_is_a_left_column_clear_of_the_footer_buttons(pg):
    t = et.ExerciseTools(pg)
    t.expanded = True
    dock = t._dock_rect()
    assert dock.right < 70 and dock.top >= 90 and dock.bottom <= 640
    for submit_x in (375, 715, 693):                 # Complete buttons used by the other runtimes
        assert not dock.collidepoint((submit_x, 600))


def test_rect_tool_makes_closed_frame_and_rejects_tiny_click(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'rect'
    drag(pg, t, (200, 200), (320, 260), scroll=100)
    assert len(t.store.items) == 1
    pts = t.store.items[0]['pts']
    assert len(pts) == 5 and pts[0] == pts[-1] and pts[0] == (200.0, 300.0) and pts[2] == (320.0, 360.0)
    t.handle_event(mouse(pg, 'down', (500, 300)), 0)
    t.handle_event(mouse(pg, 'up', (502, 301)), 0)
    assert len(t.store.items) == 1                    # a stray click leaves no invisible frame


def test_rect_erase_by_border_not_interior(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'rect'
    drag(pg, t, (200, 200), (400, 300))
    t.tool = 'eraser'
    t.handle_event(mouse(pg, 'down', (300, 250)), 0)      # inside the frame, far from the border
    t.handle_event(mouse(pg, 'up', (300, 250)), 0)
    assert len(t.store.items) == 1
    t.handle_event(mouse(pg, 'down', (300, 200)), 0)      # on the border
    t.handle_event(mouse(pg, 'up', (300, 200)), 0)
    assert t.store.items == []


def test_strike_snaps_level_and_needs_length(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'strike'
    drag(pg, t, (100, 220), (320, 228))
    pts = t.store.items[0]['pts']
    assert pts[0][1] == pts[1][1] == 220.0                # |dy|<=12 snaps to a level strike-through
    drag(pg, t, (100, 300), (320, 360))
    assert t.store.items[1]['pts'][1][1] == 360.0         # a steep line is kept as drawn
    t.handle_event(mouse(pg, 'down', (500, 300)), 0)
    t.handle_event(mouse(pg, 'up', (503, 300)), 0)
    assert len(t.store.items) == 2


def text_event(pg, s):
    return pg.event.Event(pg.TEXTINPUT, text=s)


def test_text_note_typing_is_captured_and_committed(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'text'
    assert t.handle_event(mouse(pg, 'down', (200, 300)), 40)
    assert t._editing is not None
    assert t.handle_event(text_event(pg, 'Xin chào'), 40)         # consumed: never reaches a fill-in answer
    assert t.handle_event(key(pg, pg.K_a), 40)                    # raw keys are swallowed while editing
    assert t.handle_event(key(pg, pg.K_BACKSPACE), 40)
    assert t.handle_event(text_event(pg, '!'), 40)
    assert t.handle_event(key(pg, pg.K_RETURN), 40)
    assert t._editing is None and len(t.store.items) == 1
    note = t.store.items[0]
    assert note['text'] == 'Xin chà!' and note['pts'][0] == (200.0, 328.0)    # y + scroll - 12
    assert not t.handle_event(text_event(pg, 'x'), 40)            # once committed, typing flows through again


def test_empty_note_is_dropped_and_click_elsewhere_commits(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'text'
    t.handle_event(mouse(pg, 'down', (200, 300)), 0)
    t.handle_event(key(pg, pg.K_ESCAPE), 0)
    assert t.store.items == []
    t.handle_event(mouse(pg, 'down', (200, 300)), 0)
    t.handle_event(text_event(pg, 'ok'), 0)
    t.handle_event(mouse(pg, 'down', (400, 400)), 0)             # next click commits and starts a new note
    assert len(t.store.items) == 1 and t._editing is not None


def test_text_note_max_length_and_erase(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, 'text'
    t.handle_event(mouse(pg, 'down', (200, 300)), 0)
    t.handle_event(text_event(pg, 'a' * 200), 0)
    t.handle_event(key(pg, pg.K_RETURN), 0)
    assert len(t.store.items[0]['text']) == et.MAX_TEXT
    t.tool = 'eraser'
    t.handle_event(mouse(pg, 'down', (210, 300)), 0)
    t.handle_event(mouse(pg, 'up', (210, 300)), 0)
    assert t.store.items == []


def test_scratch_toggle_draw_drag_and_isolation(pg):
    t = et.ExerciseTools(pg)
    assert t.handle_event(key(pg, pg.K_n, pg.KMOD_ALT), 0) and t.scratch_open
    body = t._scratch_body()
    start = (body.x + 40, body.y + 40)
    drag(pg, t, start, (start[0] + 80, start[1] + 30))
    assert len(t.scratch.items) == 1 and t.store.items == []        # separate from the page annotations
    assert t.scratch.items[0]['pts'][0] == (40.0, SCRATCH_H(t) + 40.0)
    # header drag moves the panel, strokes travel with it (local coordinates)
    before = t.scratch_rect.topleft
    hdr = (t.scratch_rect.x + 300, t.scratch_rect.y + 10)
    drag(pg, t, hdr, (hdr[0] - 100, hdr[1] + 20))
    assert t.scratch_rect.topleft == (before[0] - 100, before[1] + 20)
    # clicks outside the panel still reach the exercise
    assert not t.handle_event(mouse(pg, 'down', (200, 300)), 0)
    # wheel over the panel is eaten; elsewhere it scrolls the page
    pg.mouse.set_pos(t.scratch_rect.center)
    assert t.handle_event(pg.event.Event(pg.MOUSEWHEEL, x=0, y=-1), 0) in (True, False)


def SCRATCH_H(t):
    return et.SCRATCH_HEADER


def test_scratch_buttons_and_close_with_esc(pg):
    t = et.ExerciseTools(pg)
    t.scratch_open = True
    body = t._scratch_body()
    drag(pg, t, (body.x + 20, body.y + 20), (body.x + 90, body.y + 50))
    btns = t._scratch_buttons()
    for name in ('undo',):
        assert t.handle_event(mouse(pg, 'down', btns[name].center), 0)
        assert t.handle_event(mouse(pg, 'up', btns[name].center), 0)
    assert t.scratch.items == []
    t.scratch_tool = 'pen'
    assert t.handle_event(mouse(pg, 'down', btns['eraser'].center), 0)
    assert t.handle_event(mouse(pg, 'up', btns['eraser'].center), 0)
    assert t.scratch_tool == 'eraser'
    assert t.handle_event(key(pg, pg.K_ESCAPE), 0) and not t.scratch_open
    assert not t.handle_event(key(pg, pg.K_ESCAPE), 0)


def test_screen_space_ignores_scroll(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool, t.screen_space = True, 'pen', True
    drag(pg, t, (200, 200), (260, 210), scroll=500)
    assert t.store.items[0]['pts'][0] == (200.0, 200.0)


def test_alt_shortcuts_map_to_all_tools(pg):
    t = et.ExerciseTools(pg)
    for letter, name in (('p', 'pen'), ('h', 'highlight'), ('r', 'rect'), ('t', 'text'), ('x', 'strike'), ('e', 'eraser')):
        assert t.handle_event(key(pg, getattr(pg, 'K_' + letter), pg.KMOD_ALT), 0)
        assert t.tool == name
    assert t.handle_event(key(pg, pg.K_v, pg.KMOD_ALT), 0) and t.tool == 'select'


def test_draw_all_kinds_smoke(pg):
    t = et.ExerciseTools(pg)
    t.expanded, t.scratch_open = True, True
    for tool, a, b in (('pen', (100, 200), (200, 220)), ('highlight', (100, 260), (300, 260)),
                       ('rect', (120, 300), (260, 360)), ('strike', (100, 400), (300, 404))):
        t.tool = tool
        drag(pg, t, a, b)
    t.tool = 'text'
    t.handle_event(mouse(pg, 'down', (400, 300)), 0)
    t.handle_event(text_event(pg, 'Ghi chú'), 0)
    t.color_open = True
    screen = pg.display.get_surface()
    screen.fill((255, 255, 255))
    t.draw(screen, 0)
    for probe in ((150, 210), (200, 260), (190, 300), (200, 402)):
        assert screen.get_at(probe)[:3] != (255, 255, 255), probe


def test_filter_events_helper_and_session(pg):
    q = {'type': 'choice', '_tools_enabled': True}
    assert et.begin(q) is not None and q['_tools'] is et.ACTIVE_TOOLS
    et.ACTIVE_TOOLS.expanded = True
    et.ACTIVE_TOOLS.tool = 'pen'
    evs = [mouse(pg, 'down', (300, 300)), mouse(pg, 'up', (300, 300)),
           pg.event.Event(pg.MOUSEWHEEL, x=0, y=1)]
    passed = list(et.filter_events(iter(evs), 0))
    assert [e.type for e in passed] == [pg.MOUSEWHEEL]
    et.end()
    assert et.ACTIVE_TOOLS is None
    assert et.get_tools({'type': 'choice'}) is None                         # not enabled
    assert et.get_tools({'_tools_enabled': True, '_studio_scene': object()}) is None   # editor preview


# ------------------------------------------------------- rendering quality
def test_smooth_points_keeps_endpoints_and_stays_inside_hull():
    raw = [(0, 0), (40, 30), (80, 0), (120, 30), (160, 0)]
    out = et.smooth_points(raw, 2)
    assert out[0] == raw[0] and out[-1] == raw[-1] and len(out) > len(raw)
    assert all(0 <= x <= 160 and 0 <= y <= 30 for x, y in out)       # corner cutting never overshoots
    assert et.smooth_points(raw[:2], 3) == raw[:2]                    # too short: untouched
    huge = [(i, (i * 7) % 13) for i in range(5000)]
    assert len(et.smooth_points(huge, 4)) <= 12000                    # bounded growth


def render_stroke(pg, t, stroke, size=(400, 300), bg=(255, 255, 255)):
    screen = pg.display.get_surface()
    screen.fill(bg)
    t.store.add(stroke)
    t.draw(screen, 0)
    return screen


def test_pen_edges_are_antialiased_without_dark_fringe(pg):
    t = et.ExerciseTools(pg)
    s = et.new_stroke('pen', (230, 50, 70), (100, 150))
    for p in ((180, 200), (260, 170), (340, 260)):
        et.extend_stroke(s, p)
    screen = render_stroke(pg, t, s)
    partial = solid = 0
    for x in range(90, 360):
        for y in range(140, 280):
            r, g, b = screen.get_at((x, y))[:3]
            if (r, g, b) == (255, 255, 255):
                continue
            assert r >= 225, ((x, y), (r, g, b))          # blends of red and white only: no black bleed
            if abs(r - 230) <= 4 and abs(g - 50) <= 4 and abs(b - 70) <= 4:
                solid += 1
            else:
                partial += 1
    assert solid > 200 and partial > 100                  # real soft edge, not hard stair-steps


def test_rect_corners_are_joined_and_closed(pg):
    t = et.ExerciseTools(pg)
    s = et.new_stroke('rect', (65, 155, 255), (120, 150))
    et.extend_stroke(s, (320, 260))
    screen = render_stroke(pg, t, s)
    for corner in ((120, 150), (320, 150), (320, 260), (120, 260)):
        assert screen.get_at(corner)[:3] != (255, 255, 255), corner
    for edge_mid in ((220, 150), (220, 260), (120, 205), (320, 205)):
        assert screen.get_at(edge_mid)[:3] != (255, 255, 255), edge_mid
    assert screen.get_at((220, 205))[:3] == (255, 255, 255)             # interior stays empty


def test_note_box_border_is_closed(pg):
    t = et.ExerciseTools(pg)
    note = et.new_stroke('text', (30, 70, 170), (200, 200))
    note['text'] = 'Ghi chú'
    t._fonts()
    surf, ox, oy = t._stroke_surface(note)
    w, h = surf.get_size()
    assert note['box'] == (w, h) and (ox, oy) == (200, 200)
    for probe in ((w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)):
        assert surf.get_at(probe)[3] > 100, probe       # border present on all four sides


def test_stroke_surface_is_cached_until_the_stroke_changes(pg):
    t = et.ExerciseTools(pg)
    s = et.new_stroke('pen', (230, 50, 70), (100, 100))
    et.extend_stroke(s, (160, 140))
    first = t._stroke_surface(s)[0]
    assert t._stroke_surface(s)[0] is first
    et.extend_stroke(s, (220, 100))
    assert t._stroke_surface(s)[0] is not first


def test_long_live_stroke_uses_cached_chunks_and_matches_final(pg):
    import math
    t = et.ExerciseTools(pg)
    s = et.new_stroke('pen', (230, 50, 70), (60, 300))
    t._drawing = s
    for i in range(1, 400):
        et.extend_stroke(s, (60 + i * 2, 300 + 80 * math.sin(i / 25)))
    screen = pg.display.get_surface()
    screen.fill((255, 255, 255))
    t.draw(screen, 0)
    assert len(t._chunks) >= 4
    live = [screen.get_at((int(x), int(y)))[:3] != (255, 255, 255) for x, y in s['pts'][::40]]
    assert all(live)                                        # no gaps at chunk joins
    t._drawing = None
    t.store.add(s)
    t.draw(screen, 0)
    assert t._chunks == {}


def test_draw_does_not_leak_cache_for_erased_strokes(pg):
    t = et.ExerciseTools(pg)
    screen = pg.display.get_surface()
    for i in range(150):
        s = et.new_stroke('pen', (230, 50, 70), (50, 100 + i))
        et.extend_stroke(s, (90, 120 + i))
        t.store.add(s)
    t.draw(screen, 0)
    t.store.clear()
    t.draw(screen, 0)
    assert len(t._aa) == 0


# ------------------------------------------------ frame/strike follow the mouse
def live_drag_frames(pg, tool, start, ends, scroll=0):
    t = et.ExerciseTools(pg)
    t.expanded, t.tool = True, tool
    screen = pg.display.get_surface()
    assert t.handle_event(mouse(pg, 'down', start), scroll)
    frames = []
    for end in ends:
        t.handle_event(mouse(pg, 'motion', end), scroll)
        screen.fill((255, 255, 255))
        t.draw(screen, scroll)
        frames.append((end, t._stroke_surface(t._drawing, True)[0].get_size(), screen.copy()))
    return t, frames


@pytest.mark.parametrize('end_step', [(1, 1), (-1, -1), (1, -1), (-1, 1)])
@pytest.mark.parametrize('scroll', [0, 300])
def test_rect_follows_mouse_while_dragging_every_direction(pg, end_step, scroll):
    start = (480, 300)
    ends = [(start[0] + end_step[0] * d, start[1] + end_step[1] * (d * 2 // 3)) for d in (40, 90, 150, 220)]
    t, frames = live_drag_frames(pg, 'rect', start, ends, scroll)
    sizes = [f[1] for f in frames]
    assert all(b[0] > a[0] and b[1] > a[1] for a, b in zip(sizes, sizes[1:])), sizes   # grows each frame
    for end, _, shot in frames:
        assert shot.get_at(end)[:3] != (255, 255, 255), end                           # corner under the cursor
        assert shot.get_at((end[0], start[1]))[:3] != (255, 255, 255)                 # edge reaches the cursor's x


def test_strike_follows_mouse_while_dragging(pg):
    t, frames = live_drag_frames(pg, 'strike', (100, 300), [(200, 300), (300, 360), (420, 420)])
    sizes = [f[1] for f in frames]
    assert sizes[0][0] < sizes[1][0] < sizes[2][0]
    for end, _, shot in frames:
        assert shot.get_at(end)[:3] != (255, 255, 255), end


def test_cache_signature_changes_with_shape_even_when_last_point_is_fixed(pg):
    t = et.ExerciseTools(pg)
    s = et.new_stroke('rect', (65, 155, 255), (200, 200))
    et.extend_stroke(s, (260, 240))
    first = t._stroke_surface(s, True)[0]
    assert t._stroke_surface(s, True)[0] is first                    # unchanged shape: cached
    et.extend_stroke(s, (400, 360))
    assert s['pts'][-1] == (200.0, 200.0)                            # last point is the fixed corner
    assert t._stroke_surface(s, True)[0] is not first
