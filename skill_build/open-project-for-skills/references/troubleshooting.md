# Troubleshooting: skill không xuất hiện

## Kiểm tra theo thứ tự

1. Skill nằm ở đâu? Project: `<project>\.claude\skills\`. Personal: `%USERPROFILE%\.claude\skills\`.
2. Tên file đúng `SKILL.md`? Không phải `skill.md` hay `SKILL.MD`.
3. Dòng đầu tiên của file là `---`?
4. Có dòng `---` đóng frontmatter?
5. Frontmatter có `name` và `description` khác rỗng?
6. Session đã restart sau khi tạo/sửa skill?

Chạy `scripts/check-skills.ps1` để kiểm tra mục 1–5 tự động.

## Lỗi thường gặp

### Gọi `/ten-skill` không ra

- Session đang chạy từ trước khi skill được tạo → đóng chat, mở lại.
- `description` quá mơ hồ nên skill không được chọn theo ngữ cảnh → thêm "Use when ..." với từ khóa đúng như người dùng hay nói.
- Folder hoặc `name` có dấu cách, dấu chấm, chữ hoa → đổi sang kebab-case.

### Skill project không thấy, skill personal vẫn thấy

Workspace đang mở **folder con**. Ví dụ mở `E:\app\src` trong khi `.claude\skills` nằm ở `E:\app`.

Sửa: `File > Open Folder...` chọn `E:\app`. Với multi-root workspace, folder đầu tiên trong danh sách mới là root.

### Frontmatter không parse được

- Thiếu dòng `---` đóng.
- `description` chứa `:` mà không đặt trong ngoặc kép, hoặc chứa `<` `>`.
- Dùng tab thay vì space trong YAML.
- File có BOM ở đầu: lưu lại dạng UTF-8 không BOM.

Frontmatter tối thiểu hợp lệ:

```yaml
---
name: ten-skill
description: Việc skill làm. Use when nguoi dung yeu cau X.
---
```

### Sửa SKILL.md mà hành vi không đổi

Skill chỉ nạp một lần khi session bắt đầu. Sửa file giữa session thì phải restart session.

### "running scripts is disabled on this system"

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".claude\skills\open-project-for-skills\scripts\check-skills.ps1"
```

Hoặc cho phiên hiện tại: `Set-ExecutionPolicy -Scope Process Bypass`.

### Không ghi được vào `.claude`

Triệu chứng: `mkdir` báo "Access is denied", `dir .claude` báo "Access is denied", owner hiển thị trống trong `dir /a /q`.

Nguyên nhân: folder `.claude` có ACL/owner hỏng (thường do một tiến trình khác tạo với security context khác). Không sửa được nếu không có quyền admin.

Sửa, trong **PowerShell Run as Administrator**:

```powershell
takeown /f "E:\duong-dan\project\.claude" /r /d y
icacls "E:\duong-dan\project\.claude" /reset /t
Remove-Item -Recurse -Force "E:\duong-dan\project\.claude"
```

Sau đó tạo lại thư mục và cài skill.

### `~` không hoạt động trên Windows

`~` chỉ là quy ước shell. PowerShell dùng `$env:USERPROFILE`, cmd dùng `%USERPROFILE%`.

## Xác nhận skill đã nạp

1. Restart session tại đúng root.
2. Mô tả đúng việc cần làm, khớp `description`.
3. Nếu vẫn không chạy, tạo một skill tối giản đúng cấu trúc và thử lại. Skill tối giản chạy được → lỗi nằm ở nội dung skill gốc (frontmatter/description), không phải vị trí folder.
