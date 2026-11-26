"""Edit all existing curriculum blocks for a selected theme/level/lesson.

Keeps the existing level_blocks.json row schema and unrelated records intact.
"""
import copy
import hashlib
import json
import shutil
import tkinter as tk
import tkinter.font as tkfont
from tkinter import colorchooser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from tuhoc.lessons import image_children as ic
from tuhoc.lessons.level_flow import library_file, load_rows
from tuhoc.storage.safe_storage import commit_json
from tuhoc.lessons.lesson_display_names import breadcrumb
from tuhoc.studio.studio_list import find_rows, remove_at
from tuhoc.ui.ui_components import Toast


def open_block_editor(app, theme, level, lesson=1, create_mode=False):
    data_dir = app.curriculum.data_dir
    level, lesson = int(level), int(lesson or 1)
    path = library_file(data_dir, 'blocks')
    original = load_rows(data_dir, 'blocks', None)
    def matches(row):
        return (str(row.get('theme', '')) == str(theme) and
                int(row.get('level') or 0) == level and
                int(row.get('lesson') or 1) == lesson)
    selected = [copy.deepcopy(row) for row in original if matches(row)]
    selected.sort(key=lambda row: int(row.get('order') or 0))
    blocks = selected
    if create_mode and selected:
        messagebox.showwarning('Đã có nội dung', 'Bài học đã có block. Hãy mở từ danh sách để sửa.')
        return None
    window = tk.Toplevel(app)
    window.title(f'{"Tạo" if create_mode else "Sửa"} bài học · {breadcrumb(data_dir, theme, level, lesson)}')
    # Start maximized on Windows; use screen-sized geometry on other systems.
    try:
        window.state('zoomed')
    except tk.TclError:
        window.geometry(f'{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0')
    window.minsize(780, 530)
    window.configure(bg='#F5F8F5')
    # A maximized child must not be repositioned relative to its owner.
    # On Windows, zoomed uses the work area (excludes taskbar).
    window.grab_set()
    active = {'index': 0 if blocks else None}
    dirty = {'value': False}
    updating = {'value': False}

    heading = tk.Frame(window, bg='#244D3B', padx=16, pady=12)
    heading.pack(fill='x')
    tk.Label(heading, text=breadcrumb(data_dir, theme, level, lesson),
             bg='#244D3B', fg='white', font=('Segoe UI', 15, 'bold')).pack(anchor='w')
    tk.Label(heading, text='Mỗi block gồm: Giới thiệu (title) · Hình ảnh (image) · Nội dung chính (content)',
             bg='#244D3B', fg='#D6E8DB').pack(anchor='w')
    main = tk.Frame(window, bg='#F5F8F5', padx=12, pady=12)
    main.pack(fill='both', expand=True)
    left = tk.Frame(main, bg='white', padx=10, pady=10, width=330)
    left.pack(side='left', fill='y', padx=(0, 12))
    left.pack_propagate(False)
    tk.Label(left, text='DANH SÁCH BLOCK', bg='white', fg='#244D3B',
             font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
    search=tk.StringVar()
    tk.Label(left,text='Tìm tên hoặc nội dung',bg='white').pack(anchor='w')
    ttk.Entry(left,textvariable=search).pack(fill='x',pady=(0,6))
    sort=tk.StringVar(value='Thứ tự bài')
    ttk.Combobox(left,textvariable=sort,values=('Thứ tự bài','Tiêu đề'),
                 state='readonly').pack(fill='x',pady=(0,6))
    visible=[]
    listbox = tk.Listbox(left, font=('Segoe UI', 11), exportselection=False, activestyle='none')
    listbox.pack(fill='both', expand=True)
    right = tk.Frame(main, bg='white', padx=18, pady=12)
    right.pack(side='left', fill='both', expand=True)
    title_var = tk.StringVar()
    image_var = tk.StringVar()
    layout_var = tk.StringVar(value='auto')
    layout_row = tk.Frame(right, bg='white')
    layout_row.pack(fill='x', pady=(0, 10))
    tk.Label(layout_row, text='BỐ CỤC HIỂN THỊ', bg='white', fg='#244D3B',
             font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 12))
    layout_combo = ttk.Combobox(layout_row, textvariable=layout_var, state='readonly',
        values=('auto', 'image_wrap_left', 'image_children', 'legacy'))
    layout_combo.pack(side='left', fill='x', expand=True)
    tk.Label(layout_row, text='auto = bài cũ · image_wrap_left = chữ ôm ảnh · image_children = Hình + nội dung',
             bg='white', fg='#526C59').pack(side='left', padx=(8, 0))
    tk.Label(right, text='GIỚI THIỆU / TIÊU ĐỀ BLOCK', bg='white', fg='#244D3B',
             font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(4, 5))
    title_entry = ttk.Entry(right, textvariable=title_var, font=('Segoe UI', 12))
    title_entry.pack(fill='x', pady=(0, 16))
    tk.Label(right, text='HÌNH ẢNH MINH HỌA', bg='white', fg='#244D3B',
             font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
    image_row = tk.Frame(right, bg='white')
    image_row.pack(fill='x', pady=(0, 16))
    ttk.Entry(image_row, textvariable=image_var).pack(side='left', fill='x', expand=True)
    content_label = tk.Label(right, text='NỘI DUNG CHÍNH', bg='white', fg='#244D3B',
                             font=('Segoe UI', 10, 'bold'))
    content_label.pack(anchor='w', pady=(0, 5))
    content = tk.Text(right, font=('Segoe UI', 12), wrap='word', undo=True)
    content.pack(fill='both', expand=True)
    scrollbar = ttk.Scrollbar(content, orient='vertical', command=content.yview)
    scrollbar.pack(side='right', fill='y')
    content.configure(yscrollcommand=scrollbar.set)
    # --- Bố cục "Hình + nội dung": quản lý các mục con (chỉ hiện khi chọn image_children).
    children_frame = tk.Frame(right, bg='white')
    child_title_var = tk.StringVar()
    child_font_var = tk.StringVar()
    child_bold, child_italic, child_underline = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
    child_state = {'index': None, 'drag': None}
    child_history = ic.ChildHistory()
    tk.Label(children_frame, text='CÁC MỤC (kéo để đổi thứ tự)', bg='white', fg='#244D3B',
             font=('Segoe UI', 10, 'bold')).pack(anchor='w')
    child_list = tk.Listbox(children_frame, height=5, exportselection=False, activestyle='none',
                            font=('Segoe UI', 11))
    child_list.pack(fill='x', pady=(4, 6))
    child_actions = tk.Frame(children_frame, bg='white')
    child_actions.pack(fill='x', pady=(0, 8))
    for label, fn in [('+ Thêm mục', lambda: add_child()), ('Nhân bản mục', lambda: dup_child()),
                      ('Xóa mục', lambda: remove_child()), ('Hoàn tác', lambda: undo_children())]:
        ttk.Button(child_actions, text=label, command=fn).pack(side='left', padx=(0, 6))
    tk.Label(children_frame, text='TIÊU ĐỀ MỤC', bg='white', fg='#244D3B',
             font=('Segoe UI', 10, 'bold')).pack(anchor='w')
    child_title_entry = ttk.Entry(children_frame, textvariable=child_title_var, font=('Segoe UI', 12))
    child_title_entry.pack(fill='x', pady=(2, 8))
    format_row = tk.Frame(children_frame, bg='white')
    format_row.pack(fill='x', pady=(0, 6))
    tk.Label(format_row, text='Font', bg='white').pack(side='left')
    child_font_combo = ttk.Combobox(format_row, textvariable=child_font_var, values=ic.FONT_CHOICES, width=16)
    child_font_combo.pack(side='left', padx=(4, 12))
    for label, var in (('Đậm', child_bold), ('Nghiêng', child_italic), ('Gạch chân', child_underline)):
        tk.Checkbutton(format_row, text=label, variable=var, bg='white',
                       command=lambda: flush_child()).pack(side='left', padx=(0, 8))
    child_size_var = tk.StringVar(value='0')
    child_color_var = tk.StringVar(value='')
    tk.Label(format_row, text='Cỡ (0 = mặc định)', bg='white').pack(side='left', padx=(8, 2))
    child_size_spin = ttk.Spinbox(format_row, from_=0, to=96, width=4, textvariable=child_size_var,
                                  command=lambda: flush_child())
    child_size_spin.pack(side='left')
    child_size_spin.bind('<KeyRelease>', lambda _e: flush_child())
    child_color_btn = tk.Button(format_row, text='Màu chữ', relief='groove', command=lambda: pick_child_color())
    child_color_btn.pack(side='left', padx=(10, 2))
    ttk.Button(format_row, text='Mặc định', command=lambda: reset_child_color()).pack(side='left')
    child_text = tk.Text(children_frame, font=('Segoe UI', 12), wrap='word', undo=True, height=8)
    child_text.pack(fill='both', expand=True)
    child_font_combo.bind('<<ComboboxSelected>>', lambda _e: flush_child())
    child_title_entry.bind('<KeyRelease>', lambda _e: flush_child())
    child_text.bind('<KeyRelease>', lambda _e: flush_child())
    status = tk.StringVar(value=f'Đã nạp {len(blocks)} block từ JSON.')

    def refresh_list():
        listbox.delete(0, 'end')
        visible[:]=find_rows(blocks,search.get(),fields=('title','content'),
                             sort_by='title' if sort.get()=='Tiêu đề' else None)
        for i,block in visible:
            listbox.insert('end',f'#{i+1}  {str(block.get("title",""))[:42] or "(Chưa có giới thiệu)"}')
        indices=[i for i,_row in visible]
        if active['index'] in indices:
            index=indices.index(active['index'])
            listbox.selection_set(index)
            listbox.see(index)
        status.set(f'{len(blocks)} block · ' + ('Có thay đổi chưa lưu' if dirty['value'] else 'Chưa có thay đổi'))

    def flush():
        i = active['index']
        if updating['value'] or i is None or i >= len(blocks):
            return
        block = blocks[i]
        fields = [('title', title_var.get()), ('image', image_var.get())]
        if not ic.is_image_children(block):      # hidden for Hình + nội dung blocks
            fields.append(('content', content.get('1.0', 'end-1c')))
        for key, value in fields:
            if block.get(key, '') != value:
                block[key] = value
                dirty['value'] = True
        flush_child()
        layout = layout_var.get()
        previous = str(block.get('layout') or 'auto')
        if layout != previous:
            if layout == ic.LAYOUT:
                if block.get('children'):        # switching back: keep existing children
                    block['layout'] = layout
                    ic.ensure_block_id(block)
                    block['children'] = ic.normalize_children(block)
                else:                            # old description -> first child, image kept
                    blocks[i] = ic.migrate_legacy_block({**block, 'layout': previous})
            else:
                if previous == ic.LAYOUT:
                    block['content'] = ic.flatten_for_legacy(block)['content']
                if layout == 'auto':
                    block.pop('layout', None)
                else:
                    block['layout'] = layout
            dirty['value'] = True
            show(i)
            return
        refresh_list()

    def show(i):
        updating['value'] = True
        active['index'] = i
        block = blocks[i] if i is not None and i < len(blocks) else {}
        title_var.set(str(block.get('title', '')))
        image_var.set(str(block.get('image', '')))
        layout_var.set(str(block.get('layout') or 'auto'))
        content.configure(state='normal')
        content.delete('1.0', 'end')
        content.insert('1.0', str(block.get('content', '')))
        state = 'normal' if i is not None else 'disabled'
        title_entry.configure(state=state)
        content.configure(state=state)
        updating['value'] = False
        child_state['index'] = 0
        child_history.clear()
        refresh_layout_panel()
        refresh_list()

    def select(_event=None):
        selection = listbox.curselection()
        if selection:
            index=visible[selection[0]][0]
            if index!=active['index']:
                flush()
                show(index)
    listbox.bind('<<ListboxSelect>>', select)
    search.trace_add('write',lambda *_args:refresh_list())
    sort.trace_add('write',lambda *_args:refresh_list())

    def add():
        flush()
        block = {'theme': theme, 'level': level, 'lesson': lesson,
                 'order': len(blocks) + 1, 'title': '', 'image': '', 'content': '', 'layout': 'image_wrap_left'}
        blocks.append(block)
        dirty['value'] = True
        show(len(blocks) - 1)

    def duplicate():
        flush()
        i = active['index']
        if i is None: return
        clone = copy.deepcopy(blocks[i])
        clone.pop('id', None)  # Never duplicate an existing explicit ID.
        if ic.is_image_children(clone):
            clone.pop('block_id', None)
            ic.ensure_block_id(clone)
        blocks.insert(i + 1, clone)
        dirty['value'] = True
        show(i + 1)

    def move(delta):
        flush()
        i = active['index']
        if i is None or not 0 <= i + delta < len(blocks): return
        blocks[i], blocks[i + delta] = blocks[i + delta], blocks[i]
        dirty['value'] = True
        show(i + delta)

    def remove():
        i = active['index']
        if i is None or not messagebox.askyesno('Xóa block', 'Xóa block này khỏi bài học?', parent=window): return
        flush()
        remaining,ticket=remove_at(blocks,i)
        blocks[:]=remaining
        dirty['value']=True
        show(min(i,len(blocks)-1) if blocks else None)
        def restore():
            flush()
            blocks[:]=ticket.restore(blocks)
            dirty['value']=True
            show(min(i,len(blocks)-1))
        Toast(window,'Đã xóa block.',duration=6000,action=('Hoàn tác',restore))

    def add_children_block():
        flush()
        block = {'theme': theme, 'level': level, 'lesson': lesson, 'order': len(blocks) + 1,
                 'title': '', 'image': '', 'content': '', 'layout': ic.LAYOUT,
                 'children': [ic.make_child()]}
        ic.ensure_block_id(block)
        blocks.append(block)
        dirty['value'] = True
        show(len(blocks) - 1)

    def current_block():
        i = active['index']
        return blocks[i] if i is not None and i < len(blocks) else None

    def child_font_object():
        size = ic.clean_format({'size': child_size_var.get()})['size']
        return tkfont.Font(family=child_font_var.get() or 'Segoe UI', size=min(36, size) if size else 12,
                           weight='bold' if child_bold.get() else 'normal',
                           slant='italic' if child_italic.get() else 'roman',
                           underline=bool(child_underline.get()))

    def refresh_child_style():
        color = ic.clean_format({'color': child_color_var.get()})['color']
        child_text.configure(font=child_font_object(), fg=color or '#000000')
        child_color_btn.configure(bg=color or '#f0f0f0',
                                  fg='#ffffff' if color and sum(ic.parse_color(color)) < 380 else '#000000')

    def pick_child_color():
        chosen = colorchooser.askcolor(color=child_color_var.get() or '#000000', parent=window,
                                       title='Màu chữ nội dung')[1]
        if chosen:
            child_color_var.set(chosen)
            flush_child()

    def reset_child_color():
        child_color_var.set('')
        flush_child()

    def refresh_children(select=None):
        block = current_block()
        kids = (block.get('children') or []) if block else []
        child_list.delete(0, 'end')
        for n, kid in enumerate(kids, 1):
            child_list.insert('end', f'{n}.  {str(kid.get("title") or "(Chưa có tiêu đề)")[:48]}')
        if select is not None and kids:
            select = max(0, min(len(kids) - 1, select))
            child_list.selection_set(select)
            child_list.see(select)

    def show_child(j):
        block = current_block()
        kids = (block.get('children') or []) if block else []
        updating['value'] = True
        child_state['index'] = j if j is not None and 0 <= j < len(kids) else None
        kid = kids[child_state['index']] if child_state['index'] is not None else {}
        fmt = ic.clean_format(kid.get('format'))
        child_title_var.set(str(kid.get('title', '')))
        child_font_var.set(fmt['font'])
        child_bold.set(fmt['bold'])
        child_italic.set(fmt['italic'])
        child_underline.set(fmt['underline'])
        child_size_var.set(str(fmt['size']))
        child_color_var.set(fmt['color'])
        child_text.delete('1.0', 'end')
        child_text.insert('1.0', str(kid.get('content', '')))
        refresh_child_style()
        updating['value'] = False
        refresh_children(child_state['index'])

    def flush_child():
        block, j = current_block(), child_state['index']
        if updating['value'] or block is None or j is None or not ic.is_image_children(block):
            return
        kids = block.get('children') or []
        if j >= len(kids):
            return
        kid = kids[j]
        fmt = ic.clean_format({'font': child_font_var.get(), 'bold': child_bold.get(),
                               'italic': child_italic.get(), 'underline': child_underline.get(),
                               'size': child_size_var.get(), 'color': child_color_var.get()})
        changed = False
        for key, value in (('title', child_title_var.get()),
                           ('content', child_text.get('1.0', 'end-1c')), ('format', fmt)):
            if kid.get(key) != value:
                kid[key] = value
                changed = True
        refresh_child_style()
        if changed:
            dirty['value'] = True
            refresh_children(j)

    def change_children(builder):
        """Run a children edit with one undo snapshot; only the right list redraws."""
        block = current_block()
        if block is None or not ic.is_image_children(block):
            return
        flush_child()
        before = block.get('children') or []
        child_history.push(before)
        after, select = builder(list(before), child_state['index'] if child_state['index'] is not None else len(before) - 1)
        block['children'] = after
        dirty['value'] = True
        show_child(select)

    def add_child():
        def build(kids, j):
            kids.insert(j + 1, ic.make_child(taken={k['id'] for k in kids}))
            return kids, j + 1
        change_children(build)

    def dup_child():
        def build(kids, j):
            return (ic.duplicate_child(kids, j), j + 1) if kids else (kids, None)
        change_children(build)

    def remove_child():
        def build(kids, j):
            if len(kids) <= 1:
                messagebox.showinfo('Xóa mục', 'Block cần ít nhất một mục.', parent=window)
                return kids, j
            del kids[j]
            return kids, min(j, len(kids) - 1)
        change_children(build)

    def undo_children():
        block = current_block()
        if block is None or not ic.is_image_children(block):
            return
        flush_child()
        snapshot = child_history.undo()
        if snapshot is not None:
            block['children'] = snapshot
            dirty['value'] = True
            show_child(min(child_state['index'] or 0, len(snapshot) - 1))

    def child_select(_event=None):
        selection = child_list.curselection()
        if selection and selection[0] != child_state['index']:
            flush_child()
            show_child(selection[0])

    def child_press(event):
        child_state['drag'] = {'from': child_list.nearest(event.y), 'moved': False}

    def child_motion(event):
        drag, block = child_state['drag'], current_block()
        if not drag or block is None:
            return 'break'
        kids = block.get('children') or []
        target = child_list.nearest(event.y)
        if target == drag['from'] or not 0 <= target < len(kids) or not 0 <= drag['from'] < len(kids):
            return 'break'
        flush_child()
        if not drag['moved']:
            child_history.push(kids)             # one undo step for the whole drag
            drag['moved'] = True
        block['children'] = ic.move_child(kids, drag['from'], target)
        dirty['value'] = True
        drag['from'] = target
        show_child(target)                       # redraws the children list only
        return 'break'

    def child_release(_event):
        child_state['drag'] = None

    child_list.bind('<<ListboxSelect>>', child_select)
    child_list.bind('<ButtonPress-1>', child_press, add='+')
    child_list.bind('<B1-Motion>', child_motion)
    child_list.bind('<ButtonRelease-1>', child_release, add='+')

    def refresh_layout_panel():
        block = current_block()
        if block is not None and ic.is_image_children(block):
            content_label.pack_forget()
            content.pack_forget()
            children_frame.pack(fill='both', expand=True)
            show_child(child_state['index'] or 0)
        else:
            children_frame.pack_forget()
            if not content.winfo_ismapped():
                content_label.pack(anchor='w', pady=(0, 5))
                content.pack(fill='both', expand=True)

    def preview():
        """Open the unsaved draft in the same Pygame screen students use."""
        flush()
        from tuhoc.lessons.pygame_lesson_window import available, launch
        if not available():
            messagebox.showerror('Thiếu pygame', 'Hãy cài pygame để xem trước.', parent=window)
            return
        draft = []
        for n, block in enumerate(blocks, 1):
            item = copy.deepcopy(block)
            item['order'] = n
            if ic.is_image_children(item):
                item['children'] = ic.normalize_children(item)
            if item.get('image'):
                item['image'] = app.media_file(item['image']) or item['image']
            draft.append(item)
        heading_text = breadcrumb(data_dir, theme, level, lesson)
        started = launch(heading_text, {'title': heading_text, 'instructions': ''}, draft,
                         data_dir, dict(getattr(app, '_display_settings', {}) or {}))
        if not started:
            messagebox.showinfo('Xem trước', 'Một cửa sổ Pygame khác đang mở.', parent=window)

    def choose_image():
        i = active['index']
        if i is None: return
        source_name = filedialog.askopenfilename(parent=window, title='Chọn ảnh',
                       filetypes=[('Hình ảnh', '*.png *.jpg *.jpeg *.gif'), ('Tất cả', '*.*')])
        if not source_name: return
        source = Path(source_name)
        target_dir = Path(data_dir) / 'content_library' / 'media'
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / source.name
            if target.exists() and target.read_bytes() != source.read_bytes():
                digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
                target = target_dir / f'{source.stem}_{digest}{source.suffix.lower()}'
            if not target.exists(): shutil.copy2(source, target)
            image_var.set('media/' + target.name)
            flush()
        except OSError as exc:
            messagebox.showerror('Không thể thêm ảnh', str(exc), parent=window)

    layout_combo.bind('<<ComboboxSelected>>', lambda _event: flush())
    ttk.Button(image_row, text='Chọn ảnh...', command=choose_image).pack(side='left', padx=(8, 0))
    actions = tk.Frame(left, bg='white')
    actions.pack(fill='x', pady=(10, 0))
    actions.columnconfigure((0, 1), weight=1, uniform='act')
    # (label, command, row, column, columnspan): two columns so every button stays visible.
    for label, fn, row, col, span in [
            ('+ Thêm block', add, 0, 0, 2), ('+ Block Hình + nội dung', add_children_block, 1, 0, 2),
            ('Nhân bản', duplicate, 2, 0, 1), ('Xóa block', remove, 2, 1, 1),
            ('Lên ↑', lambda: move(-1), 3, 0, 1), ('Xuống ↓', lambda: move(1), 3, 1, 1),
            ('Xem trước', preview, 4, 0, 2)]:
        ttk.Button(actions, text=label, command=fn).grid(
            row=row, column=col, columnspan=span, sticky='ew', padx=2, pady=2)

    def save():
        flush()
        if create_mode and not blocks:
            messagebox.showwarning('Chưa có block', 'Hãy thêm ít nhất một block trước khi tạo bài học.', parent=window)
            return
        if not blocks:
            if not messagebox.askyesno('Bài học trống', 'Lưu bài học không có block?', parent=window): return
        for number, block in enumerate(blocks, 1):
            if ic.is_image_children(block):
                block['children'] = ic.normalize_children(block)
                ic.ensure_block_id(block)
                problems = ic.validate_block(block)
                if problems:
                    messagebox.showwarning('Block Hình + nội dung', f'Block {number}: ' + ' '.join(problems), parent=window)
                    return
        from tuhoc.lessons.unified_subjects import subject_image
        missing=[str(block.get('title') or index) for index,block in enumerate(blocks,1)
                 if block.get('image') and not subject_image(data_dir,block['image'])]
        if missing:
            messagebox.showwarning('Thiếu ảnh','Kiểm tra ảnh của block: '+', '.join(missing),parent=window)
            return
        new_rows = []
        inserted = False
        for row in original:
            if matches(row):
                if not inserted:
                    for i, block in enumerate(blocks, 1):
                        item = copy.deepcopy(block)
                        item['order'] = i
                        item['theme'], item['level'], item['lesson'] = theme, level, lesson
                        new_rows.append(item)
                    inserted = True
                continue
            new_rows.append(row)
        if not inserted:
            for i, block in enumerate(blocks, 1):
                item = copy.deepcopy(block)
                item['order'] = i
                new_rows.append(item)
        try:
            changes = {path: new_rows}
            if create_mode:
                lessons_path = library_file(data_dir, 'lessons')
                lesson_rows = load_rows(data_dir, 'lessons', None)
                if any(matches(row) for row in lesson_rows):
                    messagebox.showerror('Bài học đã tồn tại', 'Bài học này đã được tạo. Không ghi đè.', parent=window)
                    return
                lesson_rows.append({'theme': theme, 'level': level, 'lesson': lesson,
                                    'title': blocks[0].get('title', '') or f'Lesson {lesson}',
                                    'instructions': '', 'content': '', 'image': ''})
                changes[lessons_path] = lesson_rows
            commit_json(changes)
            app.curriculum.reload()
        except (OSError, ValueError) as exc:
            messagebox.showerror('Không lưu được', str(exc), parent=window)
            return
        dirty['value'] = False
        messagebox.showinfo('Đã lưu', f'Đã lưu {len(blocks)} block theo thứ tự order.', parent=window)
        window.destroy()
        app.level_editor('lessons')

    def close():
        flush()
        if dirty['value'] and not messagebox.askyesno('Chưa lưu', 'Bỏ các thay đổi chưa lưu?', parent=window): return
        window.destroy()

    footer = tk.Frame(window, bg='#F5F8F5', padx=14, pady=10)
    footer.pack(fill='x')
    tk.Label(footer, textvariable=status, bg='#F5F8F5', fg='#426451').pack(side='left')
    ttk.Button(footer, text='Lưu toàn bộ block', command=save).pack(side='right', padx=5)
    ttk.Button(footer, text='Đóng', command=close).pack(side='right', padx=5)
    window.protocol('WM_DELETE_WINDOW', close)
    show(active['index'])
    if create_mode:
        add()
    return window
