---
name: tuhoc-image-quiz-import
description: Dựng và nhập bài tập TuHoc từ thư mục ảnh câu N.png và MP3 cùng tên khi người dùng yêu cầu, tự xác định đáp án có căn cứ và sao lưu ngân hàng Lesson.
---

# Nhập bài tập TuHoc từ ảnh

Chạy từ checkout chứa `main.py` bằng Python 3.12. Dùng thư mục nguồn người dùng chọn và đích gồm môn, mã chủ đề, Level, Lesson. Dùng ngữ cảnh đã xác nhận trong phiên nếu đủ rõ. `VioeduEng` là mã của lô thử Tiếng Anh, Level 1, Lesson 6. Xác nhận mã từ `mon_hoc/<môn>/content_library/themes.json` khi đích thay đổi.

Đọc đáp án từ `result.png` trong thư mục Lesson. Ảnh này là bảng đáp án và nằm ngoài danh sách ảnh câu hỏi. Đọc một lượt, ghi các đáp án xác minh được theo đúng số câu vào file JSON rồi truyền `--answers`. Nếu bảng dùng A/B/C…, lần lượt đổi thành 0/1/2 sau khi xác minh thứ tự lựa chọn trong ảnh nguồn. Nếu bảng dùng chữ hoặc nhãn ảnh, giữ nguyên văn. Ghi nguồn `result.png` khi soát gói. Câu thiếu, ảnh kết quả khó đọc hoặc mâu thuẫn thì giữ chờ và ghi lý do. Python ghép đáp án với lựa chọn, model và Codex chỉ đối chiếu. Nếu chưa đọc được bảng, tiếp tục dựng nháp với file `{}` hoặc bỏ `--answers` khi đã có `result.png`. Nếu ảnh kết quả chưa có, dùng `{}` để dựng nháp chờ đáp án.

1. Chạy `python -B -m tools.local_agent process --source "<nguồn>" [--answers "<đáp án.json>"]` một lần cho cả lô. Dùng `py -3.12` nếu `python` trỏ sang phiên bản khác trên Windows. File đáp án dùng số câu làm khóa và chỉ số từ 0 hoặc nhãn nguyên văn làm giá trị, ví dụ `{"2": 1, "3": "star"}`. Có thể dùng `health` để kiểm API Ollama local và model `qwen3-vl:4b-instruct`. Bộ quét hiện có bỏ qua `1.png` và thư mục con.
2. Local Agent dùng cache, thực hiện hai lượt **dựng câu** và **đối chiếu**, rồi kiểm schema, đáp án, vùng cắt và media bằng Python. Khi cần, dùng `report --batch <id>` hoặc `resume --batch <id>`. Thêm `--refresh` vào `resume` để chạy lại model cho ngoại lệ. Chạy lại `process` khi nguồn hoặc đáp án thay đổi. Cache và bản xuất từng lượt nằm dưới `%LOCALAPPDATA%/TuHoc/local-agent` trên Windows.
3. Đọc `exceptions` và lấy mẫu `passed` để so chữ, thứ tự, vùng cắt và căn cứ với ảnh. Mở rộng kiểm tra khi mẫu sai. Chỉ giảm phạm vi sau khi benchmark của dạng đó đạt. Với `listening_image_choice`, Codex đối chiếu trực quan vùng cắt và dùng nội dung MP3 đã soát hoặc nguồn đáp án rõ ràng trước khi duyệt. Khi model hoặc API lỗi, dùng bộ quét `tools.fixtures.build_image_quiz_drafts` và xử lý phần còn thiếu theo [hợp đồng hai vai](../../../tools/fixtures/image_quiz_agent_roles.md). Codex quyết định câu nào đủ điều kiện nhập, có quyền tự xác định đáp án có căn cứ và ghi nguồn trong `review`. Giữ đáp án do người dùng cung cấp và chuyển câu sang chờ nếu có mâu thuẫn.
4. Dùng `draft` hoặc một bản sao đã bổ sung soát xét, giữ một mục cho mỗi số câu. Khi thiếu căn cứ, đặt `answer_index` thành `null` và ghi lý do trong `review`. Câu nghe thiếu MP3 hoặc đáp án nằm ngoài tập nhập. Giữ cùng ảnh và MP3 đã soát. Tạo gói bằng `python -B -m tools.fixtures.build_image_quiz_drafts "<nguồn>" --drafts "<json>" --output "<thư mục mới>" --theme "<mã>" --level <n> --lesson <n>`. Kiểm gói. Nếu yêu cầu chỉ là dựng nháp hoặc xem trước, dừng sau bước này.
5. Khi yêu cầu là **nhập** và đích đã rõ, dùng `python -B -m tools.fixtures.build_image_quiz_drafts "<gói nháp>" --publish-to "mon_hoc/<môn>" --approve <số câu đủ căn cứ>`. Lệnh sao lưu ngân hàng và nhận đúng các số câu đã đối chiếu. Codex được phép thực hiện khi đủ căn cứ. Sau nhập, dùng `python -B -m tools.local_agent verify --subject "mon_hoc/<môn>" --package "<gói nháp>" --approve <cùng số câu>` để kiểm bằng `Curriculum` và `subject_image`. Phản hồi cuối liệt kê đáp án theo số câu, dùng nhãn ảnh với câu nghe chọn ảnh, và ghi trạng thái ngắn cho câu chờ.

## Khi gặp dạng câu mới

Người dùng cho phép Codex tự triển khai dạng mới cho **Bài tập Lesson/Level** trong lượt nhập PNG. Xác định thao tác và quy tắc chấm từ ảnh, nội dung nghe hoặc tài liệu đi kèm. Nếu TuHoc đã có dạng tương đương, mở rộng bộ nhập để dùng lại dạng đó.

Nếu cần một dạng thật sự mới, đọc chỉ dẫn Canvas và hợp đồng renderer trong `AGENTS.md` trước khi sửa. Bổ sung dữ liệu câu hỏi, trình soạn và xem trước, dispatch Pygame, thao tác và chấm, hiển thị kết quả hoặc ôn lại, rồi nối dạng đó vào bộ dựng PNG. Giữ tương thích cho câu đã lưu. Kiểm thử từ đường vào Bài tập thật với ít nhất một lượt đúng, một lượt sai và đóng hoặc xem trước không ghi tiến trình trước khi nhập câu thật.

Quyền này áp dụng cho thêm dạng Bài tập, với hợp đồng lưu dữ liệu tương thích. Nếu thiếu căn cứ về thao tác hay cách chấm, kiểm thử chưa đạt, hoặc cần thay đổi cách chấm Exam Mode hay chuyển đổi dữ liệu cũ, giữ câu chờ và báo lý do. Tiếp tục các câu còn lại. Luồng PDF vẫn tạm dừng.
