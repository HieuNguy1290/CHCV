"""Card looks for the flashcard window: colour presets or the student's own picture."""
from pathlib import Path

PRESETS = (
    {'id': 'classic', 'name': 'Trắng', 'face': (255, 255, 255), 'text': (35, 52, 94), 'border': (213, 230, 220)},
    {'id': 'navy', 'name': 'Xanh navy', 'face': (35, 52, 94), 'text': (255, 255, 255), 'border': (96, 120, 180)},
    {'id': 'mint', 'name': 'Bạc hà', 'face': (226, 246, 236), 'text': (26, 84, 60), 'border': (150, 205, 175)},
    {'id': 'peach', 'name': 'Hồng đào', 'face': (255, 232, 226), 'text': (120, 45, 40), 'border': (240, 180, 170)},
    {'id': 'night', 'name': 'Tối', 'face': (33, 37, 48), 'text': (236, 240, 248), 'border': (80, 90, 112)},
)
DEFAULT_ID = 'classic'
CUSTOM_ID = 'custom'


def preset(theme_id):
    return next((p for p in PRESETS if p['id'] == theme_id), None)


def resolve_theme(setting, images_dir):
    """Settings value -> ready-to-draw theme. Anything invalid falls back to 'classic'.

    ``{'id': 'custom', 'image': 'abc.png'}`` becomes ``kind='image'`` with an absolute ``image_path``.
    """
    setting = setting if isinstance(setting, dict) else {}
    if setting.get('id') == CUSTOM_ID:
        name = Path(str(setting.get('image') or '')).name          # never follow a path out of the folder
        path = Path(images_dir) / name if name else None
        if path is not None and path.is_file():
            return {'id': CUSTOM_ID, 'name': 'Ảnh của em', 'kind': 'image', 'image_path': str(path),
                    **{k: preset(DEFAULT_ID)[k] for k in ('face', 'text', 'border')}}
    chosen = preset(setting.get('id')) or preset(DEFAULT_ID)
    return {**chosen, 'kind': 'color', 'image_path': None}


def luminance(rgb):
    """Relative brightness 0..1."""
    r, g, b = (c / 255 for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def tint_for_image(average_rgb):
    """Veil over a picture so the text stays readable: ``(rgb, alpha, text_rgb)``."""
    if luminance(average_rgb) > 0.5:
        return (255, 255, 255), 150, (35, 52, 94)
    return (0, 0, 0), 135, (255, 255, 255)
