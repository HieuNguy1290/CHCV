"""Exercise the actual library pages on Tk/X11 with a disposable profile.

Run from the repository root with xvfb-run -a python -B tests/library_ui_smoke.py.
"""
import json
import math
import os
from pathlib import Path
import sys
from struct import pack
from tempfile import TemporaryDirectory
from unittest.mock import patch
import wave

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def button(widget, caption):
    import tkinter as tk

    return next(child for child in descendants(widget)
                if isinstance(child, tk.Button) and child.cget('text') == caption)


def navigate(app, widget, caption):
    if app._navigation_busy:
        settle(app, 220)
    button(widget, caption).invoke()
    settle(app, 300)


def settle(app, delay=220):
    import tkinter as tk

    finished = tk.BooleanVar(app)
    app.after(delay, lambda: finished.set(True))
    app.wait_variable(finished)


def reader_tool(page, label):
    def find(container):
        return next((widget for widget in descendants(container)
                     if getattr(widget, 'tool_label', None) == label and widget.winfo_viewable()), None)

    page.update_idletasks()
    tool = find(page.tool_rail)
    if tool is None:
        if page.panel_name != 'tools':
            page.tool_overflow.invoke()
            page.update_idletasks()
        assert page.panel_name == 'tools'
        tool = find(page.panel)
    assert tool is not None, label
    return tool


def visible_tools(container):
    return [widget for widget in descendants(container)
            if getattr(widget, 'tool_label', None) and widget.winfo_viewable()]


