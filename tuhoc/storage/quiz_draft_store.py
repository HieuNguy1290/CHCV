"""Persistent, per-student quiz draft using the existing application SQLite connection."""
import json
import math
from contextlib import nullcontext

class QuizDraftStore:
    def __init__(self, connection):
        self.conn=connection
        columns = self.conn.execute('PRAGMA table_info(quiz_drafts)').fetchall()
        if columns and not any(column[1] == 'lesson_scope' for column in columns):
            with self.conn:
                self.conn.execute('BEGIN')
                self.conn.execute('ALTER TABLE quiz_drafts RENAME TO quiz_drafts_legacy')
                self._create_table()
                rows = self.conn.execute('SELECT * FROM quiz_drafts_legacy').fetchall()
                for student, language, theme, level, questions, answers, elapsed, updated in rows:
                    scope = self._legacy_scope(questions)
                    self.conn.execute('INSERT INTO quiz_drafts VALUES (?,?,?,?,?,?,?,?,?)',
                                      (student, language, theme, level, scope, questions, answers, elapsed, updated))
                self.conn.execute('DROP TABLE quiz_drafts_legacy')
        elif not columns:
            self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE quiz_drafts (
            student_id INTEGER NOT NULL, language TEXT NOT NULL,
            theme TEXT NOT NULL, level INTEGER NOT NULL, lesson_scope TEXT NOT NULL,
            questions TEXT NOT NULL, answers TEXT NOT NULL,
            elapsed REAL NOT NULL DEFAULT 0,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(student_id, language, theme, level, lesson_scope))''')

    @staticmethod
    def _legacy_scope(questions):
        try:
            rows = json.loads(questions)
            lessons = {str(q.get('lesson') or '1').strip() for q in rows if isinstance(q, dict)}
        except (TypeError, ValueError):
            return ''
        return lessons.pop() if len(lessons) == 1 else ''

    def save(self,student_id,language,theme,level,questions,answers,elapsed, *, lesson_scope=''):
        if not isinstance(questions,list) or not isinstance(answers,(list,tuple)) or len(answers)>len(questions):
            raise ValueError('Invalid draft progress')
        payload=[]
        for item in answers:
            if not isinstance(item,(list,tuple)) or len(item)!=2:
                raise ValueError('Invalid draft answer')
            answer,ok=item
            if not isinstance(ok,bool):
                raise ValueError('Invalid correctness flag')
            payload.append({'answer':answer,'correct':ok})
        duration=float(elapsed)
        if not math.isfinite(duration) or duration<0:raise ValueError('Invalid duration')
        with self.conn:
            self.conn.execute('''INSERT INTO quiz_drafts(student_id,language,theme,level,lesson_scope,questions,answers,elapsed)
                VALUES (?,?,?,?,?,?,?,?)
                ON CONFLICT(student_id,language,theme,level,lesson_scope) DO UPDATE SET
                questions=excluded.questions, answers=excluded.answers,
                elapsed=excluded.elapsed, updated_at=CURRENT_TIMESTAMP''',
                (student_id,language,theme,level,lesson_scope,json.dumps(questions,ensure_ascii=False),
                 json.dumps(payload,ensure_ascii=False),max(0.0,duration)))

    def load(self,student_id,language,theme,level, *, lesson_scope=''):
        row=self.conn.execute('''SELECT questions,answers,elapsed FROM quiz_drafts
            WHERE student_id=? AND language=? AND theme=? AND level=? AND lesson_scope=?''',
            (student_id,language,theme,level,lesson_scope)).fetchone()
        if row is None:return None
        try:
            questions=json.loads(row[0]);raw=json.loads(row[1]);elapsed=float(row[2])
        except (TypeError,ValueError,OverflowError) as exc:
            raise ValueError('Corrupt draft') from exc
        if not isinstance(questions,list) or not isinstance(raw,list) or len(raw)>len(questions):
            raise ValueError('Corrupt draft')
        answers=[]
        for item in raw:
            if not isinstance(item,dict) or 'answer' not in item:raise ValueError('Corrupt answer')
            if not isinstance(item.get('correct'),bool):raise ValueError('Corrupt correctness flag')
            answers.append((item['answer'],item['correct']))
        if not math.isfinite(elapsed) or elapsed<0:raise ValueError('Invalid duration')
        return {'questions':questions,'answers':answers,'elapsed':max(0.0,elapsed)}

    def delete(self,student_id,language,theme,level, *, lesson_scope='', commit=True):
        with self.conn if commit else nullcontext():
            self.conn.execute('DELETE FROM quiz_drafts WHERE student_id=? AND language=? AND theme=? AND level=? AND lesson_scope=?',
                              (student_id,language,theme,level,lesson_scope))
