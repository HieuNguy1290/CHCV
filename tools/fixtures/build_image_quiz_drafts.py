"""Scan a local lesson and package reviewed vision-agent output as TuHoc drafts."""
import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path

from mutagen.mp3 import MP3
from PIL import Image

from tuhoc.storage.safe_storage import commit_json


def scan(source):
    files = sorted(path for path in source.iterdir() if path.is_file())
    audio = {unicodedata.normalize('NFC', path.stem).casefold(): path
             for path in files if path.suffix.casefold() == '.mp3'}
    rows = {}
    for path in files:
        stem = unicodedata.normalize('NFC', path.stem).casefold()
        match = re.fullmatch(r'câu (\d+)', stem)
        if path.suffix.casefold() != '.png' or not match:
            continue
        number = int(match[1])
        if number in rows:
            raise ValueError(f'Hai ảnh có cùng số câu {number}.')
        sound = audio.get(stem)
        with Image.open(path) as image:
            image.verify()
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        rows[number] = {'number': number, 'image': path.name, 'audio': sound.name if sound else None,
                        'sha256': digest}
    return [rows[key] for key in sorted(rows)]


def crop(source, destination, box):
    with Image.open(source) as image:
        if len(box) != 4 or any(type(value) is not int for value in box):
            raise ValueError(f'Vùng cắt cần bốn tọa độ nguyên: {box!r}')
        x1, y1, x2, y2 = box
        if not (0 <= x1 < x2 <= image.width and 0 <= y1 < y2 <= image.height):
            raise ValueError(f'Vùng cắt nằm ngoài ảnh {source.name}: {box!r}')
        image.crop(box).save(destination)


def select_answer(choices, index):
    if type(index) is not int or not 0 <= index < len(choices):
        raise ValueError('Chỉ số đáp án không khớp các lựa chọn.')
    return choices[index]


def build(source, destination, drafts, theme, level, lesson):
    scanned = scan(source)
    if not scanned:
        raise ValueError('Không tìm thấy ảnh theo mẫu câu N.png.')
    drafts_by_number = {draft['number']: draft for draft in drafts}
    if len(drafts_by_number) != len(drafts) or set(drafts_by_number) != {row['number'] for row in scanned}:
        raise ValueError('Agent phải trả đúng một bản nháp cho mỗi ảnh đã quét.')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', theme) or min(level, lesson) < 1:
        raise ValueError('Mã chủ đề, Level hoặc Lesson không hợp lệ.')
    destination.mkdir(parents=True, exist_ok=False)
    media = destination / 'media'
    media.mkdir()
    questions, review = [], []
    for row in scanned:
        draft = drafts_by_number[row['number']]
        number = row['number']
        prefix = f'{theme}-L{level}-B{lesson}-Q{number}'
        if draft['answer_index'] is None:
            review.append({**row, 'id': prefix, 'status': 'blocked', 'notes': draft['review']})
            continue
        image_path = source / row['image']
        question = {'id': prefix, 'theme': theme, 'level': level, 'lesson': lesson,
                    'type': draft['type'], 'prompt': draft['prompt'],
                    'schema_version': '2.0', 'accepted_answers': []}
        if question['type'] in ('listening_image_choice', 'listening_choice'):
            if not row['audio']:
                review.append({**row, 'id': prefix, 'status': 'blocked',
                               'notes': 'Thiếu MP3 cùng tên.'})
                continue
            question['audio'] = f'{prefix}.mp3'
            audio_path = source / row['audio']
            row['audio_seconds'] = round(MP3(audio_path).info.length, 2)
            shutil.copyfile(audio_path, media / question['audio'])
        if draft.get('crop'):
            question['image'] = f'{prefix}.png'
            crop(image_path, media / question['image'], draft['crop'])
        if question['type'] == 'image_sentence_fill':
            options = draft['options']
            if len(re.findall(r'\.{3,}', draft['blank_text'])) != 1 or len(set(options)) < 2:
                raise ValueError(f'Câu {number} cần một ô trống và ít nhất hai lựa chọn.')
            answer = select_answer(options, draft['answer_index'])
            question.update(blank_text=draft['blank_text'], options=options,
                            blank_answers=[answer], answer=answer,
                            distractors=[option for option in options if option != answer])
        elif question['type'] in ('choice', 'picture_choice', 'listening_choice'):
            options = draft['options']
            if (not isinstance(options, list) or len(options) < 2
                    or any(not isinstance(option, str) or not option.strip() for option in options)
                    or len(set(options)) != len(options)):
                raise ValueError(f'Câu {number} cần ít nhất hai lựa chọn chữ khác nhau.')
            if question['type'] == 'picture_choice' and 'image' not in question:
                raise ValueError(f'Câu {number} cần hình minh họa.')
            question.update(options=options, answer=select_answer(options, draft['answer_index']))
        elif question['type'] in ('image_multi_choice', 'listening_image_choice'):
            if not 2 <= len(draft['choices']) <= 6:
                raise ValueError(f'Câu {number} cần từ hai đến sáu ảnh đáp án.')
            choices = []
            for index, choice in enumerate(draft['choices']):
                name = f'{prefix}-option-{index + 1}.png'
                crop(image_path, media / name, choice['crop'])
                choices.append({'image': name, 'label': choice['label']})
            question.update(image_options=choices, answer=select_answer(choices, draft['answer_index'])['image'])
        else:
            raise ValueError(f'Dạng chưa hỗ trợ: {question["type"]}')
        questions.append(question)
        review.append({**row, 'id': prefix, 'status': 'needs_review', 'notes': draft['review']})
    commit_json({destination / 'level_questions.json': questions,
                 destination / 'review.json': review})
    return review


