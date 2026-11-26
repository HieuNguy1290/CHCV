"""Validate the versioned library records while retaining extension fields."""
import re
from datetime import datetime, timezone
from pathlib import PurePosixPath, PureWindowsPath
from unicodedata import normalize
from uuid import uuid4

from tuhoc.library.text_split import split_sentences


SCHEMA_VERSION = '1.0'
SUBJECTS = {'tieng_viet': 'Tiếng Việt', 'tieng_anh': 'Tiếng Anh'}
MEDIA_SUFFIXES = {
    'image': frozenset({'.png', '.jpg', '.jpeg', '.gif', '.webp'}),
    'audio': frozenset({'.mp3', '.wav', '.ogg'}),
}
DEFAULT_ICON = '📚'
DEFAULT_COLOR = '#5269E8'


class LibraryError(ValueError):
    """An invalid record or an unsuccessful library operation."""


def now():
    return datetime.now(timezone.utc).isoformat()


def new_id():
    return uuid4().hex


def record_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-f0-9]{32}', value):
        raise LibraryError('Mã thư viện không hợp lệ.')
    return value


def _string(value, label, limit=None, *, required=True):
    if not isinstance(value, str):
        raise LibraryError(f'{label} phải là văn bản.')
    value = value.strip()
    if required and not value:
        raise LibraryError(f'Cần nhập {label.lower()}.')
    if limit is not None and len(value) > limit:
        raise LibraryError(f'{label} chỉ được tối đa {limit} ký tự.')
    return value


def _object(value, label):
    if not isinstance(value, dict):
        raise LibraryError(f'{label} phải là đối tượng JSON.')
    return value


def _list(value, label):
    if not isinstance(value, list):
        raise LibraryError(f'{label} phải là danh sách.')
    return value


def _subject(value):
    if not isinstance(value, str) or value not in SUBJECTS:
        raise LibraryError('Môn học phải là Tiếng Việt hoặc Tiếng Anh.')
    return value


def check_version(value):
    if value.get('schema_version') != SCHEMA_VERSION:
        raise LibraryError(f'Phiên bản dữ liệu thư viện không được hỗ trợ: {value.get("schema_version")!r}.')


def media_reference(value, kind):
    value = _string(value, 'Đường dẫn media', required=False)
    if not value:
        return ''
    path = PurePosixPath(value)
    windows_path = PureWindowsPath(value)
    if (path.is_absolute() or windows_path.drive or '\\' in value or
            any(part in {'', '.', '..'} for part in value.split('/')) or
            len(path.parts) < 2 or path.parts[0] != 'media' or
            any(':' in part or '\x00' in part or part.endswith((' ', '.'))
                or PureWindowsPath(part).is_reserved() for part in path.parts)):
        raise LibraryError('Đường dẫn tệp phải nằm trong thư mục media của thư viện.')
    if path.suffix.lower() not in MEDIA_SUFFIXES[kind]:
        raise LibraryError('Định dạng ảnh không được hỗ trợ.' if kind == 'image' else
                           'Định dạng âm thanh không được hỗ trợ.')
    return path.as_posix()


def _common(value):
    return {
        'id': record_id(value.get('id')),
        'subject': _subject(value.get('subject')),
        'created_at': _string(value.get('created_at'), 'Ngày tạo'),
        'updated_at': _string(value.get('updated_at'), 'Ngày cập nhật'),
    }


def normalize_topic(value):
    _object(value, 'Chủ đề')
    color = value.get('color', DEFAULT_COLOR)
    if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise LibraryError('Màu chủ đề phải có dạng #RRGGBB.')
    tags = [_string(tag, 'Nhãn') for tag in _list(value.get('tags', []), 'Nhãn')]
    return {
        **value, **_common(value), 'name': _string(value.get('name'), 'Tên chủ đề', 80),
        'icon': _string(value.get('icon', DEFAULT_ICON), 'Biểu tượng'), 'color': color,
        'tags': tags,
    }


def _glossary(value):
    words = []
    seen = set()
    for item in _list(value, 'Từ khó'):
        _object(item, 'Mục từ khó')
        word = _string(item.get('word'), 'Từ')
        key = normalize('NFC', word).casefold()
        if key in seen:
            raise LibraryError(f'Từ khó bị trùng: {word}.')
        seen.add(key)
        words.append({**item, 'word': word, 'meaning': _string(item.get('meaning'), 'Nghĩa')})
    return words


def _dictation(value):
    _object(value, 'Thiết lập chính tả')
    variants = [_string(item, 'Đáp án thay thế')
                for item in _list(value.get('accepted_variants', []), 'Đáp án thay thế')]
    equivalences = []
    for group in _list(value.get('equivalences', []), 'Cách viết tương đương'):
        entries = [_string(item, 'Cách viết tương đương')
                   for item in _list(group, 'Nhóm tương đương')]
        if len(entries) < 2:
            raise LibraryError('Mỗi nhóm tương đương cần ít nhất hai cách viết.')
        equivalences.append(entries)
    return {**value, 'accepted_variants': variants, 'equivalences': equivalences}


def _segments(value):
    segments = []
    for item in _list(value, 'Danh sách câu'):
        _object(item, 'Câu')
        segment = {**item, 'text': _string(item.get('text'), 'Nội dung câu')}
        for key in ('start_ms', 'end_ms'):
            time = item.get(key)
            if time is not None and (type(time) is not int or time < 0):
                raise LibraryError('Mốc thời gian câu phải là số mili giây không âm.')
            segment[key] = time
        if (segment['start_ms'] is not None and segment['end_ms'] is not None and
                segment['start_ms'] > segment['end_ms']):
            raise LibraryError('Mốc kết thúc phải sau mốc bắt đầu.')
        segments.append(segment)
    return segments


def normalize_text(value, *, regenerate_segments=False):
    _object(value, 'Bài viết')
    check_version(value)
    body = _string(value.get('body'), 'Nội dung', 20000)
    level = value.get('level', 1)
    if type(level) is not int or not 1 <= level <= 5:
        raise LibraryError('Mức độ phải là số nguyên từ 1 đến 5.')
    legacy_id = value.get('legacy_id')
    if legacy_id is not None:
        legacy_id = _string(legacy_id, 'Mã dữ liệu cũ')
    if regenerate_segments:
        segments = [{'text': sentence, 'start_ms': None, 'end_ms': None}
                    for sentence in split_sentences(body)]
    else:
        segments = _segments(value.get('segments', []))
    return {
        **value, **_common(value), 'topic_id': record_id(value.get('topic_id')),
        'title': _string(value.get('title'), 'Tiêu đề', 120), 'body': body,
        'image': media_reference(value.get('image', ''), 'image'),
        'audio': media_reference(value.get('audio', ''), 'audio'), 'level': level,
        'glossary': _glossary(value.get('glossary', [])), 'segments': segments,
        'dictation': _dictation(value.get('dictation', {})), 'legacy_id': legacy_id,
    }


def parse_dictation_fields(variants, equivalents):
    answers = [line.strip() for line in variants.splitlines() if line.strip()]
    groups = []
    for line in equivalents.splitlines():
        parts = [part.strip() for part in line.split('|') if part.strip()]
        if len(parts) == 1:
            answers.append(parts[0])
        elif parts:
            groups.append(parts)
    return {'accepted_variants': answers, 'equivalences': groups}