def check_reader(app, reader, photo):
    from tuhoc.library.reading_view import PALETTES

    page, canvas = reader.page, reader.canvas
    settle(app)
    assert page.theme == 'paper'
    assert (app.winfo_width(), app.winfo_height()) == (1440, 900), app.winfo_geometry()
    assert abs(reader._text_lines[0][1] + 320 - canvas.winfo_width() / 2) < 20
    first_line, _, _, first_font, first_size = reader._text_lines[0]
    assert first_font.size(first_line)[0] == 640
    assert any(font.size(line)[0] < 640 for line, _, _, font, _ in reader._text_lines)
    assert all(metric is not None for metric in reader._serif_font(first_size).metrics('học vẻ đến trường'))
    text_left = reader._text_lines[0][1]
    rail = page.tool_rail
    canvas_geometry = (canvas.winfo_width(), canvas.winfo_height())
    def rail_tools():
        return [widget for widget in visible_tools(rail) if widget is not page.tools]

    rail_buttons = rail_tools()
    rail_labels = [widget.tool_label for widget in rail_buttons]
    assert rail_buttons and rail.winfo_rootx() - page.winfo_rootx() <= 16
    assert rail.winfo_class() == 'Canvas' and rail.find_withtag('rail')
    assert rail.winfo_rooty() - page.header.winfo_rooty() - page.header.winfo_height() >= 16
    assert {'Màu', 'Xóa tất cả'} <= set(rail_labels)
    with patch('tkinter.colorchooser.askcolor', return_value=(None, None)) as chooser:
        reader_tool(page, 'Màu').invoke()
        chooser.assert_called_once()
    reader_tool(page, 'Xóa tất cả').invoke()
    assert len({widget.winfo_rootx() for widget in rail_buttons}) == 1
    assert len({widget.winfo_rooty() for widget in rail_buttons}) == len(rail_buttons)
    assert all(str(widget.cget('image')) for widget in rail_buttons)
    page.tools.invoke()
    app.update_idletasks()
    assert page.tools.winfo_viewable()
    assert not rail_tools()
    page.tools.invoke()
    app.update_idletasks()
    assert [widget.tool_label for widget in rail_tools()] == rail_labels
    assert (canvas.winfo_width(), canvas.winfo_height()) == canvas_geometry
    canvas.focus_force()
    initial_scroll = canvas.yview()
    canvas.event_generate('<MouseWheel>', delta=-120)
    assert canvas.yview() != initial_scroll
    canvas.event_generate('<Next>')
    assert reader._reading_anchor()[0] is not None
    anchor = reader._reading_anchor()
    page.aa.invoke()
    assert reader._text_lines[0][1] == text_left
    for theme, label in (('light', 'Sáng'), ('dark', 'Tối'), ('paper', 'Mặc định'), ('dark', 'Tối')):
        button(page.panel, label).invoke()
        assert button(page.panel, f'✓ {label}')
        assert canvas.cget('bg') == PALETTES[theme]['page']
    screenshot = os.environ.get('TUHOC_READER_CAPTURE')
    if screenshot:
        from PIL import ImageGrab

        app.update()
        ImageGrab.grab(window=int(app.wm_frame(), 0)).save(screenshot)
    zoom_down, zoom_up, spacing_down, spacing_up = page.panel_controls
    zoom_up.invoke()
    assert reader._text_lines[0][4] > first_size
    zoom_down.invoke()
    assert reader._text_lines[0][4] == first_size
    zoom_up.invoke()
    line_gap = reader._text_lines[1][2] - reader._text_lines[0][2]
    spacing_up.invoke()
    assert reader._text_lines[1][2] - reader._text_lines[0][2] > line_gap
    spacing_down.invoke()
    assert reader._text_lines[1][2] - reader._text_lines[0][2] == line_gap
    spacing_up.invoke()
    assert reader.zoom == 1.15 and reader.line_spacing == 1.8
    assert reader._reading_anchor() == anchor
    page.panel.focus_force()
    page.panel.event_generate('<Escape>')
    assert page.panel is None

    canvas.yview_moveto(0)
    line, left, y, font, _ = reader._text_lines[0]
    start = line.index('học')
    x1, x2 = (10 + left + font.size(line[:i])[0] for i in (start, start + 3))

    def drag(xa, ya, xb, yb):
        canvas.event_generate('<ButtonPress-1>', x=xa, y=ya)
        canvas.event_generate('<B1-Motion>', x=xb, y=yb)
        canvas.event_generate('<ButtonRelease-1>', x=xb, y=yb)

    drag(x1, y+5, x2, y+5)
    assert reader.selected_text() == 'học'
    popup = reader._selection_popup
    assert any(widget.cget('text') == 'đến trường' for widget in descendants(popup)
               if widget.winfo_class() == 'Label')
    with patch.object(reader, 'on_add_vocab', return_value=False):
        button(popup, 'Lưu vào Flashcard').invoke()
        assert button(popup, 'Lưu vào Flashcard')
    button(popup, 'Lưu vào Flashcard').invoke()
    assert button(popup, '✓ Đã lưu')
    with patch('tkinter.simpledialog.askstring', return_value=None):
        assert not reader.on_add_vocab('từ chưa có nghĩa')
    page.words.invoke()
    assert button(page.panel, '✓ Đã lưu')
    button(page.panel, 'Lưu vào Flashcard').invoke()
    assert len(page.saved_words) == 2
    assert reader._text_lines[0][1] == text_left
    page.words.invoke()

    reader_tool(page, 'Tô chữ').invoke()
    assert reader_tool(page, 'Tô chữ').tool_selected
    drag(x1, y+5, x2, y+5)
    reader_tool(page, 'Gạch chân').invoke()
    drag(x1, y+5, x2, y+5)
    spans = [item['text_span'] for item in reader._annotations]
    assert len(spans) == 2 and spans[0] == spans[1]
    page.aa.invoke()
    button(page.panel, '+').invoke()
    page.panel_controls[3].invoke()
    assert [item['text_span'] for item in reader._annotations] == spans
    for item in reader._annotations:
        lo, hi = item['text_span']
        text = ' '.join(line[0] for line in reader._text_lines)
        assert text[lo:hi] == 'học'
        assert reader._text_anchor_rects(item)
    page.panel_controls[2].invoke()

    reader_tool(page, 'Vẽ').invoke()
    drag(x1, y+5, x2, y+15)
    assert len(reader.strokes) == 1
    page.aa.invoke()
    assert all(control.cget('state') == 'disabled' for control in page.panel_controls)
    locked = reader.zoom, reader.line_spacing, reader._stroke_screen_points(reader.strokes[0])
    for control in page.panel_controls:
        control.invoke()
    assert (reader.zoom, reader.line_spacing, reader._stroke_screen_points(reader.strokes[0])) == locked
    button(page.panel, 'Sáng').invoke()
    assert page.theme == 'light'
    reader_tool(page, 'Tẩy').invoke()
    canvas.event_generate('<ButtonPress-1>', x=x1, y=y+5)
    assert not reader.strokes
    reader_tool(page, 'Hoàn tác').invoke()
    assert len(reader.strokes) == 1
    reader_tool(page, 'Làm lại').invoke()
    assert not reader.strokes
    reader_tool(page, 'Hoàn tác').invoke()
    assert len(reader.strokes) == 1
    reader_tool(page, 'Làm lại').invoke()
    assert not reader.strokes

    reader_tool(page, 'Ghi chú').invoke()
    note_line = reader._text_lines[1][2]
    with patch('tkinter.simpledialog.askstring', return_value='Ghi chú của em'):
        canvas.event_generate('<ButtonPress-1>', x=x1, y=note_line+6)
    assert reader.notes[0][2] == 'Ghi chú của em'
    with patch('tkinter.filedialog.askopenfilename', return_value=str(photo)):
        reader_tool(page, 'Chèn ảnh').invoke()
    picture_line = reader._text_lines[2][2]
    canvas.event_generate('<ButtonPress-1>', x=x1, y=picture_line+6)
    assert len(reader._pictures) == 1
    page.aa.invoke()
    page.panel_controls[3].invoke()
    height = reader._previous_layout['height']
    assert abs(reader.notes[0][1] * height - reader._text_lines[1][2] - 6) < 1
    assert abs(reader._pictures[0]['y'] - reader._text_lines[2][2] - 6) < 1
    page.panel_controls[2].invoke()
    reader_tool(page, 'Vẽ').invoke()
    drag(x1, y+5, x2, y+15)
    assert len(reader.strokes) == 1

    app.minsize(520, 500)
    app.geometry('610x650')
    app.update_idletasks()
    settle(app, 600)
    page.tool_overflow.invoke()
    app.update_idletasks()
    assert page.panel_name == 'tools'
    narrow_tools = visible_tools(page.panel)
    assert narrow_tools
    assert len({widget.winfo_rootx() for widget in narrow_tools}) == 1
    assert page.panel.winfo_rootx() + page.panel.winfo_width() <= page.winfo_rootx() + page.winfo_width()
    page.panel.focus_force()
    page.panel.event_generate('<Escape>')
    assert page.panel is None and page.tools.winfo_viewable()
    page.words.invoke()
    assert page.panel.winfo_x() + page.panel.winfo_width() <= page.winfo_width()
    assert reader._text_lines[0][1] < text_left, (
        app.winfo_geometry(), page.winfo_width(), canvas.winfo_width(), reader._page_width,
        reader._text_lines[0][1], text_left)
    button(page.panel, '✕').invoke()
    app.geometry('610x500')
    app.update_idletasks()
    settle(app, 600)
    assert len(rail_tools()) < len(rail_labels)
    assert {'Màu', 'Xóa tất cả'} <= {widget.tool_label for widget in rail_tools()}
    moved = next(label for label in rail_labels
                 if label != 'Công cụ khác' and label not in {widget.tool_label for widget in rail_tools()})
    assert reader_tool(page, moved).master.master is page.panel_body
    page.close_panel()
    canvas.yview_moveto(.35)
    state = (page.theme, reader.zoom, reader.line_spacing, reader._reading_anchor(), spans)
    reader.canvas.focus_force()
    reader.canvas.event_generate('<F11>')
    settle(app)
    assert page.expanded and app._v8_active_reader is reader
    assert (page.theme, reader.zoom, reader.line_spacing, reader._reading_anchor(),
            [item['text_span'] for item in reader._annotations]) == state
    app._reading_focus(False)
    settle(app)
    assert not page.expanded and app._v8_active_reader is reader
    assert (page.theme, reader.zoom, reader.line_spacing, reader._reading_anchor(),
            [item['text_span'] for item in reader._annotations]) == state
    assert len(reader.strokes) == 1
    assert reader.notes[0][2] == 'Ghi chú của em'
    assert len(reader._pictures) == 1
    app.reduce_motion = False
    page.tool_overflow.invoke()
    assert page.jobs.jobs
    page.close_panel()
    assert not page.jobs.jobs
    app.reduce_motion = True


