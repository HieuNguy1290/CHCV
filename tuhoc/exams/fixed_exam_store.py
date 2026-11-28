"""Published fixed exams and their media, independent of the question bank."""

import copy
import uuid
from pathlib import Path

from tuhoc.exams.exam_bank import SUBJECTS, ExamBank, _atomic, _read, validate_question


class FixedExamStore(ExamBank):
    def __init__(self, root):
        super().__init__(root)
        self.folder = self.folder / 'fixed_exams'
        self.media_folder = self.folder / 'exam_media'

    def published(self):
        return [_read(path, {}) for path in sorted(self.folder.glob('*.json')) if path.stem != 'draft']

    def read_draft(self):
        return _read(self.folder / 'draft.json', '')

    def save_draft(self, text):
        _atomic(self.folder / 'draft.json', text)

    def _prepare(self, data):
        if not isinstance(data, dict):
            raise ValueError('Bộ đề phải là một object JSON.')
        title = str(data.get('title', '')).strip()
        minutes = data.get('minutes')
        sections = data.get('sections')
        if not title or type(minutes) is not int or not 1 <= minutes <= 240:
            raise ValueError('Cần tiêu đề và thời lượng nguyên từ 1 đến 240 phút.')
        if not isinstance(sections, list) or not sections:
            raise ValueError('Cần ít nhất một phần trong bộ đề.')
        subject = data.get('subject', 'tieng_anh')
        if not isinstance(subject, str) or subject not in SUBJECTS:
            raise ValueError('Môn học không hợp lệ.')
        source = copy.deepcopy(data)
        for number, section in enumerate(source['sections'], 1):
            if not isinstance(section, dict) or not isinstance(section.get('questions'), list) or not section['questions']:
                raise ValueError(f'Phần {number} cần có ít nhất một câu hỏi.')
            for index, question in enumerate(section['questions']):
                if not isinstance(question, dict):
                    raise ValueError('Câu hỏi phải là object JSON.')
                question.update(subject=subject, grade='1', lesson=title)
                question.setdefault('difficulty', 1)
                try:
                    section['questions'][index] = validate_question(self._expand_question(question))
                except (TypeError, ValueError, KeyError) as exc:
                    raise ValueError(f'Phần {number}, câu {index+1}: {exc}') from exc
        if sum(len(section['questions']) for section in source['sections']) > 50:
            raise ValueError('Bộ đề hỗ trợ tối đa 50 câu.')
        source.update(title=title, minutes=minutes, subject=subject)
        return source

    def publish(self, data):
        source = self._prepare(data)
        for section in source['sections']:
            section['questions'] = [self._pack_question(q) for q in section['questions']]
        source['id'] = uuid.uuid4().hex
        self.folder.mkdir(parents=True, exist_ok=True)
        _atomic(self.folder / (source['id'] + '.json'), source)
        return source

    def assemble(self, data):
        source = self._prepare(data)
        questions = []
        for section in source['sections']:
            for offset, question in enumerate(section['questions']):
                question = dict(question, id=str(len(questions) + 1))
                question.pop('reading_group', None)
                if offset == 0:
                    question['fixed_section'] = str(section.get('title', ''))
                    question['fixed_passage'] = str(section.get('passage', ''))
                questions.append(question)
        return {'id': uuid.uuid4().hex, 'fixed_exam_id': source.get('id'),
                'title': source['title'], 'subject': source['subject'], 'grade': '1',
                'lesson': source['title'], 'level': 1, 'minutes': source['minutes'],
                'questions': questions}
