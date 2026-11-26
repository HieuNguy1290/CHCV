"""Pictures for flashcard words/meanings and card themes (copied into the app's own folder)."""
import shutil
from pathlib import Path
from uuid import uuid4

ALLOWED = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}


def import_image(source, folder, max_side=1200):
    """Copy a picture into ``folder`` (shrunk to ``max_side``) and return the stored file name.

    The copy means the card keeps working if the original file is moved or deleted.
    Raises ValueError for unsupported or unreadable files.
    """
    source = Path(str(source))
    if source.suffix.lower() not in ALLOWED or not source.is_file():
        raise ValueError('Hãy chọn ảnh PNG, JPG, WebP, GIF hoặc BMP.')
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageOps
    except ImportError:                                  # no Pillow: keep the file as it is
        name = f'{uuid4().hex[:12]}{source.suffix.lower()}'
        shutil.copyfile(source, folder / name)
        return name
    try:
        with Image.open(source) as opened:
            picture = ImageOps.exif_transpose(opened)
            picture.load()
    except Exception as error:
        raise ValueError('Không đọc được ảnh này.') from error
    picture.thumbnail((max_side, max_side))
    has_alpha = picture.mode in ('RGBA', 'LA', 'P') and 'transparency' in picture.info or picture.mode in ('RGBA', 'LA')
    if has_alpha:
        name, picture = f'{uuid4().hex[:12]}.png', picture.convert('RGBA')
    else:
        name, picture = f'{uuid4().hex[:12]}.jpg', picture.convert('RGB')
    picture.save(folder / name, optimize=True)
    return name


def image_path(folder, name):
    """Absolute path of a stored picture, or None when the name is empty/missing."""
    clean = Path(str(name or '')).name
    path = Path(folder) / clean if clean else None
    return path if path is not None and path.is_file() else None


def remove_if_unused(folder, name, in_use):
    """Delete a stored picture unless some word still references it."""
    path = image_path(folder, name)
    if path is not None and not in_use:
        try:
            path.unlink()
        except OSError:
            pass
