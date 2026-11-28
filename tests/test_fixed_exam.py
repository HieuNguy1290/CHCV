import copy
import json
import sqlite3

import pygame

from tuhoc.exams.exam_bank import ExamBank
from tuhoc.exams.exam_history_bridge import exam_records
from tuhoc.exams.exam_pygame import ExamUI, VIRTUAL
from tuhoc.exams.fixed_exam_page import EXAMPLE
from tuhoc.exams.fixed_exam_store import FixedExamStore


def test_fixed_exams_are_snapshots_in_a_separate_collection(tmp_path):
    store = FixedExamStore(tmp_path)
    store.save_draft('unfinished JSON')
    assert store.published() == []
    first = store.publish(EXAMPLE)
    edited = copy.deepcopy(first)
    edited['sections'][0]['questions'].reverse()
    second = store.publish(edited)
    assert first['id'] != second['id']
    assert store.assemble(first)['questions'][0]['type'] == 'choice'
    assert store.assemble(second)['questions'][0]['type'] == 'fill'
    assert store.read_draft() == 'unfinished JSON'
    assert not ExamBank(tmp_path).questions_path.exists()


def test_fixed_exam_scroll_input_grade_and_preview(tmp_path, monkeypatch):
    monkeypatch.setenv('SDL_VIDEODRIVER', 'dummy')
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_mode(VIRTUAL)
    store = FixedExamStore(tmp_path)
    exam = store.assemble(store.publish(EXAMPLE))
    ui = ExamUI(tmp_path, 1, fixed_exam=exam, preview=True)
    ui.font, ui.bold, ui.big, ui.small = (ui._font(22), ui._font(24, True),
                                        ui._font(36, True), ui._font(18))
    screen = pygame.Surface(VIRTUAL)

    def draw():
        ui.buttons.clear()
        ui._draw_exam(screen)

    try:
        ui._start()
        draw()
        ui._jump(1, focus_child=True)
        draw()
        assert ui.document.offset > 0
        targets = [rect for rect, _ in ui.buttons if ui.read_area.contains(rect)]
        ui._click(targets[1].center)
        assert ui.answers == {'2': 'False'}
        ui._jump(2)
        draw()
        assert ui._input_question()['id'] == '3'
        ui.answers['3'] = 'library'
        ui.document.go_to_passage(ui)
        assert ui.index == 0 and ui.document.offset == 0 and ui._input_question() is None
        ui._jump(0)
        assert ui.answers['2'] == 'False'
        ui._submit()
        assert ui.result['correct'] == 2
        assert not ui.bank.results_path.exists()

        ui.preview = False
        ui._start()
        ui.answers = {'2': 'False', '3': 'library'}
        ui._submit()
        saved = json.loads(ui.bank.results_path.read_text(encoding='utf-8'))
        assert saved[0]['fixed_exam_id'] == exam['fixed_exam_id']
        assert saved[0]['graded_answers'] == {'1': False, '2': True, '3': True}
        with sqlite3.connect(tmp_path / 'student.db') as conn:
            assert exam_records(conn, 1)[0][2].startswith('Bộ đề')
    finally:
        pygame.quit()
