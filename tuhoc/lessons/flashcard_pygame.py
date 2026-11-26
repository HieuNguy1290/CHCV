"""Fullscreen Pygame flashcard review with a simple 2D flip animation.

Each card face shows only the word/meaning: a picture on top and text below when both exist,
a picture alone, or text alone centred in the card. The card background comes from a theme
(colour preset or the student's own picture).

The window runs on its own thread (see pygame_session_guard), so it never touches the
database: every result goes out through ``on_event((kind, a, b))``:

* ``('rate', word_id, 'again' | 'hard' | 'good')``
* ``('speak', text, None)``
* ``('done', None, None)``      sent once when the window closes

``cards`` are dicts: id, word, meaning, word_image, meaning_image (absolute paths or ''),
and ``direction`` ('forward' = word first, 'reverse' = meaning first).
"""
from tuhoc.exercises.pygame_session_guard import launch as launch_guarded

FLIP_MS = 380
TEXT_SIZES = (76, 64, 54, 46, 40, 34, 30, 26, 22, 18)


def available():
    try:
        import pygame  # noqa: F401
        return True
    except ImportError:
        return False


def launch(title, cards, theme=None, on_event=None):
    if not available() or not cards:
        return False
    args = (str(title), [dict(card) for card in cards], dict(theme or {}), on_event)
    return launch_guarded(_run, args, 'TuHocFlashcards')


