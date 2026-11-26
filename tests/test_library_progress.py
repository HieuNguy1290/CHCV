import sqlite3
from contextlib import closing

import pytest

from tuhoc.library.models import LibraryError, new_id
from tuhoc.library.progress import results, save_result


def test_progress_is_per_student_and_mode_and_keeps_best_result(tmp_path):
    db_path = tmp_path / 'progress.sqlite3'
    article = new_id()
    with closing(sqlite3.connect(db_path)) as db:
        db.execute("""
            CREATE TABLE library_progress (
                student_id INTEGER, text_id TEXT, mode TEXT, best_score REAL, attempts INTEGER,
                passed INTEGER, last_at TEXT, PRIMARY KEY(student_id, text_id, mode)
            )
        """)
        save_result(db, 1, article, 'read', 100, True)
        save_result(db, 1, article, 'dictation', 100, True)
        save_result(db, 1, article, 'dictation', 62.5, False)
        save_result(db, 2, article, 'dictation', 90, False)
        for mode, score in (('unknown', 10), ('read', -1), ('read', float('nan'))):
            with pytest.raises(LibraryError):
                save_result(db, 1, article, mode, score, False)

    with closing(sqlite3.connect(db_path)) as db:
        db.row_factory = sqlite3.Row
        alice = {row['mode']: row for row in results(db, 1, article)}
        assert (alice['dictation']['best_score'], alice['dictation']['attempts'],
                alice['dictation']['passed']) == (100, 2, 1)
        assert alice['read']['attempts'] == 1 and alice['read']['last_at']
        bob, = results(db, 2)
        assert (bob['best_score'], bob['attempts'], bob['passed']) == (90, 1, 0)
