"""Preview a shared question pack and choose where its questions will go."""
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from tuhoc.storage.question_packages import suggested_topic_title


def choose_question_package_target(app, package, status, preferred):
    topic = package.topic
    window = tk.Toplevel(app)
    window.title("Nhập gói bài học" if package.lesson_content is not None else "Nhập gói bài tập")
    window.transient(app)
    window.geometry("620x460")
    window.minsize(470, 380)
    body = ttk.Frame(window, padding=14)
    body.pack(fill="both", expand=True)

    ttk.Label(body, text=package.title, wraplength=565).pack(anchor="w")
    source = package.author or "Không ghi tên"
    ttk.Label(body, text=f"{len(package.questions)} câu · {len(package.assets)} tệp đính kèm · Tác giả: {source}",
              wraplength=565).pack(anchor="w", pady=(4, 10))
    if status == "update":
        message = ("Đã có phiên bản trước. Bản này sẽ tạo một chủ đề riêng."
                   if topic else "Đã có một phiên bản của gói này. Nhập bản mới sẽ thêm các câu dưới dạng bản sao.")
        ttk.Label(body, text=message,
                  wraplength=565).pack(anchor="w", pady=(0, 8))
    if topic:
        level_count = topic["max_level"]
        lesson_count = sum(int(topic["lesson_counts"].get(str(level), topic["default_lessons"]))
                           for level in range(1, level_count + 1))
        ttk.Label(body, text=f"{topic['title']} · {level_count} Level · {lesson_count} Lesson",
                  wraplength=565).pack(anchor="w", pady=(0, 8))
    preview = ScrolledText(body, wrap="word", height=8)
    preview.pack(fill="both", expand=True)
    rows = package.questions
    if topic:
        rows = sorted(rows, key=lambda question: (question["level"], question["lesson"]))
    lines = []
    if package.lesson_content is not None:
        labels = {"lessons": "Bài học", "blocks": "Khối bài học", "reading": "Bài đọc", "vocab": "Từ vựng"}
        for kind, records in package.lesson_content.items():
            if records:
                lines.append(f"{labels[kind]} ({len(records)})")
            for row in records:
                label = row.get("title") or row.get("word") or row.get("content") or labels[kind]
                lines.append(f"Level {row['level']} · Lesson {row['lesson']} — {str(label)[:180]}")
    for index, question in enumerate(rows, 1):
        position = f"Level {question['level']} · Lesson {question['lesson']} — " if topic else ""
        lines.append(f"{index}. {position}{question.get('prompt') or question['id']}")
    preview.insert("1.0", "\n\n".join(lines))
    preview.configure(state="disabled")

    if topic:
        ttk.Label(body, text="Tên chủ đề mới").pack(anchor="w", pady=(10, 2))
        name = ttk.Entry(body)
        name.insert(0, suggested_topic_title(package))
        name.pack(fill="x", pady=(0, 8))
        return _confirm(window, body, "Tạo chủ đề mới", name.get, name)

    target = ttk.Frame(body)
    target.pack(fill="x", pady=10)
    names = {f"{name} ({code})": code for code, name, *_ in app._themes()}
    theme = tk.StringVar(window, next(iter(names)))
    level = tk.StringVar(window, "1")
    lesson = tk.StringVar(window, "1")

    def select_field(label, variable, width):
        group = ttk.Frame(target)
        group.pack(side="left", padx=(0, 10))
        ttk.Label(group, text=label).pack(anchor="w")
        field = ttk.Combobox(group, textvariable=variable, state="readonly", width=width)
        field.pack()
        return field

    theme_box = select_field("Chủ đề đích", theme, 24)
    theme_box.configure(values=list(names))
    level_box = select_field("Level", level, 8)
    lesson_box = select_field("Lesson", lesson, 8)

    def lessons(*_):
        values = [str(n) for n in range(1, app._lesson_count(names[theme.get()], int(level.get())) + 1)]
        lesson_box.configure(values=values)
        if lesson.get() not in values:
            lesson.set("1")

    def levels(*_):
        values = [str(n) for n in range(1, app._max_level(names[theme.get()]) + 1)]
        level_box.configure(values=values)
        if level.get() not in values:
            level.set("1")
        lessons()

    theme_box.bind("<<ComboboxSelected>>", levels)
    level_box.bind("<<ComboboxSelected>>", lessons)
    initial_theme, initial_level, initial_lesson = preferred
    for label, code in names.items():
        if code == initial_theme:
            theme.set(label)
            level.set(initial_level)
            lesson.set(initial_lesson)
            break
    levels()

    return _confirm(window, body, "Nhập bản mới" if status == "update" else "Nhập vào Lesson",
                    lambda: (names[theme.get()], int(level.get()), int(lesson.get())), theme_box)


def _confirm(window, body, caption, selection, focus):
    result = None

    def confirm():
        nonlocal result
        result = selection()
        window.destroy()

    actions = ttk.Frame(body)
    actions.pack(fill="x")
    ttk.Button(actions, text=caption, command=confirm).pack(side="right")
    ttk.Button(actions, text="Hủy", command=window.destroy).pack(side="right", padx=8)
    window.bind("<Escape>", lambda _: window.destroy())
    window.wait_visibility()
    window.grab_set()
    focus.focus_set()
    window.wait_window()
    return result