def _run(title, cards, theme, on_event):
    import pygame
    from pathlib import Path
    from tuhoc.exercises.pygame_window_utils import vietnamese_font
    from tuhoc.lessons.flashcard_logic import Deck, FlipAnim, clean_word, ease_in_out, face_content, fit_lines
    from tuhoc.lessons.flashcard_themes import preset, tint_for_image

    def emit(kind, a=None, b=None):
        if on_event is not None:
            try:
                on_event((kind, a, b))
            except Exception:
                pass

    pygame.init()
    try:
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        pygame.display.set_caption('Flashcard - ESC: Quay lai')
        clock = pygame.time.Clock()
        w, h = screen.get_size()

        NAVY, BG, MUTED = (35, 52, 94), (244, 247, 245), (113, 134, 120)
        RATE_STYLE = {'again': ('Chưa nhớ', '1', (214, 86, 78)),
                      'hard': ('Hơi nhớ', '2', (226, 154, 44)),
                      'good': ('Đã nhớ', '3', (46, 156, 98))}
        title_font = vietnamese_font(pygame, 22, bold=True)
        small = vietnamese_font(pygame, 17)
        small_bold = vietnamese_font(pygame, 17, bold=True)
        body_font = vietnamese_font(pygame, 34)
        font_cache = {}

        def card_font(bold, size):
            key = (bold, size)
            if key not in font_cache:
                font_cache[key] = vietnamese_font(pygame, size, bold=bold)
            return font_cache[key]

        # --- card geometry --------------------------------------------------------------
        card_w = min(int(w * 0.62), 840)
        card_h = min(int(h * 0.46), 480)
        below = 140                                   # buttons under the card
        top = 78 + max(14, (h - 78 - card_h - below) // 2)
        center = (w // 2, top + card_h // 2)
        card_rect = pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = center

        # --- card background (theme) ----------------------------------------------------
        radius = 28
        mask = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)

        def load_picture(path):
            if not path or not Path(str(path)).is_file():
                return None
            try:
                return pygame.image.load(str(path)).convert_alpha()
            except pygame.error:
                return None

        def make_base():
            fallback = preset('classic')
            colors = {key: tuple(theme.get(key) or fallback[key]) for key in ('face', 'text', 'border')}
            picture = load_picture(theme.get('image_path')) if theme.get('kind') == 'image' else None
            if picture is not None:                               # cover the card, then a veil for readability
                pw, ph = picture.get_size()
                scale = max(card_w / pw, card_h / ph)
                scaled = pygame.transform.smoothscale(picture, (max(card_w, int(pw * scale) + 1), max(card_h, int(ph * scale) + 1)))
                base = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                base.blit(scaled, ((card_w - scaled.get_width()) // 2, (card_h - scaled.get_height()) // 2))
                veil_rgb, veil_alpha, text_rgb = tint_for_image(pygame.transform.average_color(base))
                veil = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                veil.fill((*veil_rgb, veil_alpha))
                base.blit(veil, (0, 0))
                base.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                return base, text_rgb
            base = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            pygame.draw.rect(base, colors['face'], base.get_rect(), border_radius=radius)
            pygame.draw.rect(base, colors['border'], base.get_rect(), 3, border_radius=radius)
            return base, colors['text']

        base_face, text_color = make_base()

        # --- card faces (rendered once, flipped by scaling) ---------------------------
        faces = {}
        pad, gap = 34, 18

        def make_face(card, side):
            text, image_path = face_content(card, side)
            text = text.strip()
            picture = load_picture(image_path)
            if picture is None and not text:
                text = '…'                                    # nothing to show on this side
            face = base_face.copy()
            inner = pygame.Rect(pad, pad, card_w - 2 * pad, card_h - 2 * pad)
            is_word = (card.get('direction') == 'reverse') == (side == 'back')
            band = 0
            if picture is not None:
                band = int(inner.h * 0.58) if text else inner.h
                pw, ph = picture.get_size()
                scale = min(inner.w / pw, band / ph, 2.5)
                shown = pygame.transform.smoothscale(picture, (max(1, int(pw * scale)), max(1, int(ph * scale))))
                top_y = inner.top + (band - shown.get_height()) // 2
                face.blit(shown, shown.get_rect(midtop=(card_w // 2, top_y)))
            if text:
                area_top = inner.top + (band + gap if picture is not None else 0)
                area = pygame.Rect(inner.x, area_top, inner.w, inner.bottom - area_top)
                sizes = tuple(s for s in TEXT_SIZES if s <= 46) if picture is not None else TEXT_SIZES
                size, lines = fit_lines(text, sizes, lambda z, s: card_font(is_word, z).size(s)[0],
                                        lambda z: card_font(is_word, z).get_linesize() + 4,
                                        int(area.w * 0.94), area.h)
                font = card_font(is_word, size)
                line_h = font.get_linesize() + 4
                y = area.centery - len(lines) * line_h // 2
                for line in lines:
                    surf = font.render(line, True, text_color)
                    face.blit(surf, surf.get_rect(midtop=(card_w // 2, y)))
                    y += line_h
            return face

        def face_for(card, side):
            key = (card.get('id'), side)
            if key not in faces:
                faces[key] = make_face(card, side)
            return faces[key]

        # --- state ------------------------------------------------------------------------
        deck = Deck(cards)
        anim = FlipAnim(FLIP_MS)
        pop_started = pygame.time.get_ticks()
        POP_MS = 180
        closing = False

        speak_btn = pygame.Rect(0, 0, 170, 40)
        skip_btn = pygame.Rect(0, 0, 170, 40)
        speak_btn.midtop = (w // 2 - 95, card_rect.bottom + 26)
        skip_btn.midtop = (w // 2 + 95, card_rect.bottom + 26)
        rate_btns = {}
        for i, name in enumerate(('again', 'hard', 'good')):
            rect = pygame.Rect(0, 0, 210, 56)
            rect.midtop = (w // 2 + (i - 1) * 226, speak_btn.bottom + 18)
            rate_btns[name] = rect

        def answer_shown(now):
            return anim.target == 1.0 and not anim.busy(now)

        def do_rate(name):
            nonlocal pop_started
            now = pygame.time.get_ticks()
            if not answer_shown(now):
                return
            result = deck.rate(name)
            if result:
                emit('rate', result[0].get('id'), result[1])
                anim.reset(now)
                pop_started = now

        def do_skip():
            nonlocal pop_started
            now = pygame.time.get_ticks()
            if len(deck.queue) > 1:
                deck.skip()
                anim.reset(now)
                pop_started = now

        def do_speak():
            card = deck.current
            if card:
                # speak the word, whichever side is showing (a picture-only word has no text)
                emit('speak', clean_word(card.get('word')))

        def draw_button(rect, label, fill, enabled=True, mouse=None):
            color = fill if enabled else tuple(int(c * .45 + 140 * .55) for c in fill)
            if enabled and mouse and rect.collidepoint(mouse):
                color = tuple(min(255, c + 22) for c in color)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            text = small_bold.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

        def draw_header():
            pygame.draw.rect(screen, NAVY, (0, 0, w, 64))
            screen.blit(title_font.render('FLASHCARD  |  ' + title[:60], True, (255, 255, 255)), (23, 18))
            info_text = small.render(f'{deck.done}/{deck.total}   ·   ESC: Thoát', True, (205, 216, 240))
            screen.blit(info_text, (w - info_text.get_width() - 23, 22))
            pygame.draw.rect(screen, (60, 80, 130), (0, 64, w, 6))
            if deck.total:
                pygame.draw.rect(screen, (96, 200, 150), (0, 64, int(w * deck.done / deck.total), 6))

        def draw_card(now):
            card = deck.current
            value = anim.value(now)
            width_k, height_k = FlipAnim.width_scale(value), FlipAnim.height_scale(value)
            pop = 0.92 + 0.08 * ease_in_out((now - pop_started) / POP_MS)
            face = face_for(card, 'back' if FlipAnim.showing_back(value) else 'front')
            tw, th = max(2, int(card_w * width_k * pop)), max(2, int(card_h * height_k * pop))
            shadow = pygame.Surface((int(card_w * 0.86 * width_k * pop) + 4, 26), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 46), shadow.get_rect())
            screen.blit(shadow, shadow.get_rect(center=(center[0], card_rect.bottom + 12)))
            if (tw, th) == (card_w, card_h):
                screen.blit(face, card_rect.topleft)
            else:
                scaled = pygame.transform.smoothscale(face, (tw, th))
                dim = int(70 * (1.0 - width_k))              # darker while edge-on
                if dim:
                    scaled.fill((255 - dim, 255 - dim, 255 - dim, 255), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(scaled, scaled.get_rect(center=center))

        def draw_summary():
            lines = [('Hoàn thành bộ thẻ!', title_font), (f'Đã ôn {deck.total} từ', body_font)]
            y = h // 2 - 120
            for text, font in lines:
                surf = font.render(text, True, NAVY)
                screen.blit(surf, surf.get_rect(midtop=(w // 2, y)))
                y += surf.get_height() + 18
            for name in ('good', 'hard', 'again'):
                label, _key, color = RATE_STYLE[name]
                surf = small_bold.render(f'{label}: {deck.counts[name]} lượt', True, color)
                screen.blit(surf, surf.get_rect(midtop=(w // 2, y)))
                y += 32
            tip = small.render('Nhấn ESC hoặc Enter để quay lại', True, MUTED)
            screen.blit(tip, tip.get_rect(midtop=(w // 2, y + 18)))

        # --- main loop --------------------------------------------------------------------
        while not closing:
            now = pygame.time.get_ticks()
            mouse = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    closing = True
                elif ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_ESCAPE, pygame.K_F11):
                        closing = True
                    elif deck.finished:
                        if ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            closing = True
                    elif ev.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                        anim.flip(now)
                    elif ev.key in (pygame.K_1, pygame.K_KP1):
                        do_rate('again')
                    elif ev.key in (pygame.K_2, pygame.K_KP2):
                        do_rate('hard')
                    elif ev.key in (pygame.K_3, pygame.K_KP3):
                        do_rate('good')
                    elif ev.key == pygame.K_RIGHT:
                        do_skip()
                    elif ev.key == pygame.K_s:
                        do_speak()
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and not deck.finished:
                    if speak_btn.collidepoint(ev.pos):
                        do_speak()
                    elif skip_btn.collidepoint(ev.pos):
                        do_skip()
                    else:
                        rated = next((n for n, r in rate_btns.items() if r.collidepoint(ev.pos)), None)
                        if rated:
                            do_rate(rated)
                        elif card_rect.collidepoint(ev.pos):
                            anim.flip(now)

            screen.fill(BG)
            draw_header()
            if deck.finished:
                draw_summary()
            else:
                draw_card(now)
                draw_button(speak_btn, 'Phát âm (S)', NAVY, True, mouse)
                draw_button(skip_btn, 'Bỏ qua (→)', (110, 124, 150), len(deck.queue) > 1, mouse)
                ready = answer_shown(now)
                for name, rect in rate_btns.items():
                    label, key, color = RATE_STYLE[name]
                    draw_button(rect, f'{label}  ({key})', color, ready, mouse)
            pygame.display.flip()
            clock.tick(60)
    finally:
        emit('done')