def publish(package, subject, approved):
    """Append selected drafts to one subject bank, preserving existing rows."""
    subject = subject.resolve()
    library = subject / 'content_library'
    bank = library / 'level_questions.json'
    themes = json.loads((library / 'themes.json').read_text(encoding='utf-8-sig'))
    theme_codes = {row['code'] for row in themes}
    original = bank.read_bytes()
    existing = json.loads(original.decode('utf-8-sig'))
    drafts = {row['id']: row for row in json.loads(
        (package / 'level_questions.json').read_text(encoding='utf-8'))}
    review = {row['number']: row for row in json.loads(
        (package / 'review.json').read_text(encoding='utf-8'))}
    known = {row['id']: row for row in existing if 'id' in row}
    additions, skipped, media_files = [], [], {}

    def media_ref(name):
        if not name or Path(name).name != name or '/' in name or '\\' in name:
            raise ValueError(f'Tên media không hợp lệ: {name!r}')
        source = package / 'media' / name
        if not source.is_file():
            raise ValueError(f'Thiếu media: {name}')
        target = library / 'media' / name
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError(f'Trùng tên media với nội dung khác: {name}')
        media_files[target] = source
        return f'media/{name}'

    for number in dict.fromkeys(approved):
        item = review.get(number)
        if not item or item['status'] != 'needs_review' or item['id'] not in drafts:
            raise ValueError(f'Câu {number} chưa đủ điều kiện nhập.')
        row = drafts[item['id']]
        if row['theme'] not in theme_codes:
            raise ValueError(f'Không tìm thấy mã chủ đề {row["theme"]} trong môn đã chọn.')
        for field in ('image', 'audio'):
            if row.get(field):
                row[field] = media_ref(row[field])
        if row.get('image_options'):
            row['answer'] = media_ref(row['answer'])
            for option in row['image_options']:
                option['image'] = media_ref(option['image'])
        previous = known.get(row['id'])
        if previous is None:
            additions.append(row)
        elif previous == row:
            skipped.append(row['id'])
        else:
            raise ValueError(f'Mã câu đã có nội dung khác: {row["id"]}')

    created = []
    backup = None
    try:
        (library / 'media').mkdir(exist_ok=True)
        for target, source in media_files.items():
            if not target.exists():
                with target.open('xb') as output:
                    created.append(target)
                    with source.open('rb') as input_file:
                        shutil.copyfileobj(input_file, output)
            elif target.read_bytes() != source.read_bytes():
                raise ValueError(f'Media đã thay đổi: {target.name}')
        if bank.read_bytes() != original:
            raise ValueError('Ngân hàng vừa thay đổi. Hãy chạy lại lệnh nhập.')
        if additions:
            backup = commit_json({bank: existing + additions})
    except Exception:
        for file in created:
            file.unlink(missing_ok=True)
        raise
    return {'added': [row['id'] for row in additions], 'already_present': skipped,
            'backup': str(backup) if backup else None}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('source', type=Path)
    cli.add_argument('--drafts', type=Path, help='JSON do vai dựng câu và đối chiếu cung cấp')
    cli.add_argument('--output', type=Path)
    cli.add_argument('--theme')
    cli.add_argument('--level', type=int)
    cli.add_argument('--lesson', type=int)
    cli.add_argument('--publish-to', type=Path, help='Thư mục môn đích khi source là gói nháp')
    cli.add_argument('--approve', type=int, nargs='+', help='Các số câu đã được xác nhận')
    args = cli.parse_args()
    if args.publish_to is not None:
        if not args.approve or args.drafts is not None:
            cli.error('--publish-to cần --approve và nhận gói nháp làm source')
        result = publish(args.source, args.publish_to, args.approve)
    elif args.approve:
        cli.error('--approve chỉ dùng cùng --publish-to')
    elif args.drafts is None:
        result = scan(args.source)
    else:
        if None in (args.output, args.theme, args.level, args.lesson):
            cli.error('--drafts cần --output, --theme, --level và --lesson')
        result = build(args.source, args.output, json.loads(args.drafts.read_text(encoding='utf-8')),
                       args.theme, args.level, args.lesson)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
