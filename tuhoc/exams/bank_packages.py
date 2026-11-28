"""Share the questions and reading groups of one Exam Mode bank lesson."""
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from tuhoc.exams.exam_bank import ExamBank, SUBJECTS, _read, validate_question
from tuhoc.exams.fixed_exam_packages import exam_question_media, staged_exam_media
from tuhoc.storage.question_packages import (
    MAX_ITEMS, _digest, _family, _json, _locked, _status, collect_assets, read_archive, write_archive,
)
from tuhoc.storage.safe_storage import commit_json
from tuhoc.studio.question_layout_store import validate_layout

FORMAT = "tuhoc-exam-bank-v1"


@dataclass
class BankPackage:
    scope: dict
    questions: list
    groups: list
    assets: dict
    family: str
    revision: str


def _scope(subject, grade, lesson):
    if subject not in SUBJECTS or any(not isinstance(value, str) or not value.strip() or len(value) > 200
                                      for value in (grade, lesson)):
        raise ValueError("Môn, lớp hoặc bài trong ngân hàng kiểm tra không hợp lệ.")
    return {"subject": subject, "grade": grade.strip(), "lesson": lesson.strip()}


def _rows(scope, questions, groups, replace):
    if (not isinstance(questions, list) or not isinstance(groups, list)
            or not 0 < len(questions) + len(groups) <= MAX_ITEMS):
        raise ValueError("Gói ngân hàng phải chứa câu hỏi hoặc nhóm bài đọc.")
    singles = [dict(exam_question_media(row, replace), **scope) for row in questions]
    readings = []
    for group in groups:
        if (not isinstance(group, dict) or not isinstance(group.get("questions"), list)
                or not 2 <= len(group["questions"]) <= 10
                or any(not isinstance(group.get(key), str) or not group[key].strip() for key in ("title", "passage"))):
            raise ValueError("Nhóm bài đọc cần tiêu đề, đoạn đọc và 2–10 câu.")
        children = [dict(exam_question_media(child, replace), **scope, type="choice")
                    for child in group["questions"]]
        packed = dict(scope, id=group.get("id"), title=group["title"],
                      passage=group["passage"], questions=children)
        if "layout" in group:
            packed["layout"] = validate_layout(group["layout"])
        readings.append(packed)
    return singles, readings


def _validate(bank, questions, groups):
    for row in [*questions, *(child for group in groups for child in group["questions"])]:
        validate_question(bank._expand_question(row))
        if "layout" in row:
            validate_layout(row["layout"])


def export_bank(path, bank, subject, grade, lesson, questions, groups):
    scope = _scope(subject, grade, lesson)
    assets, collect = collect_assets(
        lambda ref: Path(ref) if Path(ref).is_file() else None,
    )
    questions, groups = _rows(scope, questions, groups, bank._resolve_media)
    _validate(bank, questions, groups)
    questions, groups = _rows(scope, questions, groups, collect)
    questions.sort(key=lambda row: str(row.get("id", "")))
    groups.sort(key=lambda row: str(row.get("id", "")))
    write_archive(path, {"format": FORMAT, "scope": scope,
                         "family": _family(bank.folder, [FORMAT, scope]),
                         "questions": questions, "groups": groups}, assets)


def read_bank(path):
    data, assets = read_archive(path)
    if not isinstance(data, dict) or data.get("format") != FORMAT:
        raise ValueError("Tệp này không phải gói ngân hàng kiểm tra.")
    where = data.get("scope")
    family = data.get("family")
    if (not isinstance(where, dict) or not isinstance(family, str) or len(family) != 64
            or any(char not in "0123456789abcdef" for char in family)):
        raise ValueError("Gói ngân hàng kiểm tra không hợp lệ.")
    scope = _scope(where.get("subject"), where.get("grade"), where.get("lesson"))
    seen = set()

    def check(ref):
        if not isinstance(ref, str) or ref not in assets:
            raise ValueError(f"Gói thiếu tệp đính kèm: {ref}")
        seen.add(ref)
        return ref

    questions, groups = _rows(scope, data.get("questions"), data.get("groups"), check)
    if seen != set(assets):
        raise ValueError("Gói có tệp đính kèm không sử dụng.")
    with TemporaryDirectory() as directory:
        bank = ExamBank(directory)
        with staged_exam_media(bank.media_folder / "preview", assets) as replace:
            _validate(bank, *_rows(scope, questions, groups, replace))
    return BankPackage(scope, questions, groups, assets, family, _digest(_json([scope, questions, groups])))


def bank_status(bank, package):
    return _status(package, bank.questions() + bank.reading_groups())


def import_bank(bank, package, lesson=None, *, allow_update=False):
    with _locked(bank.folder):
        questions = _read(bank.questions_path, [])
        groups = bank.reading_groups()
        if not isinstance(questions, list) or any(not isinstance(row, dict) for row in questions + groups):
            raise ValueError("Ngân hàng kiểm tra hiện tại không hợp lệ.")
        status = _status(package, questions + groups)
        if status == "duplicate":
            return None
        if status == "update" and not allow_update:
            raise ValueError("Hãy xác nhận nhập bản mới thành một mục riêng.")
        scope = dict(package.scope)
        base = (lesson or "").strip() or scope["lesson"]
        used = {name.casefold() for name in bank.lessons(scope["grade"], scope["subject"])}
        candidate = base
        number = 2
        while candidate.casefold() in used:
            candidate = f"{base} ({number})"
            number += 1
        scope = _scope(scope["subject"], scope["grade"], candidate)
        source = {"family": package.family, "revision": package.revision}
        with staged_exam_media(bank.media_folder / f"shared-{uuid4().hex}", package.assets) as replace:
            singles, readings = _rows(scope, package.questions, package.groups, replace)
            for row in singles + readings:
                row.update(id=uuid4().hex, shared_source=source)
            for group in readings:
                for child in group["questions"]:
                    child["id"] = f"{group['id']}:{uuid4().hex[:12]}"
            _validate(bank, singles, readings)
            updates = {}
            if singles:
                updates[bank.questions_path] = questions + singles
            if readings:
                updates[bank.readings_path] = groups + readings
            commit_json(updates)
    return scope