def smoke(root):
    import tkinter as tk
    from tkinter import ttk

    from PIL import Image

    from tuhoc.app import main
    from tuhoc.lessons import dictation_vi, upgrade_v2
    from tuhoc.library import ui_mixin
    from tuhoc.library.dictation_view import AudioPanel
    from tuhoc.library.store import LibraryStore

    project = root / 'source-data'
    photo = root / 'ảnh.png'
    Image.new('RGB', (640, 360), 'green').save(photo)
    audio = root / 'bài.wav'
    with wave.open(str(audio), 'wb') as sound:
        sound.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
        sound.writeframes(b''.join(pack('<h', round(1800 * math.sin(2 * math.pi * 440 * i / 8000)))
                                   for i in range(8000)))
    dictation = project / 'mon_hoc' / 'tieng_anh' / 'dictation'
    dictation.mkdir(parents=True)
    old_file = dictation / 'dap_an_chinh_ta.json'
    old_file.write_text(json.dumps({'items': [
        {'id': 'ct01', 'title': 'Bài cũ', 'audio': str(audio), 'answer': 'Hello there.'},
    ]}), encoding='utf-8')
    legacy_bytes = old_file.read_bytes()

    errors = []

    def report_error(*args, message=None, **kwargs):
        errors.append(message if message is not None else args[1])

    with patch.object(upgrade_v2, 'PROJECT_ROOT', project), patch.object(dictation_vi, 'PROJECT_ROOT', project), \
         patch.object(ui_mixin, 'PROJECT_ROOT', project), patch('tkinter.messagebox.showerror', side_effect=report_error):
        app = main.App()
        db = app.db
        try:
            sid = db.add_student('Học viên thử', 2)
            app.student = db.students()[0]
            app.reduce_motion = True
            if os.environ.get('TUHOC_SMOKE_DPI'):
                app.tk.call('tk', 'scaling', float(os.environ['TUHOC_SMOKE_DPI']) / 72)
            store = LibraryStore(app.data_dir)
            page = app.reading_menu()
            app.update()
            button(page, '＋ Chủ đề mới').invoke()
            editor = app.grab_current()
            topic_name = next(child for child in descendants(editor) if isinstance(child, ttk.Entry)
                              and not isinstance(child, ttk.Combobox))
            topic_name.insert(0, 'Gia đình em')
            button(editor, 'Lưu').invoke()
            topic, = store.topics()
            page = app.library_topic(topic['id'])
            app.update()
            button(page, '＋ Bài mới').invoke()
            editor = app.grab_current()
            title = next(child for child in descendants(editor) if isinstance(child, ttk.Entry)
                         and not isinstance(child, ttk.Combobox))
            title.insert(0, 'Đi học')
            body, variants, equivalents, preview = [child for child in descendants(editor)
                                                     if isinstance(child, tk.Text)]
            body.insert('1.0', 'Em đi học. Em vui!')
            variants.insert('1.0', 'Em đến lớp. Em vui!')
            equivalents.insert('1.0', 'vui | vui vẻ')
            with patch('tkinter.filedialog.askopenfilename', side_effect=[str(photo), str(audio)]):
                for child in descendants(editor):
                    if isinstance(child, tk.Button) and child.cget('text') == 'Chọn tệp để sao chép':
                        child.invoke()
            with patch('tkinter.simpledialog.askstring', side_effect=['học', 'đến trường']):
                button(editor, 'Thêm từ').invoke()
            button(editor, 'Cập nhật danh sách câu').invoke()
            assert preview.get('1.0', 'end-1c') == 'Em đi học.\nEm vui!'
            with patch('tkinter.messagebox.askyesno', return_value=False) as confirmation:
                button(editor, 'Hủy').invoke()
                confirmation.assert_called_once()
                assert editor.winfo_exists()
            button(editor, 'Lưu').invoke()
            article, = store.texts(topic['id'])
            assert article['image'] and article['audio'] and article['glossary']
            captions = lambda page: [widget.cget('text') for widget in descendants(page)
                                     if isinstance(widget, tk.Button)]
            assert 'Đọc' in captions(app) and 'Chép chính tả' not in captions(app)
            detail = app.library_article(article['id'], 'dictation')
            assert 'Chép chính tả' in captions(detail) and 'Đọc' not in captions(detail)
            assert any(getattr(child, 'image', None) for child in descendants(app))

            long_article = store.save_text({
                'topic_id': topic['id'], 'subject': article['subject'], 'title': 'Đi học · bài dài',
                'body': '\n\n'.join(f'Em đi học. {i} Em vui vẻ đến trường cùng các bạn. ' * 5
                                      for i in range(30)),
                'image': article['image'], 'audio': article['audio'],
                'glossary': [*article['glossary'], {'word': 'các bạn', 'meaning': 'bạn học'}],
            })
            app.state('normal')
            app.maxsize(2000, 1500)
            app.geometry('1440x900+0+0')
            app.update()
            reader = app.library_practice(long_article['id'], 'read')
            app.update()
            assert reader.winfo_viewable()
            check_reader(app, reader, photo)
            with patch.object(app, 'play_learning_audio') as playback:
                reader._listen_button.invoke()
                playback.assert_called_once_with(store.resolve_media(long_article['audio'], 'audio'))
            player = None
            if os.environ.get('TUHOC_SMOKE_REAL_AUDIO'):
                import pygame

                reader._listen_button.invoke()
                player = app._waveform_window
                player.play_btn.invoke()
                assert player.playing and pygame.mixer.music.get_busy()
                settle(app, 180)
                assert player.pos > 0
            reader.page.back_button.invoke()
            assert not reader.winfo_exists()
            if player is not None:
                assert not player.winfo_exists() and not pygame.mixer.music.get_busy()
            reader = app.library_practice(article['id'], 'read')
            app.update()
            assert reader.on_add_vocab('học')
            app.flashcards()
            app.update()
            assert any(isinstance(child, tk.Label) and child.cget('text') == 'Đi học'
                       for child in descendants(app))

            store.delete_text(long_article['id'])
            second = store.save_text({'topic_id': topic['id'], 'subject': 'tieng_anh',
                                      'title': 'Bài không có âm thanh', 'body': 'Next article.'})
            reader = app.library_practice(second['id'], 'read')
            settle(app)
            assert reader.page.theme == 'light' and reader.zoom == 1.3 and reader.line_spacing == 1.8
            assert reader.image_file is None
            with patch.object(app, '_speak') as speaker:
                reader._listen_button.invoke()
                speaker.assert_called_once_with(second['body'])
            page = app.library_practice(article['id'], 'dictation')
            app.update()
            player = next(child for child in descendants(page) if isinstance(child, AudioPanel))
            player.toggle()
            assert player.player.active
            player.seek_fraction(0.5)
            assert player.player.position_ms() >= 500
            field = next(child for child in descendants(page) if isinstance(child, tk.Text))
            field.insert('1.0', 'Em đến lớp, em vui vẻ!')
            button(page, '✓ Kiểm tra đáp án').invoke()
            progress = {row['mode']: row['best_score'] for row in db.library_progress(sid, article['id'])}
            assert progress == {'read': 100, 'dictation': 100}
            navigate(app, page, 'Bài tiếp theo →')
            assert not player.player.active
            with patch.object(app, '_speak') as speaker:
                button(app, '🔊 Đọc bài bằng giọng máy').invoke()
                speaker.assert_called_once_with(second['body'])
            page = app.library_topic(topic['id'], 'dictation')
            assert any(isinstance(child, tk.Label) and 'Chép tốt nhất 100%' in child.cget('text')
                       and '✓ Đã đọc' in child.cget('text') for child in descendants(page))

            page = app.dictation_page()
            with patch('tkinter.messagebox.showinfo') as info:
                button(page, 'Nhập từ dữ liệu cũ').invoke()
                assert 'Đã nhập 1 bài' in info.call_args.kwargs['message']
                button(app, 'Nhập từ dữ liệu cũ').invoke()
                assert 'Đã nhập 0 bài, bỏ qua 1 bài' in info.call_args.kwargs['message']
            assert old_file.read_bytes() == legacy_bytes
            navigate(app, app, 'Xem bản cũ')
            assert button(app, 'VÀO CHÉP CHÍNH TẢ →').winfo_exists()
            page = app.reading_menu()
            navigate(app, page, 'Xem bản cũ')
            assert 'Tập đọc' in app._admin_page
            assert not errors

            original = store.topics_file.read_bytes()
            broken = b'{"topics":'
            store.topics_file.write_bytes(broken)
            try:
                app.reading_menu()
                assert 'Expecting value' in errors[-1]
                assert store.topics_file.read_bytes() == broken
            finally:
                store.topics_file.write_bytes(original)
        finally:
            app.destroy()
            db.conn.close()

        # Reopen the saved profile without modifying legacy or learner data.
        app = main.App()
        try:
            assert LibraryStore(app.data_dir).get_text(article['id']) == article
            assert len(app.db.library_progress(sid, article['id'])) == 2
            app.db.delete_student(sid)
            assert app.db.library_progress(sid) == []
        finally:
            app.destroy()
            app.db.conn.close()


if __name__ == '__main__':
    import faulthandler

    faulthandler.dump_traceback_later(45, exit=True)
    with TemporaryDirectory(prefix='tuhoc-library-smoke-') as temp:
        os.environ['LOCALAPPDATA'] = str(Path(temp) / 'profile')
        os.environ['TU_HOC_PROFILE'] = '0'
        if not os.environ.get('TUHOC_SMOKE_REAL_AUDIO'):
            os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        smoke(Path(temp))
    faulthandler.cancel_dump_traceback_later()
    print('Passed library Tk/SDL smoke: CRUD editor, attachments, reading, Flashcard, scoring, import, legacy and restart.')
