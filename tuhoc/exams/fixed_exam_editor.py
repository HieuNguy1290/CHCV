"""Visual editor for the ordered sections and questions of a fixed exam."""

import copy
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from tuhoc.exams.exam_bank import SUBJECTS
from tuhoc.ui.ui_tokens import COLORS, font_at
from tuhoc.ui.ui_components import Tooltip


FIELDS = {
    'options': 'Lựa chọn · mỗi dòng một mục',
    'answer': 'Đáp án đúng',
    'wrong': 'Từ hoặc cụm từ sai',
    'corrected': 'Nội dung đã sửa',
    'image': 'Ảnh minh họa',
    'audio': 'File nghe',
    'gap_answers': 'Đáp án từng ô · mỗi dòng một đáp án',
    'sequence': 'Mỗi dòng một mục · nhập theo thứ tự đúng',
    'pairs': 'Mỗi dòng một cặp · trái | phải',
}
TYPES = {
    'choice': ('Chọn một đáp án', 'options', 'answer'),
    'true_false': ('Đúng / Sai', 'options', 'answer'),
    'fill': ('Nhập đáp án', 'answer'),
    'error': ('Tìm và sửa lỗi', 'wrong', 'corrected'),
    'picture_choice': ('Nhìn hình và chọn', 'options', 'answer', 'image'),
    'image_multi_choice': ('Chọn ảnh', 'options', 'answer'),
    'picture_missing_letters': ('Nhìn hình và điền chữ', 'answer', 'image'),
    'listening_choice': ('Nghe và chọn', 'options', 'answer', 'audio', 'image'),
    'listening_fill': ('Nghe và điền', 'answer', 'audio', 'image'),
    'sentence_gaps': ('Điền ô trong câu', 'gap_answers'),
    'conversation_gaps': ('Điền ô hội thoại', 'gap_answers'),
    'passage_gaps': ('Điền ô trong đoạn', 'gap_answers'),
    'order': ('Sắp xếp', 'sequence'),
    'matching': ('Nối cặp', 'pairs'),
}
LIST_FIELDS = {'options', 'gap_answers', 'sequence', 'pairs'}
MEDIA_FIELDS = {'image', 'audio'}


def textbox(parent, height, size=12):
    return ScrolledText(parent, wrap='word', height=height, undo=True, font=font_at(size),
                        padx=12, pady=8, spacing1=2, spacing3=5,
                        bg=COLORS['surface'], fg=COLORS['text'], insertbackground=COLORS['text'],
                        selectbackground=COLORS['primary'], selectforeground='white')


def text_of(widget):
    return widget.get('1.0', 'end-1c')


def set_text(widget, value):
    widget.delete('1.0', 'end')
    widget.insert('1.0', value)
    widget.edit_reset()


def icon_button(parent, icon, label, command):
    button = ttk.Button(parent, text=icon, width=3, style='FixedExam.Icon.TButton', command=command)
    Tooltip(button, label)
    return button


def toggle_maximize(window):
    try:
        window.state('normal' if window.state() == 'zoomed' else 'zoomed')
    except tk.TclError:
        try:
            window.attributes('-zoomed', not bool(window.attributes('-zoomed')))
        except tk.TclError:
            geometry = getattr(window, '_restored_geometry', None)
            if geometry:
                window.geometry(geometry)
                window._restored_geometry = None
            else:
                window._restored_geometry = window.geometry()
                window.geometry(f'{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0')
    return 'break'


