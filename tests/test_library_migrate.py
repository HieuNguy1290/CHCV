import json

from tuhoc.library.migrate_legacy import migrate_legacy
from tuhoc.library.store import LibraryStore


def test_import_twice_copies_media_and_keeps_sources(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    audio = source / 'old.mp3'
    image = source / 'old.png'
    audio.write_bytes(b'old audio')
    image.write_bytes(b'old image')
    legacy = source / 'dap_an_chinh_ta.json'
    options = {'accepted_variants': ["He's here!"], 'equivalences': [["he's", 'he is']]}
    legacy.write_text(json.dumps({'items': [
        {'id': 'lesson-1', 'title': 'Bài nghe', 'answer': 'He is here.', 'audio': audio.name, **options},
    ]}), encoding='utf-8')
    before = legacy.read_bytes()
    reading = [
        {'theme': 'family', 'level': 12, 'lesson': 1, 'title': 'Bài đọc', 'content': 'Câu một.',
         'image': image.name},
        {'theme': 'family', 'level': 12, 'lesson': 1, 'title': 'Bài đọc', 'content': 'Câu khác.'},
    ]
    store = LibraryStore(tmp_path / 'profile')

    def run():
        return migrate_legacy(store, 'tieng_anh', dictation_file=legacy, reading_rows=reading,
                              image_resolver=lambda reference: source / reference)

    assert run() == {'imported': 3, 'skipped': 0, 'warnings': []}
    assert run() == {'imported': 0, 'skipped': 3, 'warnings': []}
    assert len({article['legacy_id'] for article in store.texts()}) == 3
    assert {topic['name'] for topic in store.topics()} == {'Chính tả cũ', 'Bài đọc giáo trình'}
    listening = next(article for article in store.texts() if article['audio'])
    assert listening['dictation'] == options
    assert store.resolve_media(listening['audio'], 'audio').read_bytes() == audio.read_bytes()
    visual = next(article for article in store.texts() if article['image'])
    assert visual['level'] == 5
    assert store.resolve_media(visual['image'], 'image').read_bytes() == image.read_bytes()
    assert legacy.read_bytes() == before


def test_corrupt_legacy_source_is_reported_without_blocking_other_source(tmp_path):
    legacy = tmp_path / 'dap_an_chinh_ta.json'
    legacy.write_bytes(b'{"items":')
    store = LibraryStore(tmp_path)
    summary = migrate_legacy(store, 'tieng_viet', dictation_file=legacy,
                             reading_rows=[{'title': 'Bài đọc', 'content': 'Câu một.'}])
    assert summary['imported'] == 1
    assert 'Expecting value' in summary['warnings'][0]
    assert legacy.read_bytes() == b'{"items":'
