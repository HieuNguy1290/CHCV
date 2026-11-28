"""Sharing published fixed exams, including their sections and attachments."""
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from tuhoc.exams.fixed_exam_store import FixedExamStore
from tuhoc.storage.question_packages import (
    _digest, _json, _locked, _status, collect_assets, read_archive, rewrite_media_fields,
    write_archive,
)
from tuhoc.storage.safe_storage import commit_json
from tuhoc.studio.question_layout_store import validate_layout

FORMAT = "tuhoc-fixed-exam-v1"


def exam_question_media(question, replace):
    if not isinstance(question, dict):
        raise ValueError("Câu hỏi trong bộ đề không hợp lệ.")
    copied = rewrite_media_fields(question, replace, ("image", "audio"))
    if "layout" in copied:
        validate_layout(copied["layout"])
    if question.get("type") == "image_multi_choice":
        copied["options"] = [replace(ref) for ref in question.get("options", [])]
        copied["answer"] = replace(question.get("answer"))
    return copied


@contextmanager
def staged_exam_media(media, assets):
    written = []
    filenames = {}
    try:
        if assets:
            media.mkdir(parents=True)
            for number, (ref, payload) in enumerate(sorted(assets.items()), 1):
                name = f"{number}{Path(ref).suffix}"
                filenames[ref] = name
                target = media / name
                written.append(target)
                target.write_bytes(payload)
        yield lambda ref: f"exam_media/{media.name}/{filenames[ref]}"
    except Exception:
        for target in written:
            target.unlink(missing_ok=True)
        if assets and media.is_dir():
            media.rmdir()
        raise


def _with_media(exam, replace):
    prepared = {key: deepcopy(exam.get(key)) for key in ("title", "minutes", "subject", "sections")}
    if not isinstance(prepared["sections"], list):
        raise ValueError("Bộ đề thiếu danh sách các phần.")
    for number, section in enumerate(prepared["sections"]):
        if not isinstance(section, dict) or not isinstance(section.get("questions"), list):
            raise ValueError("Phần của bộ đề không hợp lệ.")
        prepared["sections"][number] = {
            "title": section.get("title", ""), "passage": section.get("passage", ""),
            "questions": [exam_question_media(question, replace) for question in section["questions"]],
        }
    return prepared


def export_exam(path, store, exam):
    source_id = exam.get("id")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("Hãy xuất bản bộ đề trước khi chia sẻ.")
    source = store._prepare(exam)
    assets, collect = collect_assets(lambda ref: Path(ref) if isinstance(ref, str) and Path(ref).is_file() else None)
    document = {"format": FORMAT, "family": _digest(_json([FORMAT, source_id])),
                "exam": _with_media(source, collect)}
    write_archive(path, document, assets)


@dataclass
class ExamPackage:
    exam: dict
    assets: dict
    family: str
    revision: str


def read_exam(path):
    document, assets = read_archive(path)
    if not isinstance(document, dict) or document.get("format") != FORMAT:
        raise ValueError("Tệp này không phải gói Bộ đề TuHoc.")
    family, exam = document.get("family"), document.get("exam")
    if (not isinstance(exam, dict) or not isinstance(family, str) or len(family) != 64
            or any(ch not in "0123456789abcdef" for ch in family)):
        raise ValueError("Thông tin gói bộ đề không hợp lệ.")
    seen = set()

    def check(ref):
        if not isinstance(ref, str) or ref not in assets:
            raise ValueError(f"Gói thiếu tệp đính kèm: {ref}")
        seen.add(ref)
        return ref

    exam = _with_media(exam, check)
    if seen != set(assets):
        raise ValueError("Gói bộ đề có tệp không sử dụng.")
    with TemporaryDirectory() as directory:
        validator = FixedExamStore(directory)
        with staged_exam_media(validator.media_folder / "preview", assets) as replace:
            validator._prepare(_with_media(exam, replace))
    return ExamPackage(exam, assets, family, _digest(_json(exam)))


def exam_status(store, package):
    return _status(package, store.published())


def import_exam(store, package, title=None, *, allow_update=False):
    with _locked(store.folder):
        rows = store.published()
        status = _status(package, rows)
        if status == "duplicate":
            return None
        if status == "update" and not allow_update:
            raise ValueError("Hãy xác nhận nhập bản mới của bộ đề.")
        base_title = (title or "").strip() or package.exam["title"]
        title = base_title
        used = {str(item.get("title", "")).casefold() for item in rows}
        number = 2
        while title.casefold() in used:
            title = f"{base_title} ({number})"
            number += 1
        exam_id = uuid4().hex
        media = store.media_folder / f"shared-{exam_id}"
        with staged_exam_media(media, package.assets) as replace:
            data = _with_media(package.exam, replace)
            data.update(id=exam_id, title=title, shared_source={
                "family": package.family, "revision": package.revision,
            })
            store._prepare(data)
            commit_json({store.folder / f"{exam_id}.json": data})
    return data