class FixedExamEditor(tk.Toplevel):
    def __init__(self, app, store, example, published, preview, refresh):
        super().__init__(app)
        self.store, self.example, self.preview, self.refresh = store, example, preview, refresh
        self.title('Soạn bộ đề')
        self.geometry(f'{min(1100, self.winfo_screenwidth()-24)}x{min(760, self.winfo_screenheight()-85)}')
        self.minsize(760, 530)
        self.bind('<F11>', lambda _e:toggle_maximize(self))
        ttk.Style(self).configure('FixedExam.Icon.TButton', font=('Segoe UI Symbol', 14), padding=6)
        self.section_index = self.question_index = None
        self.fields = {}
        self._build()
        self.protocol('WM_DELETE_WINDOW', self._close)
        try:
            draft = published if published is not None else store.read_draft()
            self._load(json.loads(draft) if isinstance(draft, str) and draft else draft or example)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self._load(example)
            self.status.set(f'Không mở được bản nháp. {exc}')

    def _build(self):
        header = ttk.Frame(self, padding=12)
        header.pack(fill='x')
        self.name, self.minutes, self.subject = (tk.StringVar(self) for _ in range(3))
        ttk.Label(header, text='Tên bộ đề').pack(side='left', padx=(0,8))
        icon_button(header,'□','Phóng to hoặc khôi phục (F11)',lambda:toggle_maximize(self)).pack(side='right',padx=(8,0))
        ttk.Combobox(header, values=tuple(SUBJECTS.values()), textvariable=self.subject,
                     state='readonly', width=12).pack(side='right')
        ttk.Spinbox(header, from_=1, to=240, width=5, textvariable=self.minutes).pack(side='right', padx=(5,12))
        ttk.Label(header, text='Phút').pack(side='right', padx=(12,0))
        ttk.Entry(header, textvariable=self.name).pack(side='left', fill='x', expand=True)

        main = ttk.Panedwindow(self, orient='horizontal')
        main.pack(fill='both', expand=True, padx=12)
        rail = ttk.Frame(main, padding=(0,0,8,0))
        main.add(rail, weight=0)
        notebook = ttk.Notebook(main)
        main.add(notebook, weight=1)
        self.section_list = self._list(rail, 'Các phần', True)

        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text='Đoạn văn')
        row = ttk.Frame(tab)
        row.pack(fill='x', pady=(0,8))
        self.section_title = tk.StringVar(self)
        ttk.Label(row, text='Tên phần').pack(side='left', padx=(0,7))
        icon_button(row,'⤢','Mở rộng đoạn văn',self._expand).pack(side='right', padx=(7,0))
        section_name = ttk.Entry(row, textvariable=self.section_title)
        section_name.pack(side='left', fill='x', expand=True)
        section_name.bind('<FocusOut>', self._rename_section)
        self.passage = textbox(tab, 14)
        self.passage.pack(fill='both', expand=True)
        self.count = ttk.Label(tab)
        self.count.pack(anchor='e', pady=(5,0))
        self.passage.bind('<<Modified>>', self._word_count)

        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text='Câu hỏi')
        questions = ttk.Frame(tab)
        questions.pack(side='left', fill='y', padx=(0,10))
        self.question_list = self._list(questions, 'Các câu', False)
        body = ttk.Frame(tab)
        body.pack(side='left', fill='both', expand=True)
        self.kind = tk.StringVar(self)
        picker = ttk.Combobox(body, values=tuple(spec[0] for spec in TYPES.values()),
                              textvariable=self.kind, state='readonly')
        picker.pack(fill='x', pady=(0,8))
        picker.bind('<<ComboboxSelected>>', self._change_type)
        scroll_area = ttk.Frame(body)
        scroll_area.pack(fill='both', expand=True)
        self.form_canvas = tk.Canvas(scroll_area, width=1, height=1, highlightthickness=0,
                                     bg=COLORS['surface'], yscrollincrement=20)
        bar = ttk.Scrollbar(scroll_area, command=self.form_canvas.yview)
        bar.pack(side='right', fill='y')
        self.form_canvas.configure(yscrollcommand=bar.set)
        self.form_canvas.pack(side='left', fill='both', expand=True)
        self.form = ttk.Frame(self.form_canvas)
        window = self.form_canvas.create_window(0, 0, window=self.form, anchor='nw')
        self.form.bind('<Configure>', lambda _e:self.form_canvas.configure(scrollregion=self.form_canvas.bbox('all')))
        self.form_canvas.bind('<Configure>', lambda e:self.form_canvas.itemconfigure(window,width=e.width))
        for target in (self.form_canvas,self.form):
            self._bind_form_scroll(target)

        self.status = tk.StringVar(self)
        ttk.Label(self, textvariable=self.status, wraplength=730).pack(anchor='w', padx=12, pady=6)
        footer = ttk.Frame(self, padding=(12,0,12,10))
        footer.pack(fill='x')
        for icon, label, fn in (('📂','Nhập bộ đề JSON',self._import), ('▤','Dùng đề mẫu',self._use_example),
                                ('💾','Lưu nháp (Ctrl+S)',self._save), ('▶','Xem trước (F5)',self._preview),
                                ('⤒','Phát hành bộ đề',self._publish)):
            icon_button(footer,icon,label,lambda action=fn:self._safe(action)).pack(side='left',padx=(0,6))
        self.bind('<Control-s>',lambda _e:self._safe(self._save))
        self.bind('<F5>',lambda _e:self._safe(self._preview))

    def _list(self, parent, title, section):
        ttk.Label(parent, text=title, font=font_at(12, 'bold')).pack(anchor='w')
        row = ttk.Frame(parent)
        row.pack(fill='both', expand=True, pady=6)
        box = tk.Listbox(row, width=18, exportselection=False, font=font_at(11),
                         bg=COLORS['surface'], fg=COLORS['text'],
                         selectbackground=COLORS['primary'], selectforeground='white')
        bar = ttk.Scrollbar(row, command=box.yview)
        box.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y')
        box.pack(fill='both', expand=True)
        box.bind('<<ListboxSelect>>', lambda _e: self._select(box, section))
        controls = ttk.Frame(parent)
        controls.pack(fill='x')
        item='phần' if section else 'câu hỏi'
        for icon,label,action in (('+',f'Thêm {item}','add'),('−',f'Xóa {item}','remove'),
                                  ('↑',f'Đưa {item} lên',-1),('↓',f'Đưa {item} xuống',1)):
            icon_button(controls,icon,label,lambda op=action:self._edit_list(section,op)).pack(side='left')
        return box

    def _load(self, data):
        if not isinstance(data, dict) or not isinstance(data.get('sections'), list):
            raise ValueError('Bộ đề cần danh sách các phần.')
        for section in data['sections']:
            if not isinstance(section, dict) or not isinstance(section.get('questions'), list):
                raise ValueError('Mỗi phần cần danh sách câu hỏi.')
            if any(not isinstance(q, dict) or q.get('type', 'choice') not in TYPES for q in section['questions']):
                raise ValueError('Bộ đề có dạng câu chưa hỗ trợ.')
        self.model = copy.deepcopy(data)
        for section in self.model['sections']:
            for question in section['questions']:
                question.setdefault('type', 'choice')
        self.name.set(data.get('title', ''))
        self.minutes.set(data.get('minutes', 60))
        self.subject.set(SUBJECTS.get(data.get('subject'), SUBJECTS['tieng_anh']))
        self._open_section(0 if self.model['sections'] else None)
        self.saved = self._data()

    def _section(self):
        return self.model['sections'][self.section_index] if self.section_index is not None else None

    def _question(self):
        return self._section()['questions'][self.question_index] if self.question_index is not None else None

    def _commit(self):
        section = self._section()
        if section is None:
            return
        section.update(title=self.section_title.get(), passage=text_of(self.passage))
        question = self._question()
        if question is None:
            return
        for key, widget in self.fields.items():
            value = text_of(widget) if isinstance(widget, tk.Text) else widget.get()
            if key in LIST_FIELDS:
                value = [line.strip() for line in value.splitlines() if line.strip()]
                if key == 'pairs':
                    value = [[part.strip() for part in line.split('|', 1)] for line in value]
            question[key] = value
        if question.get('type') == 'matching':
            question['matching_mode'] = 'Chữ ↔ Chữ'

    def _data(self):
        self._commit()
        raw = self.minutes.get().strip()
        subject = next(key for key, label in SUBJECTS.items() if label == self.subject.get())
        self.model.update(title=self.name.get(), minutes=int(raw) if raw.isdecimal() else raw, subject=subject)
        return copy.deepcopy(self.model)

    @staticmethod
    def _populate(box, labels, index):
        box.delete(0, 'end')
        for label in labels:
            box.insert('end', label)
        if index is not None:
            box.selection_set(index)
            box.see(index)

    def _section_labels(self):
        return [s.get('title') or f'Phần {i+1}' for i,s in enumerate(self.model['sections'])]

    def _rename_section(self, _event):
        section = self._section()
        if section is not None and section.get('title') != self.section_title.get():
            section['title'] = self.section_title.get()
            index = self.section_index
            self.section_list.delete(index)
            self.section_list.insert(index, self._section_labels()[index])
            self.section_list.selection_set(index)

    def _open_section(self, index):
        self.section_index = index
        section = self._section()
        self.section_title.set(section.get('title', '') if section else '')
        set_text(self.passage, section.get('passage', '') if section else '')
        self._word_count()
        self._populate(self.section_list, self._section_labels(), index)
        self._open_question(0 if section and section['questions'] else None)

    def _open_question(self, index):
        self.question_index = index
        section = self._section()
        before = sum(len(s['questions']) for s in self.model['sections'][:self.section_index])
        rows = section['questions'] if section else []
        labels = [f'{before+i+1}. {" ".join(str(q.get("prompt", "")).split())[:28]}' for i,q in enumerate(rows)]
        self._populate(self.question_list, labels, index)
        q = self._question()
        self.kind.set(TYPES[q.get('type', 'choice')][0] if q is not None else '')
        self._draw_question()

    def _items(self, sections):
        if sections:
            return self.model['sections'], self.section_index, self._open_section
        section = self._section()
        return section['questions'] if section else None, self.question_index, self._open_question

    def _select(self, box, sections):
        selected = box.curselection()
        _, current, show = self._items(sections)
        if selected and selected[0] != current:
            self._commit()
            show(selected[0])

    def _edit_list(self, sections, action):
        items, index, show = self._items(sections)
        if items is None:
            return
        self._commit()
        if action == 'add':
            items.append({'title': f'Phần {len(items)+1}', 'passage': '', 'questions': []}
                         if sections else {'type': 'choice', 'prompt': '', 'options': [], 'answer': ''})
            show(len(items)-1)
        elif index is not None and action == 'remove':
            target = 'phần này và các câu bên trong' if sections else 'câu này'
            if messagebox.askyesno('Xác nhận', f'Xóa {target}?', parent=self):
                items.pop(index)
                show(min(index,len(items)-1) if items else None)
        elif index is not None and isinstance(action, int) and 0 <= index+action < len(items):
            items[index], items[index+action] = items[index+action], items[index]
            show(index+action)

    def _change_type(self, _event=None):
        q = self._question()
        if q is None:
            self.kind.set('')
            return
        self._commit()
        kind = next(key for key, spec in TYPES.items() if spec[0] == self.kind.get())
        q['type'] = kind
        self._draw_question()

    def _draw_question(self):
        for widget in self.form.winfo_children():
            widget.destroy()
        self.fields.clear()
        self.form_canvas.yview_moveto(0)
        q = self._question()
        if q is None:
            ttk.Label(self.form, text='Chọn hoặc thêm câu hỏi.').pack(anchor='w')
            return
        kind = q.get('type', 'choice')
        for key in ('prompt', *TYPES[kind][1:]):
            row = ttk.Frame(self.form)
            row.pack(fill='x')
            label = FIELDS.get(key, 'Nội dung câu hỏi')
            if key == 'prompt' and 'gap_answers' in TYPES[kind]:
                label += ' · dùng {1}, {2}, … cho ô trống'
            if kind == 'image_multi_choice' and key == 'options':
                label = 'Các ảnh lựa chọn · mỗi đường dẫn một dòng'
            ttk.Label(row, text=label).pack(side='left')
            value = q.get(key, '')
            if key == 'prompt' or key in LIST_FIELDS:
                control = textbox(self.form, 3)
                if key == 'pairs':
                    value = '\n'.join(' | '.join(pair) for pair in value)
                elif key in LIST_FIELDS:
                    value = '\n'.join(value)
                set_text(control, value)
                control.pack(fill='both', expand=True, pady=(3,7))
            else:
                control = ttk.Entry(self.form)
                control.insert(0, value)
                control.pack(fill='x', pady=(3,7))
            if key in MEDIA_FIELDS or (kind == 'image_multi_choice' and key in ('options', 'answer')):
                icon_button(row,'📂','Chọn tệp',lambda w=control:self._choose_media(w)).pack(side='right')
            self.fields[key] = control
            for widget in (control,row,*row.winfo_children()):
                self._bind_form_scroll(widget)
            control.bind('<FocusIn>',lambda _e,w=control:self._reveal_form_control(w),add='+')
            if isinstance(control, ScrolledText):
                self._bind_form_scroll(control.frame)

    def _bind_form_scroll(self, widget):
        for sequence in ('<MouseWheel>','<Button-4>','<Button-5>'):
            widget.bind(sequence,self._scroll_form,add='+')

    def _scroll_form(self,event):
        direction=-1 if getattr(event,'num',None)==4 or event.delta>0 else 1
        if isinstance(event.widget,tk.Text):
            start,end=event.widget.yview()
            if (direction<0 and start>0) or (direction>0 and end<1):
                return None
        self.form_canvas.yview_scroll(direction*3,'units')
        return 'break'

    def _reveal_form_control(self, widget):
        canvas=self.form_canvas
        bounds=canvas.bbox('all')
        if not bounds:
            return
        top=widget.winfo_rooty()-self.form.winfo_rooty()
        edge=canvas.canvasy(0)
        height=canvas.winfo_height()
        if top<edge:
            canvas.yview_moveto(top/max(1,bounds[3]))
        elif top+widget.winfo_height()>edge+height:
            canvas.yview_moveto(max(top-8,0)/max(1,bounds[3]))

    def _choose_media(self, widget):
        if isinstance(widget, tk.Text):
            paths = filedialog.askopenfilenames(parent=self)
            if paths:
                widget.insert('end', ('\n' if text_of(widget) else '') + '\n'.join(paths))
        else:
            path = filedialog.askopenfilename(parent=self)
            if path:
                widget.delete(0, 'end')
                widget.insert(0, path)

    def _word_count(self, _event=None):
        if self.passage.edit_modified():
            self.passage.edit_modified(False)
        self.count.configure(text=f'{len(text_of(self.passage).split())} từ')

    def _expand(self):
        if self._section() is None:
            return
        window = tk.Toplevel(self)
        window.title(self.section_title.get() or 'Đoạn văn')
        window.bind('<F11>',lambda _e:toggle_maximize(window))
        window.geometry(f'{min(1080, self.winfo_screenwidth()-24)}x{min(780, self.winfo_screenheight()-80)}')
        editor = textbox(window, 20, 14)
        editor.configure(padx=24, pady=14)
        set_text(editor, text_of(self.passage))
        editor.pack(fill='both', expand=True, padx=12, pady=12)
        def apply():
            set_text(self.passage, text_of(editor))
            self._word_count()
            window.destroy()
        tools=ttk.Frame(window,padding=(12,0,12,12))
        tools.pack(fill='x')
        icon_button(tools,'✓','Áp dụng đoạn văn',apply).pack(side='right')
        icon_button(tools,'□','Phóng to hoặc khôi phục (F11)',lambda:toggle_maximize(window)).pack(side='right',padx=8)
        window.grab_set()
        editor.focus_set()

    def _safe(self, action):
        try:
            action()
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self.status.set(str(exc))

    def _confirm_replace(self):
        return self._data() == self.saved or messagebox.askyesno(
            'Xác nhận', 'Bỏ các thay đổi chưa lưu?', parent=self)

    def _use_example(self):
        if self._confirm_replace():
            self._load(self.example)

    def _import(self):
        path = filedialog.askopenfilename(parent=self, filetypes=[('Bộ đề JSON', '*.json')])
        if not path or not self._confirm_replace():
            return
        source = Path(path)
        data = json.loads(source.read_text(encoding='utf-8-sig'))
        for section in data['sections']:
            for q in section['questions']:
                images = q.get('type') == 'image_multi_choice'
                for key in MEDIA_FIELDS | ({'answer'} if images else set()):
                    if q.get(key):
                        q[key] = str((source.parent / q[key]).resolve())
                if images:
                    q['options'] = [str((source.parent / p).resolve()) for p in q['options']]
        self._load(data)

    def _save(self):
        data = self._data()
        self.store.save_draft(data)
        self.saved = data
        self.status.set('Đã lưu nháp.')

    def _preview(self):
        self.preview(self._data(), True)

    def _publish(self):
        data = self._data()
        result = self.store.publish(data)
        self.saved = data
        self.status.set(f'Đã phát hành {result["title"]}.')
        self.refresh()

    def _close(self):
        if self._confirm_replace():
            self.destroy()
