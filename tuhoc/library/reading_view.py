"""Connect library articles to the existing interactive reader."""
import sqlite3
import tkinter as tk
import unicodedata
import webbrowser
from tkinter import messagebox, simpledialog, ttk
from time import monotonic

from tuhoc.library.audio import speak_article
from tuhoc.library.models import LibraryError
from tuhoc.lessons.pygame_embedded_reader import EmbeddedReader, available
from tuhoc.paths import PROJECT_ROOT
from tuhoc.ui.ui_components import Tooltip
from tuhoc.ui.ui_keys import keyboard_button
from tuhoc.ui.ui_motion import MotionJobs, ease_out_cubic
from tuhoc.ui.ui_tokens import DURATION


PALETTES = {
    'light': dict(page='#FAFBF8', panel='#EDF1ED', ink='#222D25', accent='#A0DBC2',
                  accent_ink='#152D23', selection='#326950', selection_ink='#FFFFFF', dark=False),
    'paper': dict(page='#F6EFDE', panel='#EDE3CF', ink='#302B22', accent='#A5D7BB',
                  accent_ink='#192E23', selection='#45664F', selection_ink='#FFFFFF', dark=False),
    'dark': dict(page='#171C19', panel='#252D28', ink='#E9E8DE', accent='#A0E1C3',
                 accent_ink='#172C23', selection='#386451', selection_ink='#F7F7EE', dark=True),
}
THEME_LABELS = {'light': 'Sáng', 'paper': 'Mặc định', 'dark': 'Tối'}
TOOL_LABELS = {'select': 'Chọn chữ', 'draw': 'Vẽ', 'highlight': 'Tô chữ',
               'underline': 'Gạch chân', 'textbox': 'Hộp chữ', 'fill': 'Tô vùng',
               'note': 'Ghi chú', 'erase': 'Tẩy', 'read': 'Cuộn', 'picture': 'Chèn ảnh'}
TOOL_ICON_DIR = PROJECT_ROOT / 'assets' / 'library_reader_tools'
TOOL_ROW_HEIGHT = 38
TOOL_RAIL_WIDTH = 42
TOOL_TOP_GAP = 18
PRIMARY_TOOLS = ('select', 'draw', 'color', 'clear', 'highlight', 'underline', 'erase',
                 'textbox', 'note', 'picture', 'undo', 'redo')
TOOL_RAIL_FINISH = {
    'light': ('#DCE6DE', '#FFFFFF', '#A6B6AC', '#85978C'),
    'paper': ('#DFD2B8', '#FFF8E9', '#B2A286', '#8E7C60'),
    'dark': ('#29352E', '#52655A', '#142019', '#0C110E'),
}


def glossary_key(text):
    return ' '.join(unicodedata.normalize('NFC', text).casefold().split())


class LibraryReader(EmbeddedReader):
    def __init__(self, page, item, image, **callbacks):
        self.page = page
        super().__init__(page, item, image, reading_palette=page.palette,
                         external_dock=True, **callbacks)
        self.set_tool_color('draw', '#668674')
        self._scroll_top = None
        self.canvas.configure(yscrollcommand=self.update_scrollbar)

    def update_scrollbar(self, first, last):
        self._scrollbar.set(first, last)
        if first != self._scroll_top:
            self._hide_selection_popup()
        self._scroll_top = first

    def _show_selection_popup(self):
        self._hide_selection_popup()
        text = self.selected_text()
        if not text or not self._selected_text_rects:
            return
        page = self.page
        page.close_panel()
        entry = page.glossary.get(glossary_key(text))
        popup = page.panel_frame(self.canvas)
        width = min(320, max(1, self.canvas.winfo_width() - 16))
        page.label(popup, entry['word'] if entry else text, bold=True, wrap=width - 24).pack(
            fill='x', padx=10, pady=(8, 2))
        if entry:
            page.label(popup, entry['meaning'], wrap=width - 24).pack(fill='x', padx=10, pady=(0, 6))
        actions = tk.Frame(popup, bg=page.palette['panel'])
        actions.pack(fill='x', padx=6, pady=(0, 6))
        page.flashcard_button(actions, text).pack(fill='x')
        row = tk.Frame(actions, bg=page.palette['panel'])
        row.pack(fill='x')
        for label, command in (('Phát âm', self.speak_selected_text),
                               ('Tô chữ', self.apply_text_highlight),
                               ('Sao chép', self.copy_selected_text)):
            page.button(row, label, command).pack(side='left', fill='x', expand=True)
        popup.update_idletasks()
        box = self._selected_text_rects[0]
        height = popup.winfo_reqheight()
        x = max(8, min(box[0], self.canvas.winfo_width() - width - 8))
        top = self.canvas.canvasy(0)
        y = box[3] - top + 8
        if y + height > self.canvas.winfo_height() - 8:
            y = box[1] - top - height - 8
        y = max(8, min(y, self.canvas.winfo_height() - height - 8))
        popup.place(x=x, y=y, width=width)
        self._selection_popup = popup

    def set_mode(self, mode):
        super().set_mode(mode)
        self.page.update_tool_state()

    def render(self):
        super().render()
        self.page.update_tool_state()


