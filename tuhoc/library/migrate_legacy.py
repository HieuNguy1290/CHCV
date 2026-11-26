"""Read old dictation and curriculum records without writing to their sources."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from tuhoc.library.models import LibraryError, media_reference


DICTATION_TOPIC = 'Chính tả cũ'
READING_TOPIC = 'Bài đọc giáo trình'


def _legacy_id(subject, source, key):
    data = json.dumps(key, ensure_ascii=False, sort_keys=True).encode('utf-8')
    return f'{source}:{subject}:{hashlib.sha256(data).hexdigest()}'


def load_legacy_dictation(path):
    if path is None:
        return []
    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding='utf-8-sig'))
        if not isinstance(payload, dict) or not isinstance(payload.get('items'), list):
            raise ValueError('items phải là danh sách.')
        return payload['items']
    except (OSError, ValueError, RecursionError) as exc:
        raise LibraryError(f'Không đọc được {path.name}: {exc}') from exc


def check_reading_source(path):
    """Surface parse errors hidden by the curriculum's legacy fallback."""
    if not path.exists():
        return
    try:
        if not isinstance(json.loads(path.read_text(encoding='utf-8-sig')), list):
            raise ValueError('Dữ liệu phải là danh sách.')
    except (OSError, ValueError, RecursionError) as exc:
        raise LibraryError(f'Không đọc được {path.name}: {exc}') from exc


def migrate_legacy(store, subject, *, dictation_file=None, reading_rows=(), image_resolver=None):
    """Import independently usable rows. Return counts and concrete skipped-row details."""
    summary = {'imported': 0, 'skipped': 0, 'warnings': []}
    topics = {topic['name']: topic['id'] for topic in store.topics() if topic['subject'] == subject}
    seen = {text['legacy_id'] for text in store.texts() if text['legacy_id']}
    try:
        dictation = load_legacy_dictation(dictation_file)
    except LibraryError as exc:
        summary['warnings'].append(str(exc))
        dictation = []
    reading_occurrences = Counter()
    for source, name, rows, body_field, kind in (
        ('dictation', DICTATION_TOPIC, dictation, 'answer', 'audio'),
        ('reading', READING_TOPIC, reading_rows, 'content', 'image'),
    ):
        for index, row in enumerate(rows, 1):
            try:
                if not isinstance(row, dict):
                    raise LibraryError('Dòng phải là đối tượng JSON.')
                if source == 'dictation':
                    key = row.get('id')
                    if not isinstance(key, str) or not key.strip():
                        raise LibraryError('Thiếu mã bài chính tả.')
                else:
                    fields = tuple(str(row.get(field, '')) for field in ('theme', 'level', 'lesson', 'title'))
                    reading_occurrences[fields] += 1
                    key = [*fields, reading_occurrences[fields]]
                legacy_id = _legacy_id(subject, source, key)
                if legacy_id in seen:
                    summary['skipped'] += 1
                    continue
                text = {
                    'subject': subject, 'title': row.get('title'), 'body': row.get(body_field),
                    'legacy_id': legacy_id,
                }
                if source == 'dictation':
                    text['dictation'] = {field: row.get(field, [])
                                        for field in ('accepted_variants', 'equivalences')}
                else:
                    try:
                        text['level'] = min(5, max(1, int(row.get('level', 1))))
                    except (ValueError, TypeError, OverflowError):
                        text['level'] = 1
                if name not in topics:
                    topics[name] = store.save_topic({'name': name, 'subject': subject})['id']
                text['topic_id'] = topics[name]
                media = {}
                reference = row.get(kind)
                if reference:
                    try:
                        if kind == 'audio':
                            path = Path(dictation_file).parent / Path(reference)
                        else:
                            path = image_resolver(reference) if image_resolver else None
                        if path is None or not Path(path).is_file():
                            raise LibraryError(f'Không tìm thấy tệp: {reference}.')
                        media_reference(f'media/{Path(path).name}', kind)
                        media[kind] = path
                    except (LibraryError, TypeError, OSError) as exc:
                        summary['warnings'].append(f'{name}, dòng {index}: {exc}')
                store.save_text(text, media=media)
                seen.add(legacy_id)
                summary['imported'] += 1
            except LibraryError as exc:
                summary['skipped'] += 1
                summary['warnings'].append(f'{name}, dòng {index}: {exc}')
    return summary
