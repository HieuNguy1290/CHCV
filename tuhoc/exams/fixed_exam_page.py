"""Choose a published fixed exam or prepare one in the separate collection."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from tuhoc.exams import fixed_exam_packages
from tuhoc.exams.fixed_exam_editor import FixedExamEditor
from tuhoc.exams.fixed_exam_store import FixedExamStore
from tuhoc.storage.question_packages import EXTENSION
from tuhoc.ui.question_package_dialog import _confirm
from tuhoc.ui.ui_components import Card, EmptyState, RoundedButton
from tuhoc.ui.ui_tokens import COLORS, font_at


EXAMPLE = {
    'title': 'Reading practice',
    'minutes': 15,
    'subject': 'tieng_anh',
    'sections': [{
        'title': 'Passage 1',
        'passage': 'The city library opens at nine every weekday. It closes on Sundays.',
        'questions': [
            {'type': 'choice', 'prompt': 'When does the library open?',
             'options': ['At seven', 'At nine', 'At ten'], 'answer': 'At nine'},
            {'type': 'choice', 'prompt': 'The library opens on Sundays.',
             'options': ['True', 'False', 'Not Given'], 'answer': 'False'},
            {'type': 'fill', 'prompt': 'The building is a city ____.', 'answer': 'library'},
        ],
    }],
}


def show_fixed_exams(app):
    store = FixedExamStore(app.data_dir)
    body = app.layout('Kiểm tra / Bộ đề')

    def launch(data, preview=False):
        from tuhoc.exams.exam_pygame import run_fixed_exam
        from tuhoc.exercises.pygame_session_guard import launch as launch_sdl
        try:
            exam = store.assemble(data)
            student_id = app.student['id'] if app.student else None
            args = (app.data_dir, student_id, exam, preview, getattr(app,'reduce_motion',False))
            if not launch_sdl(run_fixed_exam, args, 'TuHocFixedExamSDL'):
                raise ValueError('Một cửa sổ bài tập hoặc kiểm tra đang mở.')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            messagebox.showerror('Bộ đề', str(exc), parent=app)

    def edit(published=None):
        existing = getattr(app, '_fixed_exam_editor', None)
        if existing is not None and existing.winfo_exists():
            existing.lift()
            return
        app._fixed_exam_editor = FixedExamEditor(app, store, EXAMPLE, published, launch, refresh)

    package_types = [('Gói Bộ đề TuHoc', '*' + EXTENSION)]

    def export_shared(data):
        path = filedialog.asksaveasfilename(parent=app, filetypes=package_types,
                                            defaultextension=EXTENSION)
        if not path:
            return
        try:
            fixed_exam_packages.export_exam(path, store, data)
        except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
            messagebox.showerror('Không xuất được bộ đề', str(exc), parent=app)
            return
        messagebox.showinfo('Đã xuất bộ đề', 'Đã lưu đề và các tệp đính kèm.', parent=app)

    def import_shared():
        path = filedialog.askopenfilename(parent=app, filetypes=package_types)
        if not path:
            return
        try:
            package = fixed_exam_packages.read_exam(path)
            status = fixed_exam_packages.exam_status(store, package)
            if status == 'duplicate':
                messagebox.showinfo('Bộ đề đã có', 'Phiên bản này đã được nhập trước đó.', parent=app)
                return
            title = _preview_package(app, package, status)
            if title is None:
                return
            added = fixed_exam_packages.import_exam(store, package, title, allow_update=status == 'update')
        except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
            messagebox.showerror('Không nhập được bộ đề', str(exc), parent=app)
            return
        if added is None:
            messagebox.showinfo('Bộ đề đã có', 'Phiên bản này đã được nhập trước đó.', parent=app)
        else:
            refresh()
            messagebox.showinfo('Đã nhập bộ đề', f'Đã thêm {added["title"]} vào danh sách Bộ đề.', parent=app)

    actions = tk.Frame(body, bg=COLORS['background'])
    actions.pack(fill='x', pady=(0, 12))
    RoundedButton(actions, 'Soạn bộ đề', edit).pack(side='left')
    RoundedButton(actions, 'Nhập gói bộ đề', import_shared).pack(side='left', padx=8)
    listing = tk.Frame(body, bg=COLORS['background'])
    listing.pack(fill='x')

    def refresh():
        if not listing.winfo_exists():
            return
        for widget in listing.winfo_children():
            widget.destroy()
        try:
            exams = store.published()
        except (OSError, ValueError) as exc:
            EmptyState(listing, str(exc)).pack(fill='x')
            return
        if not exams:
            EmptyState(listing, 'Chưa có bộ đề cố định.').pack(fill='x')
        for data in exams:
            card = Card(listing)
            card.pack(fill='x', pady=4)
            count = sum(len(section['questions']) for section in data['sections'])
            tk.Label(card, text=f'{data["title"]} · {count} câu · {data["minutes"]} phút',
                     bg=COLORS['surface'], fg=COLORS['text'], font=font_at(14, 'bold')).pack(side='left')
            RoundedButton(card, 'Làm bài', lambda item=data: launch(item)).pack(side='right')
            button = RoundedButton(card, 'Soạn bản mới', lambda item=data: edit(item), variant='outline', width=130)
            button.pack(side='right', padx=8)
            RoundedButton(card, 'Xuất gói', lambda item=data: export_shared(item),
                          variant='outline', width=100).pack(side='right')

    refresh()
    app._fixed_morph_header = listing
    morph = getattr(app,'morph',None)
    if morph:
        morph.arrive('fixed-list',listing)


def _preview_package(app, package, status):
    data = package.exam
    window = tk.Toplevel(app)
    window.title('Nhập gói bộ đề')
    window.transient(app)
    window.geometry('620x460')
    window.minsize(460, 360)
    body = ttk.Frame(window, padding=14)
    body.pack(fill='both', expand=True)
    subject = {'tieng_anh': 'Tiếng Anh', 'tieng_viet': 'Tiếng Việt', 'toan': 'Toán'}
    count = sum(len(section['questions']) for section in data['sections'])
    ttk.Label(body, text=f"{subject[data['subject']]} · {data['minutes']} phút · {count} câu"
                         f" · {len(package.assets)} tệp đính kèm").pack(anchor='w')
    if status == 'update':
        ttk.Label(body, text='Đã có phiên bản trước. Bản này sẽ được thêm thành bộ đề riêng.').pack(anchor='w')
    preview = ScrolledText(body, wrap='word', height=8)
    preview.pack(fill='both', expand=True, pady=(8, 0))
    for index, section in enumerate(data['sections'], 1):
        preview.insert('end', f"{section.get('title') or f'Phần {index}'}\n")
        if section.get('passage'):
            preview.insert('end', str(section['passage']) + '\n\n')
        for number, row in enumerate(section['questions'], 1):
            preview.insert('end', f"{number}. {row.get('prompt') or row['type']}\n")
        preview.insert('end', '\n')
    preview.configure(state='disabled')
    ttk.Label(body, text='Tên bộ đề mới').pack(anchor='w', pady=(10, 2))
    title = ttk.Entry(body)
    title.insert(0, data['title'])
    title.pack(fill='x', pady=(0, 8))
    return _confirm(window, body, 'Thêm bộ đề', title.get, title)
