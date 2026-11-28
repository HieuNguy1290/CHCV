"""Regression coverage for the local image importer without a model server."""

import json
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from sqlite3 import connect
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image

from tools.fixtures.build_image_quiz_drafts import build, publish
from tools.local_agent.__main__ import read_answers, run, source_rows
from tools.local_agent.image_quiz import ANSWER, REVIEW, VISION, validate
from tools.local_agent.ollama_client import Ollama


class FakeOllama:
    offline = False
    interrupt_at = None
    broken_review = False
    requests = []
    vision = {
        "type": "image_sentence_fill", "prompt": "Look and choose:", "blank_text": "The .... is shining.",
        "options": ["sun", "sail"], "crop": [100, 100, 500, 600], "choices": [], "uncertainty": "",
    }

    def __init__(self, timeout, context):
        self.options = {"num_ctx": context}
        self.calls = 0

    def health(self):
        if self.offline:
            raise OSError("Ollama offline")
        return {"model": "qwen3-vl:4b-instruct", "digest": "test-digest"}

    def chat(self, image, prompt, schema, validate):
        self.calls += 1
        self.requests.append(schema)
        assert image.startswith(b"\x89PNG")
        if self.calls == self.interrupt_at:
            raise KeyboardInterrupt
        if schema is REVIEW and self.broken_review:
            raise ValueError("JSON invalid")
        result = {
            id(VISION): self.vision,
            id(ANSWER): {"answer_index": 0, "evidence": "The illustrated sun is shining."},
            id(REVIEW): {"differences": [], "evidence": "Text and options match."},
        }[id(schema)]
        validate(result)
        return result


class LocalAgentTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / "Ảnh bài tập"
        self.source.mkdir()
        self.state = self.root / "state"
        self.patch = patch("tools.local_agent.__main__.Ollama", FakeOllama)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        FakeOllama.requests.clear()

    def image(self, name, color="white", folder=None):
        Image.new("RGB", (100, 200), color).save((folder or self.source) / name)

    def command(self, command, **arguments):
        return run(SimpleNamespace(command=command, timeout=10, context=4096, state_dir=self.state,
                                   **arguments))

    def process(self, answers=None):
        return self.command("process", source=self.source, answers=answers)

    def read(self, filename):
        return json.loads(Path(filename).read_text(encoding="utf-8"))

    def test_answer_change_reuses_vision_and_preserves_prior_exports(self):
        self.image("câu 3.png")
        self.image("1.png")
        nested = self.source / "nested"
        nested.mkdir()
        self.image("câu 80.png", folder=nested)
        answers = self.root / "answers.json"
        answers.write_text('{"3":"sun"}')
        vision = {**FakeOllama.vision, "blank_text": "The ... is shining.",
                  "choices": [{"label": "sun", "crop": FakeOllama.vision["crop"]},
                              {"label": "sail", "crop": [600, 650, 750, 750]}]}
        with patch.object(FakeOllama, "vision", vision):
            original = self.process(answers)
        self.assertEqual(original["total"], 1)
        self.assertEqual(original["passed"], 1)
        self.assertEqual(original["approved"], 0)
        self.assertEqual(FakeOllama.requests, [VISION, REVIEW])
        answers.write_text('{"3":1}')
        changed = self.process(answers)
        self.assertEqual(changed["cache_hits"], 1)
        self.assertEqual(changed["ollama_calls"], 1)
        self.assertEqual(self.read(changed["draft"])[0]["answer_index"], 1)
        self.assertEqual(self.read(original["draft"])[0]["answer_index"], 0)
        self.assertEqual(self.read(changed["draft"])[0]["crop"], [10, 20, 50, 120])
        self.assertEqual(self.read(changed["draft"])[0]["blank_text"], "The .... is shining.")
        self.assertNotEqual(original["batch_id"], changed["batch_id"])

    def test_interrupted_batch_resumes_and_reuses_finished_checkpoint(self):
        self.image("câu 2.png")
        self.image("câu 7.png", "yellow")
        with patch.object(FakeOllama, "interrupt_at", 4), self.assertRaises(KeyboardInterrupt):
            self.process()
        with closing(connect(self.state / "state.sqlite3")) as db:
            batch = db.execute("SELECT id FROM batch").fetchone()[0]
        self.assertEqual(self.command("report", batch=batch)["pending"], 1)
        result = self.command("resume", batch=batch)
        self.assertEqual(result["checkpoint_hits"], 1)
        self.assertEqual(result["passed"], 2)
        self.assertEqual(result["ollama_calls"], 3)
        with patch.object(FakeOllama, "offline", True):
            self.assertEqual(self.command("resume", batch=batch)["ollama_calls"], 0)

    def test_missing_media_malformed_review_and_unsupported_stay_out_of_package(self):
        self.image("câu 2.png")
        listening = {**FakeOllama.vision, "type": "listening_image_choice", "blank_text": "",
                     "options": [], "crop": [],
                     "choices": [{"label": "sun", "crop": [0, 0, 200, 200]},
                                 {"label": "box", "crop": [500, 0, 700, 200]}]}
        with patch.object(FakeOllama, "vision", listening):
            result = self.process()
        exception = self.read(result["exceptions"])[0]
        self.assertEqual(exception["status"], "needs_review")
        self.assertIn("MP3", exception["notes"])
        self.assertIsNone(self.read(result["draft"])[0]["answer_index"])
        with patch.object(FakeOllama, "broken_review", True):
            failed = self.command("resume", batch=result["batch_id"], refresh=True)
        self.assertEqual(failed["failed"], 1)
        self.assertIsNone(self.read(failed["draft"])[0]["answer_index"])
        with patch.object(FakeOllama, "vision", {**listening, "type": "matching"}):
            unsupported = self.command("resume", batch=result["batch_id"], refresh=True)
        self.assertEqual(unsupported["unsupported"], 1)

    def test_build_publish_backup_curriculum_and_subject_media_in_temp_subject(self):
        self.image("câu 2.png")
        result = self.process()
        package = self.root / "package"
        build(self.source, package, self.read(result["draft"]), "demo", 2, 3)
        subject = self.root / "tieng_anh"
        library = subject / "content_library"
        library.mkdir(parents=True)
        (library / "themes.json").write_text('[{"code":"demo","title":"Demo","max_level":2}]')
        (library / "level_questions.json").write_text("[]")
        published = publish(package, subject, [2])
        self.assertTrue(Path(published["backup"]).exists())
        self.assertEqual(self.command("verify", subject=subject, package=package, approve=[2]),
                         {"verified": ["demo-L2-B3-Q2"]})
        self.assertEqual(publish(package, subject, [2])["already_present"], ["demo-L2-B3-Q2"])

    def test_listening_uses_supplied_label_and_requires_matching_mp3(self):
        self.image("câu 2.png")
        # MPEG-1 Layer III headers, 128 kbps, 44.1 kHz. Payload is for metadata checks only.
        (self.source / "câu 2.mp3").write_bytes((bytes.fromhex("fffb9064") + bytes(413)) * 6)
        answers = self.root / "answers.json"
        answers.write_text('{"2":"box"}')
        listening = {**FakeOllama.vision, "type": "listening_image_choice", "blank_text": "",
                     "options": [], "crop": [],
                     "choices": [{"label": "sun", "crop": [0, 0, 200, 200]},
                                 {"label": "box", "crop": [500, 0, 700, 200]}]}
        with patch.object(FakeOllama, "vision", listening):
            original = self.process(answers)
            without_answer = self.process()
        self.assertEqual(original["passed"], 1)
        self.assertEqual(self.read(original["draft"])[0]["answer_index"], 1)
        self.assertEqual(without_answer["needs_review"], 1)
        self.assertNotIn(ANSWER, FakeOllama.requests)
        package = self.root / "package"
        build(self.source, package, self.read(original["draft"]), "demo", 2, 3)
        question = self.read(package / "level_questions.json")[0]
        self.assertEqual(question["answer"], question["image_options"][1]["image"])
        self.assertTrue((package / "media" / question["audio"]).is_file())
        (self.source / "câu 2.mp3").write_bytes(b"invalid")
        with self.assertRaisesRegex(ValueError, "MP3"):
            self.command("resume", batch=original["batch_id"])

    def test_answer_file_rejects_unscanned_numbers_and_duplicates(self):
        self.image("câu 2.png")
        rows = source_rows(self.source)
        answers = self.root / "answers.json"
        for malformed in ('{"1":0}', '{"2":0,"2":1}', '{"2":true}'):
            answers.write_text(malformed)
            with self.assertRaises(ValueError):
                read_answers(answers, rows)

    def test_missing_and_null_supplied_answers_are_held_without_solving(self):
        for number in (2, 3, 4):
            self.image(f"câu {number}.png")
        answers = self.root / "answers.json"
        answers.write_text('{"2":0,"3":null}')
        result = self.process(answers)
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["needs_review"], 2)
        self.assertEqual([row["answer_index"] for row in self.read(result["draft"])], [0, None, None])
        self.assertNotIn(ANSWER, FakeOllama.requests)

    def test_lesson_result_image_is_excluded_and_disables_solving(self):
        self.image("câu 2.png")
        self.image("result.png")
        result = self.process()
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["needs_review"], 1)
        self.assertIsNone(self.read(result["draft"])[0]["answer_index"])
        self.assertNotIn(ANSWER, FakeOllama.requests)

    def test_misclassified_listening_fill_never_solves_from_the_screenshot(self):
        self.image("câu 22.png")
        vision = {**FakeOllama.vision, "prompt": "Listen and make sentence:", "blank_text": "......"}
        with patch.object(FakeOllama, "vision", vision):
            result = self.process()
        self.assertEqual(result["needs_review"], 1)
        self.assertIn("bỏ phần nghe", self.read(result["exceptions"])[0]["notes"])
        self.assertIsNone(self.read(result["draft"])[0]["answer_index"])
        self.assertEqual(FakeOllama.requests, [VISION, REVIEW])


class OllamaTest(unittest.TestCase):
    def test_structured_chat_retries_truncated_output_then_validates(self):
        client = Ollama()
        response = {"done": True, "done_reason": "stop",
                    "message": {"content": '{"answer_index":0,"evidence":"visible"}'}}
        with patch.object(client, "request", side_effect=[{**response, "done_reason": "length"}, response]) as api:
            result = client.chat(b"source image", "prompt", ANSWER, lambda output: validate(output, ANSWER))
        self.assertEqual(result["answer_index"], 0)
        self.assertEqual(client.calls, 2)
        endpoint, payload = api.call_args.args
        self.assertEqual(endpoint, "/api/chat")
        self.assertEqual(payload["model"], "qwen3-vl:4b-instruct")
        self.assertEqual(payload["messages"][1]["images"], ["c291cmNlIGltYWdl"])
        self.assertEqual(payload["format"], ANSWER)
        self.assertFalse(payload["stream"])


if __name__ == "__main__":
    unittest.main()
