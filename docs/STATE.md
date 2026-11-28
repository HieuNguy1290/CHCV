## Quyết định đã chốt

- Mã ứng dụng theo chức năng dưới `tuhoc/`. Công cụ kiểm tra chạy bằng `python -B -m tools.checks.<tên>`. Công cụ di trú và dữ liệu mẫu nằm dưới `tools/`.
- `python -B main.py` và hai lệnh di trú cũ vẫn chạy. Đường dẫn hồ sơ, học liệu và tài nguyên được xác định từ gốc dự án.
- Mục Kiểm tra có kho Bộ đề riêng trong `content_library/fixed_exams/`. Bộ đề dùng màn thi hiện có ở chế độ cuộn dọc, còn đề rút theo M1–M5 dùng chế độ từng câu.
- Cài đặt hiển thị có theme Tối cho shell Tk, hồ sơ, chọn môn, Trang chủ, bản đồ bài học và trình soạn Bộ đề. Trong Bộ đề, nút Về đoạn văn cuộn đến đầu phần đang làm.

## Việc còn lại

- Chưa kiểm trực tiếp trên Windows với taskbar, DPI, IME, âm thanh và đóng gói.

## Học – Hình + nội dung (đang làm)

- Đã có: `tuhoc/lessons/lesson_canvas_math.py` (toạ độ neo, tô sáng theo khoảng ký tự), `tuhoc/lessons/image_children.py` (JSON `image_children`, Pager), trình soạn trong `multi_block_editor.py`, màn xem trong `pygame_lesson_window.py`. Test: `python -B -m unittest tests.test_lesson_canvas`.
- Chưa kiểm trên máy có GUI: toàn bộ phần vẽ Pygame và Tk của các thay đổi trên. Ca nghiệm thu: vẽ lên ảnh → tô sáng → zoom/cuộn → đổi mục → quay lại → tẩy/hoàn tác.

