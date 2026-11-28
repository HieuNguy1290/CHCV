import sqlite3
import time
from types import SimpleNamespace
from unittest.mock import patch

from tuhoc.app.main import Storage
from tuhoc.lessons.upgrade_v2 import GameAppMixin, LearningService
from tuhoc.storage.quiz_draft_store import QuizDraftStore


def test_legacy_draft_migrates_and_new_lessons_keep_separate_drafts():
    db = sqlite3.connect(':memory:')
    try:
        db.execute('''CREATE TABLE quiz_drafts (
            student_id, language, theme, level, questions, answers, elapsed, updated_at,
            PRIMARY KEY(student_id, language, theme, level))''')
        key = (1, 'en', 'family', 1)
        db.execute('INSERT INTO quiz_drafts VALUES (?,?,?,?,?,?,?,?)',
                   (*key, '[{"id":"a","lesson":1}]', '[{"answer":"A","correct":true}]', 6, 'old'))
        db.commit()
        store = QuizDraftStore(db)
        store.save(*key, [{'id': 'b', 'lesson': 2}], [('B', True)], 8, lesson_scope='2')
        store.save(*key, [{'id': 'c'}], [('C', True)], 9)
        assert store.load(*key, lesson_scope='1')['answers'] == [('A', True)]
        assert store.load(*key, lesson_scope='2')['answers'] == [('B', True)]
        assert store.load(*key)['answers'] == [('C', True)]
        store.delete(*key, lesson_scope='1')
        assert store.load(*key, lesson_scope='1') is None
        assert store.load(*key, lesson_scope='2') is not None
    finally:
        db.close()


def test_finish_rolls_back_and_retry_records_once():
    class Quiz(GameAppMixin):
        def layout(self, title):
            return None

        def _quiz_exit_results(self):
            self.recovery_shown = True

    db = Storage(':memory:')
    try:
        quiz = Quiz()
        quiz.db = db
        quiz.lang = 'en'
        quiz.learning = LearningService(db, SimpleNamespace(language='en'))
        quiz.student = {'id': db.add_student('Audit', 1)}
        quiz.s_theme, quiz.s_level, quiz.s_lesson = 'family', 1, 2
        quiz.s_questions = [{'id': key, 'type': 'choice', 'answer': 'A'} for key in ('a', 'b')]
        quiz.s_answers = [(q, 'A', True) for q in quiz.s_questions]
        quiz.s_started = quiz._quiz_timer_started = time.monotonic()
        quiz._save_quiz_draft()
        db.conn.execute("""CREATE TRIGGER block_second BEFORE INSERT ON attempts
            WHEN NEW.exercise_id = 'b' BEGIN SELECT RAISE(ABORT, 'blocked'); END""")
        with patch('tkinter.messagebox.showerror'), patch('tuhoc.exercises.pygame_review_panel.show_review'):
            quiz.session_finish()
            assert quiz.recovery_shown
            assert db.conn.execute('SELECT count(*) FROM attempts').fetchone()[0] == 0
            assert db.conn.execute('SELECT count(*) FROM level_time_records').fetchone()[0] == 0
            assert quiz._draft_store().load(*quiz._draft_key(), lesson_scope='2') is not None
            db.conn.execute('DROP TRIGGER block_second')
            quiz.session_finish()
            quiz.session_finish()
            assert db.conn.execute('SELECT count(*) FROM attempts').fetchone()[0] == 2
            assert db.conn.execute('SELECT count(*) FROM learning_sessions').fetchone()[0] == 1
            assert quiz._draft_store().load(*quiz._draft_key(), lesson_scope='2') is None
    finally:
        db.conn.close()
