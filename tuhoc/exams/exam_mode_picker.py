"""Entry page for the two exam modes."""

import tkinter as tk

from tuhoc.ui.ui_components import Card, RoundedButton
from tuhoc.ui.ui_tokens import COLORS, font_at


def show_exam_modes(app):
    body = app.layout('Kiểm tra')
    grid = tk.Frame(body, bg=COLORS['background'])
    grid.pack(fill='x', padx=8, pady=(18, 0))
    choices = (
        ('Bộ đề', 'Đề kiểm tra đã soạn', 'Làm bài theo bộ đề cố định.', None),
        ('Kiểm tra', 'Ngân hàng câu hỏi', 'Tạo đề theo môn, Level, Lesson và tỷ lệ M1–M5.',
         app.open_bank_exam),
    )
    buttons = []
    for index, (name, heading, description, command) in enumerate(choices):
        grid.columnconfigure(index, weight=1, uniform='exam-mode')
        card = Card(grid)
        card.grid(row=0, column=index, sticky='nsew', padx=8)
        tk.Label(card, text=name, bg=COLORS['tint'], fg=COLORS['primary_text'],
                 font=font_at(26, 'bold'), pady=30).pack(fill='x')
        tk.Label(card, text=heading, bg=COLORS['surface'], fg=COLORS['text'],
                 font=font_at(15, 'bold')).pack(pady=(14, 5))
        tk.Label(card, text=description, bg=COLORS['surface'], fg=COLORS['muted'],
                 font=font_at(11), wraplength=240, height=2).pack()
        if command is None:
            morph = getattr(app,'morph',None)
            def command(widget=card):
                if morph:
                    morph.begin(widget,'fixed-list','Bộ đề')
                app._navigate_to(app.fixed_exam_page)
            if morph:
                morph.arrive('fixed-card',card)
        button = RoundedButton(card, f'Chọn {name}', command)
        button.pack(pady=(14, 0))
        buttons.append(button)
    for index, button in enumerate(buttons):
        other = buttons[1 - index]
        button.bind('<Left>', lambda _event, target=other: target.focus_set())
        button.bind('<Right>', lambda _event, target=other: target.focus_set())
