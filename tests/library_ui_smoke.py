"""Exercise the actual library pages on Tk/X11 with a disposable profile.

Run from the repository root with xvfb-run -a python -B tests/library_ui_smoke.py.
"""
import json
import os
from pathlib import Path
import sys
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
    import tkinter as tk

    button(widget, caption).invoke()
    finished = tk.BooleanVar(app)
    app.after(200, lambda: finished.set(True))
    app.wait_variable(finished)


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
    Image.new('RGB', (40, 24), 'green').save(photo)
    audio = root / 'bài.wav'
    with wave.open(str(audio), 'wb') as sound:
        sound.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
        sound.writeframes(b'\x00\x00' * 8000)
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
            assert button(app, 'Đọc').winfo_exists() and button(app, 'Chép chính tả').winfo_exists()
            assert any(getattr(child, 'image', None) for child in descendants(app))

            reader = app.library_practice(article['id'], 'read')
            app.update()
            assert reader.winfo_viewable()
            with patch('tkinter.simpledialog.askstring', return_value='đến trường'):
                reader.on_add_vocab('học')
            with patch.object(app, 'play_learning_audio') as playback:
                reader.on_play_audio()
                playback.assert_called_once_with(store.resolve_media(article['audio'], 'audio'))
            reader._expand_reading_button.invoke()
            app.update()
            assert app._reading_focus_active and app._v8_active_reader is not reader
            app._reading_focus(False)
            app.update()
            assert not app._reading_focus_active
            app.flashcards()
            app.update()
            assert any(isinstance(child, tk.Label) and child.cget('text') == 'Đi học'
                       for child in descendants(app))

            second = store.save_text({'topic_id': topic['id'], 'subject': 'tieng_anh',
                                      'title': 'Bài không có âm thanh', 'body': 'Next article.'})
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
    with TemporaryDirectory(prefix='tuhoc-library-smoke-') as temp:
        os.environ['LOCALAPPDATA'] = str(Path(temp) / 'profile')
        os.environ['TU_HOC_PROFILE'] = '0'
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        smoke(Path(temp))
    print('Passed library Tk/SDL smoke: CRUD editor, attachments, reading, Flashcard, scoring, import, legacy and restart.')
