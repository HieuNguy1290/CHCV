"""File dialogs shared by the Lesson and Question editors."""
from tkinter import filedialog, messagebox, simpledialog

from tuhoc.storage import question_packages as packs
from tuhoc.ui.question_package_dialog import choose_question_package_target


def export_level_package(app, questions, scope, *, topic=None, content=None):
    lesson_pack = content is not None
    label = "gói bài học" if lesson_pack else "gói bài tập"
    if lesson_pack and not any(content.values()):
        messagebox.showinfo("Xuất " + label, "Chủ đề chưa có nội dung bài học để xuất.", parent=app)
        return
    if not lesson_pack and not questions:
        messagebox.showinfo("Xuất " + label, "Không có câu hỏi để xuất.", parent=app)
        return
    if lesson_pack and questions:
        include = messagebox.askyesnocancel(
            "Xuất " + label, f"Đính kèm {len(questions)} câu bài tập của chủ đề?", parent=app,
        )
        if include is None:
            return
        if not include:
            questions = []
    description = "trong toàn bộ chủ đề" if topic else "theo bộ lọc hiện tại"
    prompt = "Tên gói bài học:" if lesson_pack else f"Tên gói gồm {len(questions)} câu {description}:"
    title = simpledialog.askstring("Xuất " + label, prompt,
                                   initialvalue=topic["title"] if topic else "", parent=app)
    if not title or not title.strip():
        return
    author = simpledialog.askstring("Xuất " + label, "Tên người chia sẻ (có thể bỏ trống):", parent=app)
    if author is None:
        return
    path = filedialog.asksaveasfilename(parent=app, filetypes=[("Gói TuHoc", "*" + packs.EXTENSION)],
                                        defaultextension=packs.EXTENSION)
    if not path:
        return
    try:
        packs.export_package(path, app.curriculum.data_dir, app.lang, scope, title, author,
                             questions, app.media_file, topic=topic, lesson_content=content)
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        messagebox.showerror("Không xuất được gói", str(exc), parent=app)
        return
    message = ("Đã lưu nội dung cùng các tệp đính kèm." if lesson_pack else
               f"Đã lưu {len(questions)} câu cùng tệp đính kèm.")
    messagebox.showinfo("Đã xuất " + label, message, parent=app)


def import_level_package(app, *, lesson_pack=False, preferred=None):
    label = "gói bài học" if lesson_pack else "gói bài tập"
    path = filedialog.askopenfilename(parent=app, title="Nhập " + label,
                                      filetypes=[("Gói TuHoc", "*" + packs.EXTENSION)])
    if not path:
        return None
    try:
        package = packs.read_package(path)
        if (package.lesson_content is not None) != lesson_pack:
            editor = "Thêm/sửa Bài học" if package.lesson_content is not None else "Thêm/sửa Bài tập"
            raise ValueError(f"Hãy mở {editor} để nhập gói này.")
        if package.language != app.lang:
            subject = "Tiếng Việt" if package.language == "vi" else "Tiếng Anh"
            raise ValueError(f"Gói này thuộc môn {subject}. Hãy chuyển sang môn đó trước khi nhập.")
        data_dir = app.curriculum.data_dir
        state = packs.package_status(package, data_dir)
        if state == "duplicate":
            count = 0
        else:
            selected = choose_question_package_target(app, package, state, preferred)
            if selected is None:
                return None
            if package.topic is not None:
                count, theme = packs.import_topic_package(package, data_dir, app.lang,
                                                           allow_update=state == "update", topic_title=selected)
                target = (theme, None, None)
                message = f"Đã tạo chủ đề mới với {count} mục ở các Level và Lesson tương ứng."
            else:
                count = packs.import_package(package, data_dir, app.lang, *selected,
                                             allow_update=state == "update")
                target = selected
                message = f"Đã thêm {count} câu vào Lesson đã chọn."
    except (OSError, ValueError, TypeError) as exc:
        messagebox.showerror("Không nhập được gói", str(exc), parent=app)
        return None
    if not count:
        messagebox.showinfo("Gói đã có", "Phiên bản này đã được nhập trước đó.", parent=app)
        return None
    app.curriculum.reload()
    messagebox.showinfo("Đã nhập " + label, message, parent=app)
    return target
