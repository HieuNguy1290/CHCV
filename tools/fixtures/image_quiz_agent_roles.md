# Hai vai nhập Bài tập từ ảnh

Chạy `python -B -m tools.fixtures.build_image_quiz_drafts "<thư mục nguồn>"` để lấy danh sách câu theo số. Thư mục nguồn do người dùng chọn. Ảnh `1.png` và thư mục con nằm ngoài lượt quét.

## Vai dựng câu

Đọc ảnh gốc và danh sách MP3 đã ghép. Trả một object cho mỗi `number`. Dùng `image_sentence_fill` cho câu điền một từ bằng hình, với `prompt`, `blank_text` chứa một `....`, `options` và `crop` nếu có ảnh minh họa. Dùng `listening_image_choice` cho câu nghe chọn ảnh, với `prompt` và `choices` gồm các cặp `label`, `crop` theo thứ tự nguồn. Vùng cắt dùng pixel gốc `[trái, trên, phải, dưới]`. Dùng chữ trong ảnh làm nhãn riêng khi vùng cắt chỉ chứa hình.

## Vai đối chiếu

So từng câu với ảnh gốc, kiểm thứ tự lựa chọn, phạm vi cắt và MP3 được ghép đúng số. Điền `answer_index` từ 0 khi xác định được một đáp án. Có thể đọc đáp án đánh dấu rõ hoặc giải từ dữ kiện của đề. Phân biệt dấu xác nhận đúng với phương án chỉ đang được học viên chọn. Với câu nghe, dùng nội dung nghe đã đối chiếu hoặc nguồn đáp án rõ ràng. Tên MP3 chỉ dùng để ghép tệp. Ghi căn cứ trong `review`. Nếu thiếu bằng chứng, đặt `answer_index: null` và ghi lý do trong `review` để câu được giữ chờ.

## Xuất gói thử

```powershell
python -B -m tools.fixtures.build_image_quiz_drafts "<thư mục nguồn>" --drafts tools/fixtures/vioedueng_lesson6_drafts.json --output "<thư mục thử mới>" --theme VioeduEng --level 1 --lesson 6
```

Lượt thử dùng bản JSON do Codex đọc và đối chiếu hai ảnh nguồn. Script tạo `level_questions.json`, `media/` và `review.json` trong thư mục mới. `review.json` lưu căn cứ đã đối chiếu và các câu còn chờ.

Khi người dùng yêu cầu nhập, chọn các số câu đã xác định được đáp án và đúng thư mục môn.

```powershell
python -B -m tools.fixtures.build_image_quiz_drafts "<gói nháp>" --publish-to "mon_hoc/tieng_anh" --approve 1 2
```

Lệnh nhập kiểm tra mã chủ đề, xử lý tham chiếu media và sao lưu ngân hàng. Chạy lại cùng gói sẽ bỏ qua mã câu có nội dung trùng. Mã câu hoặc media trùng tên mà khác nội dung cần được xử lý trước.

Nếu cần một dạng ngoài các dạng bộ nhập hiểu, áp dụng mục **Khi gặp dạng câu mới** trong [luồng PNG](../../agents/skills/tuhoc-image-quiz-import/SKILL.md). Chỉ xuất và nhập theo dạng mới sau khi kiểm thử tương tác và chấm đạt.
