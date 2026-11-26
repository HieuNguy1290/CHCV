"""Versioned local storage for topics, texts, and their media."""
import json
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

from tuhoc.library.models import (
    MEDIA_SUFFIXES, SCHEMA_VERSION, LibraryError,
    check_version, media_reference, new_id, normalize_text, normalize_topic, now,
    record_id,
)


def _read_json(path):
    try:
        payload = json.loads(path.read_text(encoding='utf-8'), parse_constant=_invalid_constant)
        if not isinstance(payload, dict):
            raise LibraryError('Cần một đối tượng JSON.')
        check_version(payload)
        return payload
    except (OSError, ValueError, RecursionError) as exc:
        raise LibraryError(f'Không đọc được {path.name}: {exc}') from exc


def _invalid_constant(value):
    raise ValueError(f'Giá trị JSON không hợp lệ: {value}.')


def _replace_file(target, write):
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f'.{target.name}.',
                                     suffix='.tmp', delete=False) as stream:
        temporary = Path(stream.name)
        try:
            write(stream)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def _write_json(path, payload):
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    if not path.is_file():
        _replace_file(path, lambda stream: stream.write(encoded))
        return
    backup = path.with_suffix('.bak')
    if backup.is_symlink():
        raise LibraryError(f'Tệp sao lưu là liên kết: {backup.name}.')
    previous_backup = backup.read_bytes() if backup.exists() else None
    original = path.read_bytes()
    _replace_file(backup, lambda stream: stream.write(original))
    try:
        _replace_file(path, lambda stream: stream.write(encoded))
    except BaseException:
        if previous_backup is None:
            backup.unlink()
        else:
            _replace_file(backup, lambda stream: stream.write(previous_backup))
        raise


def _updated(existing, changes):
    timestamp = now()
    merged = {**existing, **changes, 'created_at': existing.get('created_at', timestamp),
              'updated_at': timestamp}
    return merged