class ReadingPage(tk.Frame):
    def __init__(self, app, article, image, back, **callbacks):
        self.app = app
        self.article = article
        self.back = back
        self.glossary = {glossary_key(entry['word']): entry for entry in article['glossary']}
        self.saved_words = set()
        settings = app._display_settings.get('library_reading')
        self.settings = dict(settings) if isinstance(settings, dict) else {}
        theme = self.settings.get('theme')
        self.theme = theme if isinstance(theme, str) and theme in PALETTES else 'paper'
        self.palette = PALETTES[self.theme]
        super().__init__(app, bg=self.palette['page'])
        self.panel = None
        self.panel_name = None
        self.panel_controls = []
        self.mode_buttons = {}
        self.rail_buttons = {}
        self.tool_icons = {}
        self.tools_visible = True
        self.visible_tools = ()
        self.jobs = MotionJobs(self)
        self.expanded = False
        self.header = tk.Frame(self)
        self.header.pack(fill='x')
        self.center = tk.Label(self.header, text=article['title'], font=('Segoe UI', 11, 'bold'))
        self.center.place(relx=.5, rely=.5, anchor='center')
        self.back_button = self.button(self.header, '← Danh sách', back)
        self.back_button.pack(side='left', padx=12, pady=8)
        self.expand = self.button(self.header, '⤢ Mở rộng', self.set_expanded)
        self.expand.pack(side='right', padx=(4, 12), pady=8)
        self.aa = self.button(self.header, 'Aa', lambda: self.toggle_panel('appearance'))
        self.aa.pack(side='right', pady=8)
        self.footer = tk.Frame(self)
        self.footer.pack(side='bottom', fill='x')
        self.words = self.button(self.footer, 'Từ khó ▸', lambda: self.toggle_panel('glossary'))
        self.words.pack(side='right', padx=12, pady=8)
        item = {'title': article['title'], 'content': article['body'], 'image': article['image']}
        self.reader = LibraryReader(self, item, image, **callbacks)
        keyboard_button(self.reader._listen_button)
        self.reader._expand_reading_button = self.expand
        self.reader.zoom = self.number_setting('zoom', 1.0, .7, 1.7)
        self.reader.line_spacing = self.number_setting('spacing', 1.65, 1.35, 2.25)
        self.reader.pack(fill='both', expand=True, padx=TOOL_RAIL_WIDTH + 4)
        self.create_tool_rail()
        for bar in (self.header, self.footer):
            bar.bind('<Configure>', lambda event: self.layout_tool_rail(), add='+')
        self.reader.set_mode('select')
        self.reader.canvas.bind('<ButtonPress-1>', self.dismiss_panel, add='+')
        self.bind('<Configure>', self.on_resize, add='+')
        self.recolor()

    def number_setting(self, key, default, low, high):
        value = self.settings.get(key)
        return max(low, min(high, value)) if type(value) in (float, int) else default

    def button(self, parent, text, command, primary=False):
        widget = tk.Button(parent, text=text, command=command, font=('Segoe UI', 10),
                           relief='flat', bd=0, padx=8, pady=5, cursor='hand2')
        self.color_button(widget, primary)
        keyboard_button(widget)
        return widget

    def color_button(self, widget, primary=False):
        p = self.palette
        widget.configure(bg=p['accent'] if primary else p['panel'],
                         fg=p['accent_ink'] if primary else p['ink'],
                         activebackground=p['accent'], activeforeground=p['accent_ink'],
                         disabledforeground=p['ink'], highlightbackground=p['panel'],
                         highlightcolor=p['selection'])

    def tool_image(self, icon, light_ink):
        key = icon, light_ink
        if key not in self.tool_icons:
            from PIL import Image, ImageTk

            directory = TOOL_ICON_DIR / 'light_ink' if light_ink else TOOL_ICON_DIR
            with Image.open(directory / f'{icon}.png') as source:
                image = source.convert('RGBA')
            image.thumbnail((22, 22), Image.Resampling.LANCZOS)
            self.tool_icons[key] = ImageTk.PhotoImage(image, master=self)
        return self.tool_icons[key]

    def tool_button(self, parent, icon, label, command):
        widget = self.button(parent, label, command)
        widget.tool_icon = icon
        widget.tool_label = label
        widget.configure(padx=0, pady=0, compound='none')
        widget.tool_tip = Tooltip(widget, label)
        self.paint_tool(widget)
        return widget

    def paint_tool(self, widget, selected=False):
        widget.tool_selected = selected
        self.color_button(widget, selected)
        light_ink = self.palette['dark'] and not selected
        widget.configure(image=self.tool_image(widget.tool_icon, light_ink))
        if light_ink:
            widget.configure(activebackground=self.palette['selection'])

    def create_tool_rail(self):
        self.tool_rail = tk.Canvas(self, bd=0, highlightthickness=0)
        self.tools = self.tool_button(self.tool_rail, 'collapse', 'Ẩn thanh công cụ', self.toggle_tool_rail)
        self.tool_overflow = self.tool_button(self.tool_rail, 'more', 'Công cụ khác',
                                             lambda: self.toggle_panel('tools'))
        reader = self.reader
        self.tool_actions = {
            mode: (label, lambda mode=mode: reader.set_mode(mode), mode)
            for mode, label in TOOL_LABELS.items() if mode != 'picture'
        }
        self.tool_actions.update({
            'picture': ('Chèn ảnh', reader.add_picture, None),
            'color': ('Màu', self.choose_tool_color, None),
            'smaller': ('Bút −', lambda: reader.set_width(-2), None),
            'larger': ('Bút +', lambda: reader.set_width(2), None),
            'undo': ('Hoàn tác', reader.undo, None),
            'redo': ('Làm lại', reader.redo_action, None),
            'clear': ('Xóa tất cả', reader.clear, None),
            'info': ('Giới thiệu công cụ', lambda: self.show_panel('credits'), None),
        })
        for key in PRIMARY_TOOLS:
            label, command, _ = self.tool_actions[key]
            self.rail_buttons[key] = self.tool_button(self.tool_rail, key, label, command)
        self.layout_tool_rail()

    def toggle_tool_rail(self):
        self.tools_visible = not self.tools_visible
        if self.panel_name == 'tools':
            self.close_panel()
        self.tools.tool_icon = 'collapse' if self.tools_visible else 'expand'
        self.tools.tool_label = 'Ẩn thanh công cụ' if self.tools_visible else 'Hiện thanh công cụ'
        self.tools.tool_tip.hide()
        self.tools.tool_tip.text = self.tools.tool_label
        self.tools.configure(text=self.tools.tool_label)
        self.paint_tool(self.tools)
        self.layout_tool_rail()

    def layout_tool_rail(self):
        top = self.header.winfo_y() + self.header.winfo_height() + TOOL_TOP_GAP
        available = self.winfo_height() - top - self.footer.winfo_height() - 8
        limit = max(0, available // TOOL_ROW_HEIGHT - 2)
        visible = PRIMARY_TOOLS[:limit] if self.tools_visible else ()
        overflow_changed = visible != self.visible_tools
        self.visible_tools = visible
        # Keep the destructive action near the end while giving it a direct slot.
        keys = [key for key in visible if key != 'clear']
        if 'clear' in visible:
            keys.append('clear')
        slots = [self.tools, *(self.rail_buttons[key] for key in keys)]
        if self.tools_visible:
            slots.append(self.tool_overflow)
        for widget in (*self.rail_buttons.values(), self.tool_overflow):
            if widget not in slots and widget.winfo_manager():
                widget.tool_tip.hide()
                widget.place_forget()
        self.rail_slots = slots
        for i, widget in enumerate(slots):
            widget.place(x=7, y=7 + i * TOOL_ROW_HEIGHT,
                         width=TOOL_RAIL_WIDTH - 15, height=TOOL_ROW_HEIGHT - 13)
        self.tool_rail.place(x=0, y=top, width=TOOL_RAIL_WIDTH,
                             height=len(slots) * TOOL_ROW_HEIGHT + 8)
        tk.Misc.tkraise(self.tool_rail)
        self.draw_tool_rail()
        if overflow_changed and self.panel_name == 'tools':
            self.show_panel('tools', animate=False)

    def choose_tool_color(self):
        self.reader.choose_color()
        self.draw_tool_rail()

    def draw_tool_rail(self):
        canvas = self.tool_rail
        shell, shine, bevel, shadow = TOOL_RAIL_FINISH[self.theme]
        width = TOOL_RAIL_WIDTH
        height = len(self.rail_slots) * TOOL_ROW_HEIGHT + 8
        canvas.delete('rail')
        canvas.create_rectangle(3, 4, width, height, fill=shadow, outline='', tags='rail')
        canvas.create_rectangle(0, 0, width - 3, height - 4, fill=shell, outline=bevel, tags='rail')
        canvas.create_line(1, height - 5, 1, 1, width - 4, 1, fill=shine, tags='rail')
        for i, widget in enumerate(self.rail_slots):
            top = 5 + i * TOOL_ROW_HEIGHT
            bottom = top + TOOL_ROW_HEIGHT - 8
            inset = widget.tool_selected
            canvas.create_rectangle(5, top, width - 6, bottom,
                                    fill=bevel, outline=shadow, tags='rail')
            canvas.create_line(5, bottom, 5, top, width - 6, top,
                               fill=shadow if inset else shine, tags='rail')
            canvas.create_line(6, bottom, width - 6, bottom, width - 6, top + 1,
                               fill=shine if inset else shadow, tags='rail')
            if widget.tool_icon == 'color':
                canvas.create_line(12, bottom + 3, width - 13, bottom + 3,
                                   fill=self.reader.color, width=2, tags='rail')

    def label(self, parent, text, bold=False, wrap=0):
        return tk.Label(parent, text=text, anchor='w', justify='left', wraplength=wrap,
                        bg=self.palette['panel'], fg=self.palette['ink'],
                        font=('Segoe UI', 10, 'bold' if bold else 'normal'))

    def panel_frame(self, parent):
        return tk.Frame(parent, bg=self.palette['panel'], highlightthickness=1,
                        highlightbackground=self.palette['selection'])

    def recolor(self):
        p = self.palette
        self.configure(bg=p['page'])
        self.header.configure(bg=p['panel'])
        self.footer.configure(bg=p['page'])
        self.center.configure(bg=p['panel'], fg=p['ink'])
        self.tool_rail.configure(bg=p['page'])
        for button in (self.back_button, self.expand, self.aa, self.words):
            self.color_button(button)
        for button in (self.tools, self.tool_overflow):
            self.paint_tool(button)
        self.update_tool_state()
        self.reader.apply_reading_palette(p)

    def change_setting(self, *, theme=None, zoom=0, spacing=0):
        if (zoom or spacing) and self.reader.typography_locked:
            return
        if theme is not None:
            self.theme = theme
            self.palette = PALETTES[theme]
            self.recolor()
        self.reader.zoom = max(.7, min(1.7, round(self.reader.zoom + zoom, 2)))
        self.reader.line_spacing = max(1.35, min(2.25, round(self.reader.line_spacing + spacing, 2)))
        self.reader.render()
        self.app._display_settings['library_reading'] = {
            'theme': self.theme, 'zoom': self.reader.zoom, 'spacing': self.reader.line_spacing,
        }
        try:
            self.app._save_display_settings()
        except OSError as exc:
            messagebox.showerror('Thiết lập đọc', str(exc), parent=self)
        if self.panel_name == 'appearance' and theme is not None:
            self.show_panel('appearance', animate=False)

    def set_expanded(self, enabled=None):
        enabled = not self.expanded if enabled is None else bool(enabled)
        if enabled == self.expanded:
            return
        self.close_panel()
        self.reader._hide_selection_popup()
        self.reader._pending_reading_anchor = self.reader._reading_anchor()
        self.app.attributes('-fullscreen', enabled)
        self.reader._schedule_render()
        self.expanded = enabled
        self.expand.configure(text='⤢ Thu nhỏ' if enabled else '⤢ Mở rộng')
        self.reader.canvas.focus_set()

    def escape(self):
        if self.panel is not None:
            self.close_panel()
        elif self.reader._selection_popup is not None:
            self.reader._hide_selection_popup()
        elif self.expanded:
            self.set_expanded(False)
        else:
            self.back()

    def dismiss_panel(self, event):
        if self.panel is not None:
            self.close_panel(focus=False)

    def close_panel(self, focus=True):
        self.jobs.cancel_all()
        if self.panel is not None:
            self.panel.destroy()
            if focus:
                self.reader.canvas.focus_set()
        self.panel = self.panel_name = None
        self.panel_controls.clear()
        self.mode_buttons.clear()
        self.update_tool_state()

    def toggle_panel(self, name):
        if self.panel_name == name:
            self.close_panel()
        else:
            self.show_panel(name)

    def show_panel(self, name, animate=True):
        self.close_panel(focus=False)
        self.reader._hide_selection_popup()
        self.panel_name = name
        self.panel = self.panel_frame(self)
        width = self.panel_width()
        top = tk.Frame(self.panel, bg=self.palette['panel'])
        top.pack(fill='x', padx=8, pady=(5, 0))
        title = {'appearance': 'Hiển thị', 'tools': 'Công cụ khác', 'glossary': 'Từ khó',
                 'credits': 'Giới thiệu công cụ'}[name]
        self.label(top, title, bold=True).pack(side='left')
        close = self.button(top, '✕', self.close_panel)
        close.pack(side='right')
        viewport = tk.Canvas(self.panel, bg=self.palette['panel'], highlightthickness=0)
        scroll = ttk.Scrollbar(self.panel, orient='vertical', command=viewport.yview,
                               style=self.reader._scrollbar.cget('style'))
        scroll.pack(side='right', fill='y')
        viewport.pack(side='left', fill='both', expand=True)
        viewport.configure(yscrollcommand=scroll.set)
        self.panel_body = tk.Frame(viewport, bg=self.palette['panel'])
        content = viewport.create_window(0, 0, window=self.panel_body, anchor='nw')
        viewport.bind('<Configure>', lambda e: viewport.itemconfigure(content, width=e.width))
        self.panel_body.bind('<Configure>', lambda e: viewport.configure(scrollregion=viewport.bbox(content)))
        builders = {'appearance': self.appearance_controls, 'tools': self.tool_controls,
                    'glossary': self.glossary_controls, 'credits': self.credits_controls}
        builders[name](self.panel_body, width - 54)
        self.update_tool_state()

        def bind_wheel(widget):
            def scroll_panel(event):
                steps = -int(event.delta / 120) if event.num not in (4, 5) else (-1 if event.num == 4 else 1)
                viewport.yview_scroll(steps, 'units')
                return 'break'
            for sequence in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                widget.bind(sequence, scroll_panel)
            for child in widget.winfo_children():
                bind_wheel(child)

        bind_wheel(viewport)
        close.focus_set()
        self.panel_body.update_idletasks()
        self.position_panel(animate=animate)

    def panel_width(self):
        if self.panel_name in ('tools', 'credits'):
            return min(230, max(1, self.winfo_width() - TOOL_RAIL_WIDTH - 16))
        return min(340, max(1, self.winfo_width() - 24))

    def on_resize(self, event):
        if event.widget is not self:
            return
        header_margin = max(138, self.aa.winfo_reqwidth() + self.expand.winfo_reqwidth() + 24)
        self.center.place_configure(width=max(1, event.width - 2 * header_margin))
        self.layout_tool_rail()
        self.position_panel()

    def position_panel(self, animate=False):
        if self.panel is None:
            return
        self.jobs.cancel_all()
        width = self.panel_width()
        height = max(1, min(self.panel_body.winfo_reqheight() + 48,
                            self.winfo_height() - self.header.winfo_height() - self.footer.winfo_height() - 12))
        top = self.panel_name == 'appearance'
        if top:
            y = self.header.winfo_height() + 4
            x = max(12, min(self.aa.winfo_x() + self.aa.winfo_width() - width,
                            self.winfo_width() - width - 12))
        elif self.panel_name in ('tools', 'credits'):
            x = TOOL_RAIL_WIDTH + 4
            y = self.header.winfo_y() + self.header.winfo_height() + TOOL_TOP_GAP
        else:
            y = self.winfo_height() - self.footer.winfo_height() - height - 4
            x = self.winfo_width() - width - 12
        self.panel.place(x=x, y=y, width=width, height=height)
        self.panel.lift()
        if not animate or self.app.reduce_motion or getattr(self.app, 'reduced_motion', False):
            return
        start = monotonic()

        def frame():
            progress = min(1, (monotonic() - start) * 1000 / DURATION['fast'])
            offset = round(12 * (1 - ease_out_cubic(progress)))
            self.panel.place_configure(y=y + (-offset if top else offset))
            if progress < 1:
                self.jobs.schedule(frame)

        frame()

    def appearance_controls(self, body, wrap):
        row = tk.Frame(body, bg=self.palette['panel'])
        row.pack(fill='x', padx=8, pady=4)
        for key, label in THEME_LABELS.items():
            selected = self.theme == key
            self.button(row, ('✓ ' if selected else '') + label,
                        lambda value=key: self.change_setting(theme=value), primary=selected).pack(
                side='left', expand=True, fill='x')
        self.typography_labels = {}
        for key, label in (('zoom', 'Cỡ chữ'), ('spacing', 'Giãn dòng')):
            row = tk.Frame(body, bg=self.palette['panel'])
            row.pack(fill='x', padx=8, pady=3)
            value_label = self.label(row, label)
            value_label.pack(side='left')
            self.typography_labels[key] = value_label
            controls = tk.Frame(row, bg=self.palette['panel'])
            controls.pack(side='right')
            for caption, step in (('−', -.15), ('+', .15)):
                control = self.button(controls, caption,
                                      lambda setting=key, delta=step: self.change_setting(**{setting: delta}))
                control.configure(width=3, relief='solid', bd=1)
                control.pack(side='left', padx=2)
                self.panel_controls.append(control)
        if self.reader.typography_locked:
            self.label(body, 'Cỡ chữ và giãn dòng được khóa để giữ vị trí nét vẽ. Hãy rời chế độ Vẽ và tẩy hoặc hoàn tác các nét còn lại.',
                       wrap=wrap).pack(fill='x', padx=8, pady=4)

    def tool_controls(self, body, wrap):
        for key, (label, command, mode) in self.tool_actions.items():
            if key in self.visible_tools:
                continue
            row = tk.Frame(body, bg=self.palette['panel'])
            row.pack(fill='x', padx=6, pady=1)
            widget = self.tool_button(row, key, label, command)
            widget.pack(side='left', ipadx=6, ipady=4)
            caption = self.label(row, label)
            caption.pack(side='left', padx=6, fill='x', expand=True)
            caption.bind('<Button-1>', lambda event, button=widget: button.invoke())
            if mode:
                self.mode_buttons[mode] = widget

    def credits_controls(self, body, wrap):
        self.label(body, 'Biểu tượng thanh công cụ do Icons8 cung cấp.', wrap=wrap).pack(
            fill='x', padx=8, pady=6)
        self.button(body, 'Icons8 ↗', lambda: webbrowser.open('https://icons8.com/')).pack(
            anchor='w', padx=8, pady=6)

    def update_tool_state(self):
        if not hasattr(self, 'reader'):
            return
        for key, widget in (*self.rail_buttons.items(), *self.mode_buttons.items()):
            self.paint_tool(widget, key == self.reader.mode)
        self.paint_tool(self.tool_overflow, self.panel_name == 'tools' or (
            self.tools_visible and self.reader.mode not in self.visible_tools))
        self.draw_tool_rail()
        if self.panel_name == 'appearance':
            self.typography_labels['zoom'].configure(text=f'Cỡ chữ  {self.reader.zoom:.0%}')
            self.typography_labels['spacing'].configure(text=f'Giãn dòng  {self.reader.line_spacing:g}×')
        for widget in self.panel_controls:
            widget.configure(state='disabled' if self.reader.typography_locked else 'normal')

    def flashcard_button(self, parent, word):
        key = glossary_key(word)

        def save():
            if self.reader.on_add_vocab(word):
                self.saved_words.add(key)
                widget.configure(text='✓ Đã lưu', state='disabled')

        widget = self.button(parent, 'Lưu vào Flashcard', save, primary=True)
        if key in self.saved_words:
            widget.configure(text='✓ Đã lưu', state='disabled')
        return widget

    def glossary_controls(self, body, wrap):
        if not self.glossary:
            self.label(body, 'Bài này chưa có từ khó.', wrap=wrap).pack(fill='x', padx=8, pady=8)
        for entry in self.glossary.values():
            self.label(body, entry['word'], bold=True, wrap=wrap).pack(fill='x', padx=8, pady=(8, 0))
            self.label(body, entry['meaning'], wrap=wrap).pack(fill='x', padx=8)
            self.flashcard_button(body, entry['word']).pack(anchor='w', padx=8, pady=(3, 8))

    def destroy(self):
        self.jobs.cancel_all()
        if self.expanded:
            self.app.attributes('-fullscreen', False)
        super().destroy()


def open_reading(app, store, article, back):
    if not available():
        messagebox.showerror(title='Thiếu thư viện', message='Cần pygame và Pillow để mở bài đọc.',
                             parent=app)
        return
    image = store.resolve_media(article['image'], 'image')
    def add_vocab(selection):
        if not app.student:
            messagebox.showwarning(title='Chưa chọn học sinh', message='Hãy chọn hồ sơ để lưu từ.',
                                   parent=app)
            return False
        word = selection.strip()
        if not word:
            return False
        entry = next((entry for entry in article['glossary']
                      if glossary_key(entry['word']) == glossary_key(word)), None)
        if entry:
            word, meaning = entry['word'], entry['meaning']
        else:
            meaning = simpledialog.askstring('Thêm từ vựng', f'Nghĩa của “{word}”:', parent=app)
        if not meaning or not meaning.strip():
            return False
        key = app.learning.wordkey(word)
        language = 'vi' if article['subject'] == 'tieng_viet' else 'en'
        try:
            saved = app.db.save_word_in_source(app.student['id'], key if language == app.lang else word,
                                               meaning.strip(), 'reading', theme=article['topic_id'],
                                               level=0, source_title=article['title'], lang=language)
        except sqlite3.Error as exc:
            messagebox.showerror(title='Không lưu được từ vựng', message=str(exc), parent=app)
            return False
        return saved is not None

    def play():
        try:
            audio = store.resolve_media(article['audio'], 'audio')
            if audio:
                app.play_learning_audio(audio)
            else:
                speak_article(app, article)
        except LibraryError as exc:
            messagebox.showerror(title='Không mở được âm thanh', message=str(exc), parent=app)

    app.clear()
    if app._shell is not None:
        app._shell.pack_forget()
    app._admin_page = f"Đọc · {article['title']}"
    app._page_transition_ready = False
    page = ReadingPage(app, article, image, back, speak=lambda value: speak_article(app, article, value),
                       on_add_vocab=add_vocab, on_play_audio=play)
    page.pack(fill='both', expand=True)
    morph=getattr(app,'morph',None)
    if morph:
        morph.arrive(f"practice:{article['id']}",page.center)
    reader = page.reader
    app._library_reading_page = page
    app._teaching_escape = page.escape
    app._v8_active_reader = reader
    for mode, color in getattr(app, '_v8_palette_colors', {}).items():
        reader.set_tool_color(mode, color)

    def cleanup(event):
        if event.widget is not reader:
            return
        if app._v8_active_reader is reader:
            app._v8_active_reader = None
        if app._library_reading_page is page:
            app._library_reading_page = None
        if getattr(app, '_teaching_escape', None) == page.escape:
            app._teaching_escape = None

    reader.bind('<Destroy>', cleanup, add='+')
    reader.canvas.focus_set()
    if app.student:
        app.db.save_library_result(app.student['id'], article['id'], 'read', 100, True)
    return reader
