from pathlib import Path

from PIL import Image

from tuhoc.exams import bank_packages, fixed_exam_packages
from tuhoc.exams.exam_bank import ExamBank
from tuhoc.exams.fixed_exam_store import FixedExamStore
from tuhoc.lessons.level_flow import save_rows
from tuhoc.lessons.unified_subjects import subject_image
from tuhoc.lessons.upgrade_v2 import Curriculum
from tuhoc.storage import question_packages


def test_full_lesson_topic_round_trip_without_quiz(tmp_path):
    source = tmp_path / "A" / "tieng_viet"
    target = tmp_path / "B" / "tieng_viet"
    topic = {"code": "animals", "title": "Động vật", "max_level": 3, "default_lessons": 4}
    base = {"theme": "animals", "level": 2, "lesson": 3}
    save_rows(target, "lessons", [{**base, "title": "Bài cũ", "content": "B đã soạn"}])
    image = tmp_path / "cat.png"
    Image.new("RGB", (2, 2), "green").save(image)
    content = {
        "lessons": [{**base, "title": "Mèo", "content": "Nội dung"}],
        "blocks": [{**base, "order": 1, "layout": "image_children", "image": "cat.png",
                    "children": [{"id": "child-1", "title": "Thú cưng", "content": "Mèo nhà"}]}],
        "vocab": [{**base, "word": "mèo", "meaning": "thú cưng"}],
        "reading": [{**base, "title": "Con mèo", "content": "Con mèo đang ngủ."}],
    }
    path = tmp_path / "course.tuhoc-pack"
    question_packages.export_package(path, source, "vi", ["lessons", "animals"],
                                     "Động vật", "A", [], lambda _: image,
                                     topic=topic, lesson_content=content)
    package = question_packages.read_package(path)
    count, code = question_packages.import_topic_package(package, target, "vi", topic_title="Bài của A")
    assert count == 4
    curriculum = Curriculum(target)
    assert curriculum.get("lessons", "animals", 2)[0]["title"] == "Bài cũ"
    assert curriculum.get("lessons", code, 2)[0]["lesson"] == 3
    block = curriculum.get("blocks", code, 2)[0]
    assert block["children"][0]["content"] == "Mèo nhà"
    assert subject_image(target, block["image"]).read_bytes() == image.read_bytes()
    assert curriculum.get("vocab", code, 2)[0]["word"] == "mèo"
    assert curriculum.get("reading", code, 2)[0]["title"] == "Con mèo"
    assert question_packages.import_topic_package(package, target, "vi") == (0, None)


def _question(**changes):
    return dict({"type": "choice", "prompt": "Pick the answer", "options": ["A", "B"],
                 "answer": "A", "subject": "tieng_anh", "grade": "1",
                 "lesson": "Practice", "difficulty": 2}, **changes)


def test_fixed_exam_package_preserves_passage_media_and_other_exams(tmp_path):
    source = FixedExamStore(tmp_path / "A")
    target = FixedExamStore(tmp_path / "B")
    image = tmp_path / "exam.png"
    Image.new("RGB", (2, 2), "blue").save(image)
    exam = {
        "title": "Practice", "minutes": 12, "subject": "tieng_anh",
        "sections": [{"title": "Reading", "passage": "An exam passage",
                      "questions": [_question(type="picture_choice", image=str(image))]}],
    }
    original = target.publish(exam)
    path = tmp_path / "exam.tuhoc-pack"
    fixed_exam_packages.export_exam(path, source, source.publish(exam))
    package = fixed_exam_packages.read_exam(path)
    added = fixed_exam_packages.import_exam(target, package, "Practice")
    assert added["title"] == "Practice (2)"
    assert added["id"] != original["id"]
    assert len(target.published()) == 2
    assembled = target.assemble(added)
    assert assembled["minutes"] == 12
    assert assembled["questions"][0]["fixed_passage"] == "An exam passage"
    assert Path(assembled["questions"][0]["image"]).read_bytes() == image.read_bytes()
    assert fixed_exam_packages.import_exam(target, package, "Other name") is None
    assert not target.results_path.exists()


def test_exam_bank_shares_atomic_reading_group_into_a_new_lesson(tmp_path):
    source = ExamBank(tmp_path / "A")
    target = ExamBank(tmp_path / "B")
    first = target.save_question(_question())
    source.save_question(_question())
    child = {"prompt": "First", "options": ["A", "B"], "answer": "A", "difficulty": 2}
    source.save_reading({"title": "Reading", "passage": "A short passage",
                         "subject": "tieng_anh", "grade": "1", "lesson": "Practice",
                         "questions": [child, {**child, "prompt": "Second"}]})
    path = tmp_path / "bank.tuhoc-pack"
    bank_packages.export_bank(path, source, "tieng_anh", "1", "Practice",
                              source.questions(), source.reading_groups())
    package = bank_packages.read_bank(path)
    new = bank_packages.import_bank(target, package)
    assert new["lesson"] == "Practice (2)"
    assert new["lesson"] in target.lessons("1", "tieng_anh")
    assert target.questions()[0]["id"] == first
    group = target.reading_groups()[0]
    assert group["lesson"] == new["lesson"]
    assert len({child["id"] for child in group["questions"]}) == 2
    assert bank_packages.import_bank(target, package) is None
    assert not target.config_path.exists()
    assert not target.results_path.exists()
