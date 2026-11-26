import json
from pathlib import Path

import pytest

from tuhoc.library.models import LibraryError, new_id
from tuhoc.library.store import LibraryStore


@pytest.fixture
def library(tmp_path):
    store = LibraryStore(tmp_path)
    topic = store.save_topic({'name': 'Gia đình em', 'subject': 'tieng_viet', 'extension': ['giữ']})
    article = {'topic_id': topic['id'], 'title': 'Đi học', 'body': 'Em đi học. Bạn đến lớp!',
               'subject': 'tieng_viet'}
    return store, topic, article


def test_crud_segments_and_cascade(library):
    store, topic, fields = library
    article = store.save_text(fields)
    assert [segment['text'] for segment in article['segments']] == ['Em đi học.', 'Bạn đến lớp!']
    assert all(segment['start_ms'] is None and segment['end_ms'] is None
               for segment in article['segments'])
    changed = store.save_text({'id': article['id'], 'body': 'Bài mới…'})
    assert changed['created_at'] == article['created_at']
    assert [segment['text'] for segment in changed['segments']] == ['Bài mới…']
    assert store.get_text(article['id']) == changed
    assert store.texts(topic['id']) == [changed]
    with pytest.raises(LibraryError, match='còn bài viết'):
        store.delete_topic(topic['id'])
    later = store.save_text({**fields, 'title': 'Bài khác'})
    store.delete_text(later['id'])
    with pytest.raises(LibraryError, match='Không tìm thấy'):
        store.get_text(later['id'])
    store.delete_topic(topic['id'], cascade=True)
    assert store.topics() == store.texts() == []


@pytest.mark.parametrize('changes', [
    {'subject': 'toan'}, {'title': 'a' * 121}, {'body': ''}, {'body': 'x' * 20001},
    {'level': 0}, {'level': True}, {'topic_id': new_id()},
    {'glossary': [{'word': 'Hòa', 'meaning': 'a'}, {'word': 'Ho\u0300a', 'meaning': 'b'}]},
    {'dictation': {'equivalences': [['he is']]}}, {'image': 'photo.png'},
    {'audio': 'media/file.pdf'},
])
def test_invalid_articles(library, changes):
    store, _, fields = library
    with pytest.raises(LibraryError):
        store.save_text({**fields, **changes})
    assert store.texts() == []


def test_invalid_topic_and_traversal(library, tmp_path):
    store, _, fields = library
    with pytest.raises(LibraryError, match='80'):
        store.save_topic({'name': 'x' * 81, 'subject': 'tieng_viet'})
    for path in ('media/../x.png', 'media//x.png', '../x.png', r'media\..\x.png',
                 'C:/media/x.png', 'media/x.png:stream'):
        with pytest.raises(LibraryError):
            store.save_text({**fields, 'image': path})
    with pytest.raises(LibraryError):
        store.get_text('../x')
    outside = tmp_path / 'outside.png'
    outside.write_bytes(b'outside')
    store.media_dir.mkdir()
    try:
        (store.media_dir / 'escape.png').symlink_to(outside)
    except (OSError, NotImplementedError):
        return  # symlinks require an additional privilege on some Windows hosts
    with pytest.raises(LibraryError):
        store.save_text({**fields, 'image': 'media/escape.png'})
    with pytest.raises(LibraryError):
        store.resolve_media('media/escape.png', 'image')


def test_media_copy_and_collision(library, tmp_path):
    store, _, fields = library
    photo = tmp_path / 'ảnh.png'
    photo.write_bytes(b'photo')
    first = store.import_media(photo, 'image')
    second = store.save_text(fields, media={'image': photo})['image']
    assert (first, second) == ('media/ảnh.png', 'media/ảnh_2.png')
    assert store.resolve_media(second, 'image').read_bytes() == photo.read_bytes()
    with pytest.raises(LibraryError):
        store.save_text(fields, media={'image': photo, 'audio': tmp_path / 'missing.wav'})
    assert sorted(path.name for path in store.media_dir.iterdir()) == ['ảnh.png', 'ảnh_2.png']


