import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import wave
from zipfile import ZipFile

from PIL import Image

from tuhoc.lessons.level_flow import library_file
from tuhoc.lessons.unified_subjects import subject_image
from tuhoc.lessons.upgrade_v2 import Curriculum
from tuhoc.storage import question_packages as packs
from tuhoc.ui import theme_config


class QuestionPackageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / "sender" / "tieng_anh"
        self.destination = self.root / "recipient" / "tieng_anh"
        self.file = self.root / ("sample" + packs.EXTENSION)
        self.target = library_file(self.destination, "questions")
        self.target.parent.mkdir(parents=True)
        self.original = {
            "id": "same-id", "type": "fill", "prompt": "B's own question",
            "answer": "yes", "theme": "sports", "level": 1, "lesson": 1,
        }
        self.target.write_text(json.dumps([self.original]), encoding="utf-8")

    def export(self, *questions):
        packs.export_package(
            self.file, self.source, "en", ["sports", 1, 1], "Practice", "A",
            questions, lambda name: self.root / name if (self.root / name).is_file() else None,
        )
        return packs.read_package(self.file)

    def receive(self, package, **kwargs):
        return packs.import_package(package, self.destination, "en", "sports", 1, 1, **kwargs)

    def test_existing_content_and_edited_import_survive_revisions(self):
        original_upload = {**self.original, "prompt": "A's first version"}
        first = self.export(original_upload)
        self.assertEqual(self.receive(first), 1)
        current = json.loads(self.target.read_text(encoding="utf-8"))
        self.assertEqual(current[0], self.original)
        self.assertNotEqual(current[1]["id"], self.original["id"])
        self.assertEqual(current[1]["shared_source"]["title"], "Practice")
        self.assertEqual(current[1]["shared_source"]["author"], "A")
        current[1]["prompt"] = "B's edits"
        self.target.write_text(json.dumps(current), encoding="utf-8")
        self.assertEqual(self.receive(first), 0)

        updated = self.export({**original_upload, "prompt": "A's second version"})
        self.assertEqual(packs.package_status(updated, self.destination), "update")
        with self.assertRaises(ValueError):
            self.receive(updated)
        self.assertEqual(self.receive(updated, allow_update=True), 1)
        stored = Curriculum(self.destination).get("questions", "sports", 1)
        self.assertEqual([q["prompt"] for q in stored], [
            "B's own question", "B's edits", "A's second version",
        ])
        self.assertEqual(self.receive(updated, allow_update=True), 0)

    def test_media_layout_and_grading_references_round_trip(self):
        Image.new("RGB", (4, 4), "red").save(self.root / "left.png")
        Image.new("RGB", (4, 4), "blue").save(self.root / "right.png")
        with wave.open(str(self.root / "voice.wav"), "wb") as audio:
            audio.setparams((1, 2, 8000, 0, "NONE", ""))
            audio.writeframes(b"\x00\x00" * 80)
        layout = {"version": 2, "desktop": {"question_text": {"x": 30, "y": 100, "width": 700, "height": 70}}}
        listening = {
            **self.original, "id": "listen", "type": "listening_image_choice",
            "audio": "voice.wav", "answer": "right.png",
            "options": ["left.png", "right.png"],
            "image_options": [{"image": "left.png", "label": "left"}, "right.png"],
            "layout": layout, "_resolved_audio": "C:/private/location",
        }
        matching = {
            **self.original, "id": "match", "type": "matching",
            "options": ["img:left.png = left", "img:right.png = right"],
            "answer": "img:left.png = left | img:right.png = right",
        }
        package = self.export(listening, matching)
        self.assertEqual(len(package.assets), 3)
        self.assertEqual(self.receive(package), 2)
        _, received, pairs = json.loads(self.target.read_text(encoding="utf-8"))
        self.assertEqual(received["layout"], layout)
        self.assertNotIn("_resolved_audio", received)
        self.assertEqual(received["answer"], received["image_options"][1]["image"])
        self.assertEqual(received["answer"], received["options"][1])
        with Image.open(subject_image(self.destination, received["answer"])) as image:
            self.assertEqual(image.getpixel((0, 0)), (0, 0, 255))
        with wave.open(str(subject_image(self.destination, received["audio"])), "rb") as audio:
            self.assertEqual(audio.getnframes(), 80)
        self.assertEqual(pairs["answer"], " | ".join(pairs["options"]))

    def test_missing_attachment_and_invalid_members_are_rejected(self):
        with self.assertRaises(ValueError):
            self.export({**self.original, "image": "missing.png"})
        self.assertFalse(self.file.exists())
        self.export(self.original)
        with ZipFile(self.file, "a") as archive:
            archive.writestr("../outside.png", b"invalid")
        with self.assertRaises(ValueError):
            packs.read_package(self.file)
        self.assertEqual(json.loads(self.target.read_text(encoding="utf-8")), [self.original])

    def test_failed_commit_removes_new_media_and_can_retry(self):
        (self.root / "photo.png").write_bytes(b"photo")
        package = self.export({**self.original, "image": "photo.png"})
        with patch.object(packs, "commit_json", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                self.receive(package)
        self.assertEqual(list((self.target.parent / "media").iterdir()), [])
        self.assertEqual(packs.package_status(package, self.destination), "new")
        self.assertEqual(self.receive(package), 1)

    def test_wrong_subject_leaves_recipient_data_unchanged(self):
        package = self.export(self.original)
        with self.assertRaises(ValueError):
            packs.import_package(package, self.destination, "vi", "sports", 1, 1)
        self.assertEqual(json.loads(self.target.read_text(encoding="utf-8")), [self.original])

    def test_topic_package_creates_an_independent_topic_with_original_positions(self):
        topic = {"code": "sports", "title": "Sports", "max_level": 3,
                 "default_lessons": 1, "lesson_counts": {"2": 4}}
        questions = [
            self.original,
            {**self.original, "id": "later", "level": 2, "lesson": 4},
        ]

        def export():
            packs.export_package(self.file, self.source, "en", ["topic", "sports"],
                                 "Practice", "A", questions, lambda _: None, topic=topic)
            return packs.read_package(self.file)

        first = export()
        with self.assertRaises(ValueError):
            self.receive(first)
        count, code = packs.import_topic_package(first, self.destination, "en", topic_title=" Sports ")
        self.assertEqual(count, 2)
        self.assertNotEqual(code, "sports")
        self.assertEqual(next(t["title"] for t in theme_config.load(self.destination) if t["code"] == code),
                         "Sports (2)")
        self.assertEqual(theme_config.max_level(self.destination, code), 3)
        self.assertEqual(theme_config.lesson_count(self.destination, code, 2), 4)
        curriculum = Curriculum(self.destination)
        self.assertEqual(curriculum.get("questions", "sports", 1)[0]["id"], self.original["id"])
        self.assertEqual(curriculum.get("questions", code, 2)[0]["lesson"], 4)
        self.assertEqual(curriculum.get("questions", code, 3), [])
        self.assertEqual(packs.import_topic_package(first, self.destination, "en"), (0, None))

        topic["max_level"] = 4
        update = export()
        self.assertEqual(packs.package_status(update, self.destination), "update")
        with self.assertRaises(ValueError):
            packs.import_topic_package(update, self.destination, "en")
        _, updated_code = packs.import_topic_package(update, self.destination, "en", allow_update=True)
        self.assertNotEqual(updated_code, code)
        self.assertEqual(theme_config.max_level(self.destination, code), 3)
        self.assertEqual(theme_config.max_level(self.destination, updated_code), 4)
        self.assertEqual(next(t["title"] for t in theme_config.load(self.destination) if t["code"] == updated_code),
                         "Sports · từ A")

    def test_topic_export_rejects_positions_outside_the_catalog(self):
        topic = {"code": "sports", "title": "Sports", "max_level": 1, "default_lessons": 1}
        with self.assertRaisesRegex(ValueError, "ngoài cấu trúc"):
            packs.export_package(self.file, self.source, "en", ["topic", "sports"],
                                 "Practice", "A", [{**self.original, "lesson": 2}],
                                 lambda _: None, topic=topic)
        self.assertFalse(self.file.exists())
