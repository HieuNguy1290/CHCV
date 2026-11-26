"""Modal editors for library topics and full-text activities."""
import tkinter as tk
from collections import Counter
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk

from tuhoc.library.models import DEFAULT_COLOR, DEFAULT_ICON, SUBJECTS, LibraryError, parse_dictation_fields
from tuhoc.library.text_split import split_sentences
from tuhoc.ui.ui_tokens import COLORS, font_at


class Editor:
    def __init__(self, app, title, *, scroll=False):
        self.app = app
        self.window = tk.Toplevel(app, bg=COLORS['background'])
        self.window.title(title)
        self.window.transient(app)
        self.window.minsize(420, 340)
        self.footer = tk.Frame(self.window, bg=COLORS['background'], padx=16, pady=12)
        self.footer.pack(side='bottom', fill='x')
        self.body = tk.Frame(self.window, bg=COLORS['background'], padx=16, pady=10)
        if scroll:
            width = min(750, self.window.winfo_screenwidth() - 50)
            height = min(810, self.window.winfo_screenheight() - 110)
            self.window.geometry(f'{width}x{height}')
            canvas = tk.Canvas(self.window, bg=COLORS['background'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=canvas.yview)
            scrollbar.pack(side='right', fill='y')
            canvas.pack(side='left', fill='both', expand=True)
            canvas.configure(yscrollcommand=scrollbar.set)
            self.body.destroy()
            self.body = tk.Frame(canvas, bg=COLORS['background'], padx=16, pady=10)
            content = canvas.create_window((0, 0), window=self.body, anchor='nw')
            canvas.bind('<Configure>', lambda event: canvas.itemconfigure(content, width=event.width))
            self.body.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
            self.window.bind('<MouseWheel>', lambda event: canvas.yview_scroll(
                -1 if event.delta > 0 else 1, 'units') if not isinstance(event.widget, tk.Text) else None)
            self.window.bind('<Button-4>', lambda event: canvas.yview_scroll(-1, 'units')
                             if not isinstance(event.widget, tk.Text) else None)
            self.window.bind('<Button-5>', lambda event: canvas.yview_scroll(1, 'units')
                             if not isinstance(event.widget, tk.Text) else None)
        else:
            self.body.pack(fill='both', expand=True)

    def caption(self, label):
        self.app.label(self.body, label, 11, True).pack(anchor='w', pady=(9, 3))

    def entry(self, label, value):
        self.caption(label)
        variable = tk.StringVar(self.window, value=value)
        ttk.Entry(self.body, textvariable=variable).pack(fill='x')
        return variable

    def combo(self, label, values, index=0):
        self.caption(label)
        box = ttk.Combobox(self.body, state='readonly', values=values)
        box.current(index)
        box.pack(fill='x')
        return box

    def paragraph(self, label, value, height):
        self.caption(label)
        field = tk.Text(self.body, height=height, wrap='word', undo=True, font=font_at(12))
        field.insert('1.0', value)
        field.pack(fill='x')
        return field

    def open(self, snapshot, save, done):
        original = snapshot()

        def close():
            if snapshot() == original or messagebox.askyesno(
                title='Bỏ thay đổi?', message='Bạn có muốn rời trình soạn mà không lưu thay đổi?',
                parent=self.window,
            ):
                self.window.destroy()
            return 'break'

        def submit():
            try:
                result = save()
            except LibraryError as exc:
                messagebox.showerror(title='Không lưu được', message=str(exc), parent=self.window)
                return
            self.window.destroy()
            done(result)

        self.app.action_button(self.footer, 'Lưu', submit).pack(side='right')
        self.app.action_button(self.footer, 'Hủy', close).pack(side='right', padx=8)
        self.window.protocol('WM_DELETE_WINDOW', close)
        self.window.bind('<Escape>', lambda event: close())
        self.window.wait_visibility()
        self.window.grab_set()
        self.window.focus_set()
        return self.window


def edit_topic(app, store, topic, subject, done):
    topic = topic or {}
    editor = Editor(app, 'Sửa chủ đề' if topic else 'Chủ đề mới')
    name = editor.entry('Tên chủ đề', topic.get('name', ''))
    selected = editor.combo('Môn học', list(SUBJECTS.values()),
                            list(SUBJECTS).index(topic.get('subject', subject)))
    icon = editor.entry('Biểu tượng', topic.get('icon', DEFAULT_ICON))
    color = editor.entry('Màu (#RRGGBB)', topic.get('color', DEFAULT_COLOR))

    def pick_color():
        initial = color.get()
        try:
            editor.window.winfo_rgb(initial)
        except tk.TclError:
            initial = DEFAULT_COLOR
        _, value = colorchooser.askcolor(color=initial, parent=editor.window)
        if value:
            color.set(value)

    app.action_button(editor.body, 'Chọn màu', pick_color).pack(anchor='w', pady=4)
    tags = editor.entry('Nhãn (cách nhau bằng dấu phẩy)', ', '.join(topic.get('tags', [])))

    def values():
        return {
            'name': name.get(), 'subject': list(SUBJECTS)[selected.current()],
            'icon': icon.get(), 'color': color.get(),
            'tags': [tag.strip() for tag in tags.get().split(',') if tag.strip()],
        }

    return editor.open(values, lambda: store.save_topic({**topic, **values()}), done)


def _topic_labels(topics):
    labels = [f"{topic['name']} · {SUBJECTS[topic['subject']]}" for topic in topics]
    counts = Counter(labels)
    return [f'{label} · {index + 1}' if counts[label] > 1 else label
            for index, label in enumerate(labels)]


def edit_text(app, store, topics, topic_id, text, done):
    text = text or {}
    editor = Editor(app, 'Sửa bài viết' if text else 'Bài mới', scroll=True)
    start_topic = next(index for index, topic in enumerate(topics) if topic['id'] == topic_id)
    topic_field = editor.combo('Chủ đề', _topic_labels(topics), start_topic)
    subject = editor.combo('Môn học', list(SUBJECTS.values()),
                           list(SUBJECTS).index(text.get('subject', topics[start_topic]['subject'])))
    topic_field.bind('<<ComboboxSelected>>', lambda event: subject.current(
        list(SUBJECTS).index(topics[topic_field.current()]['subject'])))
    title = editor.entry('Tiêu đề', text.get('title', ''))
    body = editor.paragraph('Nội dung bài viết', text.get('body', ''), 9)
    level = editor.combo('Mức độ', ('1', '2', '3', '4', '5'), text.get('level', 1) - 1)

    def content(widget):
        return widget.get('1.0', 'end-1c')

    media = {kind: text.get(kind, '') for kind in ('image', 'audio')}
    chosen = {}
    for kind, label, filters in (
        ('image', 'Ảnh', [('Ảnh', '*.png *.jpg *.jpeg *.gif *.webp')]),
        ('audio', 'Âm thanh', [('Âm thanh', '*.mp3 *.wav *.ogg')]),
    ):
        editor.caption(label)
        row = tk.Frame(editor.body, bg=COLORS['background'])
        row.pack(fill='x')
        value = tk.StringVar(editor.window, value=media[kind] or 'Chưa có tệp')

        def browse(kind=kind, label=label, filters=filters, value=value):
            path = filedialog.askopenfilename(title=f'Chọn {label.lower()}', filetypes=filters,
                                              parent=editor.window)
            if path:
                chosen[kind] = path
                value.set(Path(path).name)

        def remove(kind=kind, value=value):
            chosen.pop(kind, None)
            media[kind] = ''
            value.set('Chưa có tệp')

        app.action_button(row, 'Chọn tệp để sao chép', browse).pack(side='left')
        app.action_button(row, 'Bỏ tệp', remove).pack(side='left', padx=6)
        ttk.Label(row, textvariable=value, wraplength=320).pack(side='left', fill='x', expand=True)

    editor.caption('Từ khó')
    glossary = [dict(entry) for entry in text.get('glossary', [])]
    table = ttk.Treeview(editor.body, columns=('word', 'meaning'), show='headings', height=4)
    table.heading('word', text='Từ')
    table.column('word', width=160)
    table.heading('meaning', text='Nghĩa')
    table.pack(fill='x')

    def refresh_glossary():
        table.delete(*table.get_children())
        for index, entry in enumerate(glossary):
            table.insert('', 'end', iid=str(index), values=(entry['word'], entry['meaning']))

    def add_word():
        word = simpledialog.askstring('Thêm từ khó', 'Từ:', parent=editor.window)
        if not word or not word.strip():
            return
        meaning = simpledialog.askstring('Thêm từ khó', 'Nghĩa:', parent=editor.window)
        if meaning and meaning.strip():
            glossary.append({'word': word.strip(), 'meaning': meaning.strip()})
            refresh_glossary()

    def remove_word():
        for index in sorted(map(int, table.selection()), reverse=True):
            del glossary[index]
        refresh_glossary()

    refresh_glossary()
    glossary_actions = tk.Frame(editor.body, bg=COLORS['background'])
    glossary_actions.pack(anchor='w', pady=4)
    app.action_button(glossary_actions, 'Thêm từ', add_word).pack(side='left')
    app.action_button(glossary_actions, 'Xóa từ đã chọn', remove_word).pack(side='left', padx=6)

    answers = text.get('dictation', {})
    variants = editor.paragraph('Đáp án nguyên bài khác (mỗi dòng một đáp án)',
                                '\n'.join(answers.get('accepted_variants', [])), 3)
    equivalents = editor.paragraph("Các cách viết tương đương (mỗi dòng: he is | he's)",
                                   '\n'.join(' | '.join(group) for group in answers.get('equivalences', [])), 3)
    preview = editor.paragraph('Xem trước các câu', '', 5)
    preview.configure(state='disabled')

    def preview_sentences():
        preview.configure(state='normal')
        preview.delete('1.0', 'end')
        preview.insert('1.0', '\n'.join(split_sentences(content(body))))
        preview.configure(state='disabled')

    app.action_button(editor.body, 'Cập nhật danh sách câu', preview_sentences).pack(anchor='w', pady=6)
    preview_sentences()

    def values():
        return {
            'topic_id': topics[topic_field.current()]['id'], 'title': title.get(),
            'subject': list(SUBJECTS)[subject.current()], 'level': int(level.get()), 'body': content(body),
            'dictation': parse_dictation_fields(content(variants), content(equivalents)),
            'glossary': list(glossary), **media,
        }

    def save():
        changes = values()
        if text:
            changes['id'] = text['id']
        return store.save_text(changes, media=chosen)

    return editor.open(lambda: (values(), dict(chosen)), save, done)
