"""Keep the best result and the latest attempt for each learner and mode."""
import math

from tuhoc.library.models import LibraryError, record_id


def save_result(connection, student, text_id, mode, score, passed):
    record_id(text_id)
    if mode not in ('read', 'dictation'):
        raise LibraryError('Chế độ luyện tập không hợp lệ.')
    if not isinstance(score, (float, int)) or not math.isfinite(score) or not 0 <= score <= 100:
        raise LibraryError('Điểm phải từ 0 đến 100.')
    with connection:
        connection.execute("""
            INSERT INTO library_progress (student_id, text_id, mode, best_score, attempts, passed, last_at)
            VALUES (?, ?, ?, ?, 1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(student_id, text_id, mode) DO UPDATE SET
                best_score = MAX(library_progress.best_score, excluded.best_score),
                attempts = library_progress.attempts + 1,
                passed = MAX(library_progress.passed, excluded.passed),
                last_at = excluded.last_at
        """, (student, text_id, mode, score, int(bool(passed))))


def results(connection, student, text_id=None):
    if text_id is not None:
        return connection.execute(
            'SELECT * FROM library_progress WHERE student_id=? AND text_id=? ORDER BY mode',
            (student, record_id(text_id)),
        ).fetchall()
    return connection.execute(
        'SELECT * FROM library_progress WHERE student_id=? ORDER BY text_id, mode', (student,),
    ).fetchall()