class LibraryStore:
    def __init__(self, data_dir):
        self.root = Path(data_dir).resolve() / 'library'
        self.topics_file = self.root / 'topics.json'
        self.text_dir = self.root / 'texts'
        self.media_dir = self.root / 'media'

    def _check_location(self, path):
        if (self.root.resolve() != self.root or path.is_symlink()
                or not path.resolve().is_relative_to(self.root)):
            raise LibraryError(f'Đường dẫn nằm ngoài thư viện: {path.name}.')

    @contextmanager
    def _locked(self):
        """Serialize mutations and readers so a cascade is never seen halfway through."""
        try:
            guard = self.root / '.lock'
            self._check_location(guard)
            self.root.mkdir(parents=True, exist_ok=True)
            with guard.open('a+b') as lock:
                if os.name == 'nt':
                    import msvcrt
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock, fcntl.LOCK_EX)
                yield
        except (OSError, TypeError, ValueError, RuntimeError, RecursionError) as exc:
            if isinstance(exc, LibraryError):
                raise
            raise LibraryError(f'Không thể cập nhật hoặc đọc thư viện: {exc}') from exc

    def _topics_document(self):
        self._check_location(self.topics_file)
        if not self.topics_file.exists():
            return {'schema_version': SCHEMA_VERSION, 'topics': []}
        document = _read_json(self.topics_file)
        try:
            if not isinstance(document.get('topics'), list):
                raise LibraryError('Danh sách chủ đề không hợp lệ.')
            topics = [normalize_topic(topic) for topic in document['topics']]
            if len({topic['id'] for topic in topics}) != len(topics):
                raise LibraryError('Có mã chủ đề bị trùng.')
        except LibraryError as exc:
            raise LibraryError(f'Không đọc được {self.topics_file.name}: {exc}') from exc
        return {**document, 'topics': topics}

    def topics(self):
        with self._locked():
            return self._topics_document()['topics']

    def save_topic(self, topic):
        with self._locked():
            document = self._topics_document()
            topics = document['topics']
            topic_id = record_id(topic['id']) if 'id' in topic else new_id()
            saved = next((entry for entry in topics if entry['id'] == topic_id), {})
            updated = normalize_topic(_updated(saved, {**topic, 'id': topic_id}))
            if saved:
                topics[topics.index(saved)] = updated
            else:
                topics.append(updated)
            _write_json(self.topics_file, document)
            return updated

    def _text_path(self, text_id):
        path = self.text_dir / f'{record_id(text_id)}.json'
        self._check_location(path)
        return path

    def _read_text(self, path):
        self._check_location(path)
        text = _read_json(path)
        try:
            text = normalize_text(text)
            if text['id'] != path.stem:
                raise LibraryError('Mã bài viết không khớp tên tệp.')
            for kind in MEDIA_SUFFIXES:
                self._media_path(text[kind], kind)
            return text
        except LibraryError as exc:
            raise LibraryError(f'Không đọc được {path.name}: {exc}') from exc

    def _texts(self, topic_ids):
        self._check_location(self.text_dir)
        texts = [self._read_text(path) for path in sorted(self.text_dir.glob('*.json'))]
        if any(text['topic_id'] not in topic_ids for text in texts):
            raise LibraryError('Có bài viết tham chiếu đến chủ đề không tồn tại.')
        return sorted(texts, key=lambda text: (text['created_at'], text['id']))

    def texts(self, topic_id=None):
        if topic_id is not None:
            record_id(topic_id)
        with self._locked():
            topic_ids = {topic['id'] for topic in self._topics_document()['topics']}
            return [text for text in self._texts(topic_ids)
                    if topic_id is None or text['topic_id'] == topic_id]

    def get_text(self, text_id):
        with self._locked():
            topics = self._topics_document()['topics']
            path = self._text_path(text_id)
            if not path.exists():
                raise LibraryError('Không tìm thấy bài viết.')
            text = self._read_text(path)
            if not any(topic['id'] == text['topic_id'] for topic in topics):
                raise LibraryError('Chủ đề của bài viết không tồn tại.')
            return text

    def save_text(self, text, *, media=None):
        with self._locked():
            topics = self._topics_document()['topics']
            text_id = record_id(text['id']) if 'id' in text else new_id()
            path = self._text_path(text_id)
            saved = self._read_text(path) if path.exists() else {}
            changes = {**text, 'id': text_id, 'schema_version': SCHEMA_VERSION}
            if 'dictation' in changes and isinstance(changes['dictation'], dict):
                changes['dictation'] = {**saved.get('dictation', {}), **changes['dictation']}
            data = _updated(saved, changes)
            body = data.get('body')
            body_changed = not saved or (isinstance(body, str) and body.strip() != saved['body'])
            updated = normalize_text(data, regenerate_segments=body_changed)
            topic_ids = {topic['id'] for topic in topics}
            if updated['topic_id'] not in topic_ids:
                raise LibraryError('Chủ đề của bài viết không tồn tại.')
            if updated['legacy_id'] and updated['legacy_id'] != saved.get('legacy_id'):
                if any(entry['legacy_id'] == updated['legacy_id'] for entry in self._texts(topic_ids)):
                    raise LibraryError('Bài từ dữ liệu cũ đã được nhập.')
            for kind in MEDIA_SUFFIXES:
                self._media_path(updated[kind], kind)
            path.parent.mkdir(parents=True, exist_ok=True)
            imported = []
            try:
                for kind, source in (media or {}).items():
                    reference = self._import_media(source, kind)
                    imported.append(self.root / reference)
                    updated[kind] = reference
                _write_json(path, updated)
            except BaseException:
                for file in imported:
                    file.unlink()
                raise
            return updated

    def delete_text(self, text_id):
        with self._locked():
            path = self._text_path(text_id)
            if not path.exists():
                raise LibraryError('Không tìm thấy bài viết.')
            self._read_text(path)
            path.unlink()

    def delete_topic(self, topic_id, cascade=False):
        record_id(topic_id)
        with self._locked():
            document = self._topics_document()
            topics = document['topics']
            if not any(topic['id'] == topic_id for topic in topics):
                raise LibraryError('Không tìm thấy chủ đề.')
            texts = [entry for entry in self._texts({topic['id'] for topic in topics})
                     if entry['topic_id'] == topic_id]
            if texts and not cascade:
                raise LibraryError('Chủ đề còn bài viết. Hãy xác nhận xóa cả chủ đề và các bài.')
            document['topics'] = [topic for topic in topics if topic['id'] != topic_id]
            staging = Path(tempfile.mkdtemp(prefix='.deleted-', dir=self.root))
            moved = []
            try:
                for entry in texts:
                    path = self._text_path(entry['id'])
                    archived = staging / path.name
                    path.replace(archived)
                    moved.append((path, archived))
                _write_json(self.topics_file, document)
            except BaseException:
                try:
                    for path, archived in reversed(moved):
                        archived.replace(path)
                except OSError as exc:
                    raise LibraryError(f'Không khôi phục được bài viết. Bản lưu ở {staging}: {exc}') from exc
                staging.rmdir()
                raise
            shutil.rmtree(staging)

    def _media_path(self, value, kind):
        reference = media_reference(value, kind)
        if not reference:
            return None
        self._check_location(self.media_dir)
        path = self.root / reference
        if self.media_dir.resolve() != self.media_dir or not path.resolve().is_relative_to(self.media_dir):
            raise LibraryError('Tệp không nằm trong thư mục media của thư viện.')
        return path

    def resolve_media(self, value, kind):
        try:
            path = self._media_path(value, kind)
            if path is not None and not path.is_file():
                raise LibraryError(f'Không tìm thấy tệp media: {value}.')
            return path
        except (OSError, RuntimeError) as exc:
            raise LibraryError(f'Không mở được tệp media: {exc}') from exc

    def _import_media(self, src_path, kind):
        if kind not in MEDIA_SUFFIXES:
            raise LibraryError('Loại media không hợp lệ.')
        source = Path(src_path)
        if not source.is_file():
            raise LibraryError(f'Không tìm thấy tệp: {source}.')
        media_reference(f'media/{source.name}', kind)
        self._check_location(self.media_dir)
        if self.media_dir.resolve() != self.media_dir:
            raise LibraryError('Tệp không nằm trong thư mục media của thư viện.')
        self.media_dir.mkdir(parents=True, exist_ok=True)
        target = self.media_dir / source.name
        index = 2
        while target.exists() or target.is_symlink():
            target = self.media_dir / f'{source.stem}_{index}{source.suffix}'
            index += 1
        with source.open('rb') as original:
            _replace_file(target, lambda stream: shutil.copyfileobj(original, stream))
        return f'media/{target.name}'

    def import_media(self, src_path, kind):
        with self._locked():
            return self._import_media(src_path, kind)
