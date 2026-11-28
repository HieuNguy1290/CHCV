import pygame

from tuhoc.exams.exam_bank_pygame import BankManager, TYPES


def test_bank_icons_and_edge_tooltip_at_minimum_size(tmp_path, monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.init()
    pygame.font.init()
    try:
        view = BankManager(tmp_path)
        view.size = (760, 570)
        view.screen = pygame.display.set_mode(view.size)
        view.f, view.sm, view.h, view.b = (
            view.font(18), view.font(15), view.font(27, True), view.font(19, True),
        )
        view.lesson = "Lesson with a long name " * 8
        key = view.bank.save_question({
            "type": "choice", "subject": "tieng_anh", "grade": "1", "lesson": view.lesson,
            "prompt": "Nội dung câu hỏi dài " * 12, "options": ["A", "B"],
            "answer": "A", "difficulty": 2,
        })
        view.draw()
        bounds = view.screen.get_rect()
        labels = {label: rect for rect, label in view._tooltips}
        assert {"Sửa câu hỏi", "Sao chép câu hỏi", "Xóa câu hỏi",
                "Nhập gói câu hỏi", "Thêm câu hỏi"} <= labels.keys()
        assert any("Nội dung câu hỏi dài" in label for label in labels)
        assert all(bounds.contains(rect) for rect in labels.values())
        assert view.fit_text("Long word", view.sm, 1) == ""
        view.click(labels["Sửa câu hỏi"].center)
        assert view.edit_id == key

        anchor = pygame.Rect(716, 536, 42, 30)
        view._tooltips = [(anchor, "Xóa câu hỏi")]
        view.mouse_pos = anchor.center
        view.draw_tooltip()
        view._tooltip_since -= 400
        boxes = []
        monkeypatch.setattr(view, "rect", lambda rect, *args, **kwargs: boxes.append(rect.copy()))
        view.draw_tooltip()
        assert boxes and bounds.contains(boxes[0])
        assert boxes[0].bottom <= anchor.top

        view.open_dropdown("filter_type", [key for key, _ in TYPES], anchor, dict(TYPES))
        assert bounds.contains(view.dropdown_box())
        assert view.dropdown_box().bottom <= anchor.top
    finally:
        pygame.quit()