def test_preserves_extension_fields_and_exact_backup(library):
    store, topic, fields = library
    original_topics = store.topics_file.read_text(encoding='utf-8')
    topic_document = json.loads(original_topics)
    topic_document['meta'] = {'future': True}
    store.topics_file.write_text(json.dumps(topic_document, ensure_ascii=False), encoding='utf-8')
    store.save_topic({'id': topic['id'], 'name': 'Gia đình mới'})
    assert store.topics()[0]['extension'] == ['giữ']
    assert json.loads(store.topics_file.read_text(encoding='utf-8'))['meta'] == {'future': True}
    assert json.loads(store.topics_file.with_suffix('.bak').read_text(encoding='utf-8')) == topic_document

    article = store.save_text({**fields, 'custom': {'next': True}, 'dictation': {'future': 1}})
    path = store.text_dir / f"{article['id']}.json"
    original = path.read_bytes()
    saved = store.save_text({'id': article['id'], 'dictation': {'accepted_variants': ['Bài khác.']}})
    assert saved['custom'] == {'next': True}
    assert saved['dictation']['future'] == 1
    assert path.with_suffix('.bak').read_bytes() == original
    assert 'Đi học' in path.read_text(encoding='utf-8')


def test_corrupt_json_keeps_original(library):
    store, topic, fields = library
    article = store.save_text(fields)
    text_file = store.text_dir / f"{article['id']}.json"
    text_file.write_bytes(b'{broken')
    with pytest.raises(LibraryError, match='Expecting property name'):
        store.save_text({'id': article['id'], 'title': 'Đổi tên'})
    assert text_file.read_bytes() == b'{broken'
    store.topics_file.write_bytes(b'{"topics":')
    with pytest.raises(LibraryError, match='Expecting value'):
        store.save_topic({'id': topic['id'], 'name': 'Đổi tên'})
    assert store.topics_file.read_bytes() == b'{"topics":'


def test_failed_atomic_replace_keeps_text_and_restores_cascade(library, monkeypatch):
    import tuhoc.library.store as library_store

    store, topic, fields = library
    article = store.save_text(fields)
    file = store.text_dir / f"{article['id']}.json"
    original = file.read_bytes()
    replace = library_store.os.replace

    def fail_replace(source, target):
        if Path(target) in (file, store.topics_file) and Path(source).suffix == '.tmp':
            raise PermissionError('không thể thay thế')
        return replace(source, target)

    monkeypatch.setattr(library_store.os, 'replace', fail_replace)
    with pytest.raises(LibraryError, match='không thể thay thế'):
        store.save_text({'id': article['id'], 'title': 'Đổi tên'})
    assert file.read_bytes() == original
    with pytest.raises(LibraryError, match='không thể thay thế'):
        store.delete_topic(topic['id'], cascade=True)
    assert store.get_text(article['id']) == article
    assert not list(store.root.rglob('*.tmp'))


def test_cascade_keeps_recovery_files_when_restore_also_fails(library, monkeypatch):
    from tuhoc.library import store as library_store

    store, topic, fields = library
    article = store.save_text(fields)
    file = store.text_dir / f"{article['id']}.json"
    original = file.read_bytes()
    replace = library_store.os.replace

    def fail_replace(source, target):
        if Path(target) in (file, store.topics_file):
            raise PermissionError('không thể thay thế')
        return replace(source, target)

    monkeypatch.setattr(library_store.os, 'replace', fail_replace)
    with pytest.raises(LibraryError, match='Bản lưu ở .*không thể thay thế'):
        store.delete_topic(topic['id'], cascade=True)
    recovered, = store.root.glob(f'.deleted-*/{file.name}')
    assert recovered.read_bytes() == original
    assert store.topics() == [topic]
