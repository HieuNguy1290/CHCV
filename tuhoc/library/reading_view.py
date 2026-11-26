"""Connect library articles to the existing interactive reader."""
import sqlite3
from tkinter import messagebox, simpledialog

from tuhoc.library.audio import speak_article
from tuhoc.library.models import LibraryError
from tuhoc.lessons.pygame_embedded_reader import EmbeddedReader, available


def open_reading(app, store, article, back):
    if not available():
        messagebox.showerror(title='Thiếu thư viện', message='Cần pygame và Pillow để mở bài đọc.',
                             parent=app)
        return
    image = store.resolve_media(article['image'], 'image')
    body = app.layout(f"Đọc · {article['title']}")
    app.button(body, '← Về danh sách', back).pack(anchor='w', pady=(0, 8))

    def add_vocab(selection):
        if not app.student:
            messagebox.showwarning(title='Chưa chọn học sinh', message='Hãy chọn hồ sơ để lưu từ.',
                                   parent=app)
            return
        word = selection.strip()
        if not word:
            return
        meaning = next((entry['meaning'] for entry in article['glossary']
                        if entry['word'].casefold() == word.casefold()), '')
        meaning = simpledialog.askstring('Thêm từ vựng', f'Nghĩa của “{word}”:',
                                         initialvalue=meaning, parent=app)
        if not meaning or not meaning.strip():
            return
        key = app.learning.wordkey(word)
        language = 'vi' if article['subject'] == 'tieng_viet' else 'en'
        try:
            app.db.save_word_in_source(app.student['id'], key if language == app.lang else word,
                                       meaning.strip(), 'reading',
                                       theme=article['topic_id'], level=0, source_title=article['title'],
                                       lang=language)
        except sqlite3.Error as exc:
            messagebox.showerror(title='Không lưu được từ vựng', message=str(exc), parent=app)

    def play():
        try:
            audio = store.resolve_media(article['audio'], 'audio')
            if audio:
                app.play_learning_audio(audio)
            else:
                speak_article(app, article)
        except LibraryError as exc:
            messagebox.showerror(title='Không mở được âm thanh', message=str(exc), parent=app)

    item = {'title': article['title'], 'content': article['body'], 'image': article['image']}
    reader = EmbeddedReader(body, item, image, speak=lambda value: speak_article(app, article, value),
                            on_add_vocab=add_vocab, on_play_audio=play)
    reader.pack(fill='both', expand=True)
    reader._expand_reading_button.configure(
        command=lambda: app._reading_focus(True, origin=reader._expand_reading_button),
    )
    app._v8_active_reader = reader
    for mode, color in getattr(app, '_v8_palette_colors', {}).items():
        reader.set_tool_color(mode, color)

    def cleanup(event):
        if event.widget is reader and app._v8_active_reader is reader:
            app._v8_active_reader = None

    reader.bind('<Destroy>', cleanup, add='+')
    if app.student:
        app.db.save_library_result(app.student['id'], article['id'], 'read', 100, True)
    return reader
