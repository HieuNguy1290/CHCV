"""Run the TuHoc image import worker from the project root."""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from collections import Counter
from contextlib import closing
from pathlib import Path
from time import monotonic
from uuid import uuid4

from mutagen.mp3 import MP3
from mutagen import MutagenError

from tools.fixtures.build_image_quiz_drafts import scan
from tools.local_agent.cache import Store, encode, key
from tools.local_agent.image_quiz import (
    ANSWER, CHECK, PROMPT_CONTRACT_VERSION, RECOGNIZE, REVIEW, RULE_VERSION, SOLVE,
    VISION, evaluate, validate,
)
from tools.local_agent.ollama_client import Ollama, unique_object


def file_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def source_rows(source):
    rows = scan(source)
    if not rows:
        raise ValueError("Không tìm thấy ảnh theo mẫu câu N.png.")
    for row in rows:
        row.update(media_sha256=None, media_valid=False, media_issue="Thiếu MP3 cùng tên.")
        if row["audio"]:
            audio = source / row["audio"]
            row["media_sha256"] = file_digest(audio)
            try:
                if MP3(audio).info.length <= 0:
                    raise ValueError("MP3 rỗng.")
            except (MutagenError, ValueError):
                row["media_issue"] = "MP3 cùng tên không đọc được."
            else:
                row.update(media_valid=True, media_issue="")
    return rows


def read_answers(path, rows):
    if path is None:
        return None
    answers = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    numbers = {str(row["number"]) for row in rows}
    if not isinstance(answers, dict) or not answers.keys() <= numbers:
        raise ValueError("File đáp án phải là object với khóa là số câu đã quét.")
    if any(value is not None and type(value) not in (int, str) for value in answers.values()):
        raise ValueError("Đáp án phải là chỉ số từ 0, nhãn nguyên văn hoặc null.")
    return answers


def write_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(encode(value) + "\n", encoding="utf-8")
    temporary.replace(path)


def summary(batch, manifest, results):
    counts = Counter(item["status"] for item in results.values())
    return {
        "batch_id": batch, "total": len(manifest["rows"]),
        "passed": counts["passed"], "approved": 0,
        "needs_review": counts["needs_review"], "unsupported": counts["unsupported"],
        "failed": counts["failed"], "pending": len(manifest["rows"]) - len(results),
    }


def export(store, batch, manifest, results, stats):
    folder = store.root / batch / uuid4().hex
    folder.mkdir(parents=True)
    draft_file = folder / "drafts.json"
    exception_file = folder / "exceptions.json"
    drafts, exceptions = [], []
    for number, item in sorted(results.items()):
        draft = {**item["draft"], "number": number, "review": item["notes"]}
        if item["status"] != "passed":
            draft["answer_index"] = None
            exceptions.append(item)
        drafts.append(draft)
    write_json(draft_file, drafts)
    write_json(exception_file, exceptions)
    result = {
        **summary(batch, manifest, results), **stats,
        "draft": str(draft_file), "exceptions": str(exception_file),
    }
    store.finish(batch, result)
    return result


def process(store, batch, manifest, client, available, refresh=False):
    if refresh and not available:
        raise ValueError("Cần đúng model Ollama của batch để chạy lại ngoại lệ.")
    store.start(batch, manifest)
    print(f"Batch {batch}", file=sys.stderr, flush=True)
    start = monotonic()
    hits = 0
    reused = 0
    previous = store.questions(batch)
    source = Path(manifest["source"])
    answers = manifest["answers"]
    for row in manifest["rows"]:
        number = row["number"]
        if previous.get(number, {}).get("status") == "passed":
            reused += 1
            continue
        stages = {}
        draft = {}
        supplied = (answers or {}).get(str(number))
        try:
            image = (source / row["image"]).read_bytes()
            if hashlib.sha256(image).hexdigest() != row["sha256"]:
                raise ValueError("Ảnh nguồn vừa thay đổi. Chạy process lại.")

            def stage(name, schema, prompt, inputs):
                nonlocal hits
                cache_key = key([
                    row["sha256"], manifest["model"], manifest["options"],
                    manifest["stage_rules"], schema, prompt, inputs,
                ])
                value = None if refresh else store.cached(name, cache_key)
                if value is None:
                    if not available:
                        raise ValueError("Ollama local hoặc đúng model của batch chưa sẵn sàng.")
                    value = client.chat(image, prompt + "\nData: " + encode(inputs),
                                        schema, lambda output: validate(output, schema))
                    store.remember(name, cache_key, value)
                else:
                    hits += 1
                stages[name] = value
                return value

            status, draft, notes = evaluate(
                row, image, supplied, stage, require_supplied=answers is not None,
            )
        except (OSError, ValueError) as exc:
            status, notes = "failed", str(exc)
            draft = {**stages.get("vision", {}), **stages.get("answer", {})}
        store.checkpoint(batch, number, {
            "number": number, "status": status, "draft": draft,
            "image": str(source / row["image"]), "audio": str(source / row["audio"]) if row["audio"] else None,
            "supplied_answer": supplied, "notes": notes, "stages": stages,
        })
    return export(store, batch, manifest, store.questions(batch), {
        "cache_hits": hits, "checkpoint_hits": reused, "ollama_calls": client.calls,
        "seconds": round(monotonic() - start, 2),
    })


def model_identity(store, client):
    try:
        model = client.health()
    except (OSError, ValueError, KeyError, TypeError):
        return store.cached("metadata", "last_local_model"), False
    store.remember("metadata", "last_local_model", model)
    return model, True


def verify(subject, package, approved):
    from tuhoc.lessons.unified_subjects import subject_image
    from tuhoc.lessons.upgrade_v2 import Curriculum

    questions = json.loads((package / "level_questions.json").read_text(encoding="utf-8"))
    reviews = json.loads((package / "review.json").read_text(encoding="utf-8"))
    ids = {row["number"]: row["id"] for row in reviews if row["status"] == "needs_review"}
    if not set(approved) <= ids.keys():
        raise ValueError("Danh sách xác minh có câu nằm ngoài tập nhập.")
    expected = {ids[number] for number in approved}
    curriculum = Curriculum(subject)
    verified = []
    for row in questions:
        if row["id"] not in expected:
            continue
        loaded = next((question for question in curriculum.get("questions", row["theme"], row["level"])
                       if question["id"] == row["id"] and question.get("lesson") == row["lesson"]), None)
        if loaded is None:
            raise ValueError(f"Curriculum thiếu câu hoặc sai Lesson {row['id']}.")
        published = dict(row)
        names = [row[field] for field in ("image", "audio") if row.get(field)]
        for field in ("image", "audio"):
            if row.get(field):
                published[field] = f"media/{row[field]}"
        if row.get("image_options"):
            names.extend(option["image"] for option in row["image_options"])
            published["image_options"] = [{**option, "image": f"media/{option['image']}"}
                                          for option in row["image_options"]]
            published["answer"] = f"media/{row['answer']}"
        if loaded != published:
            raise ValueError(f"Nội dung Curriculum không khớp gói: {row['id']}")
        for name in names:
            ref = f"media/{name}"
            media = subject_image(subject, ref)
            if media is None or file_digest(media) != file_digest(package / "media" / name):
                raise ValueError(f"Media sau nhập không khớp gói: {ref}")
        verified.append(row["id"])
    if expected != set(verified):
        raise ValueError("Thiếu câu trong gói dùng để xác minh.")
    return {"verified": verified}


def run(args):
    if args.command == "verify":
        return verify(args.subject, args.package, args.approve)
    client = Ollama(args.timeout, args.context)
    if args.command == "health":
        return client.health()
    store = Store(args.state_dir.resolve())
    with closing(store.db):
        if args.command == "report":
            manifest, complete = store.batch(args.batch)
            return complete or summary(args.batch, manifest, store.questions(args.batch))
        with store.worker():
            model, available = model_identity(store, client)
            stage_rules = key([PROMPT_CONTRACT_VERSION, VISION, ANSWER, REVIEW, RECOGNIZE, SOLVE, CHECK])
            rules = key([RULE_VERSION, stage_rules])
            if args.command == "process":
                source = args.source.resolve()
                rows = source_rows(source)
                manifest = {"source": str(source), "rows": rows, "options": client.options,
                            "model": model, "rules": rules, "stage_rules": stage_rules,
                            "answers": read_answers(args.answers, rows)}
                if manifest["answers"] is None and (source / "result.png").is_file():
                    manifest["answers"] = {}
                batch = key(manifest)
            else:
                batch = args.batch
                manifest, _ = store.batch(batch)
                if manifest["rules"] != rules:
                    raise ValueError("Quy tắc batch đã đổi. Chạy process lại.")
                if source_rows(Path(manifest["source"])) != manifest["rows"]:
                    raise ValueError("Ảnh hoặc MP3 nguồn đã đổi. Chạy process lại.")
                if manifest["answers"] is None and (Path(manifest["source"]) / "result.png").is_file():
                    raise ValueError("Thư mục Lesson vừa có result.png. Chạy process với đáp án từ ảnh.")
                if available and manifest["model"] not in (None, model):
                    raise ValueError("Digest model đã đổi. Chạy process lại.")
                if available and manifest["model"] is None:
                    manifest["model"] = model
                client.options = manifest["options"]
            return process(store, batch, manifest, client, available, getattr(args, "refresh", False))


def main():
    root = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".cache") / "TuHoc" / "local-agent"
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--state-dir", type=Path, default=root)
    cli.add_argument("--timeout", type=int, default=300)
    cli.add_argument("--context", type=int, choices=(4096, 8192), default=4096)
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser("health")
    batch = commands.add_parser("process")
    batch.add_argument("--source", required=True, type=Path)
    batch.add_argument("--answers", type=Path)
    for name in ("resume", "report"):
        command = commands.add_parser(name)
        command.add_argument("--batch", required=True)
        if name == "resume":
            command.add_argument("--refresh", action="store_true", help="Chạy lại model cho các câu ngoại lệ")
    check = commands.add_parser("verify")
    check.add_argument("--subject", required=True, type=Path)
    check.add_argument("--package", required=True, type=Path)
    check.add_argument("--approve", required=True, nargs="+", type=int)
    args = cli.parse_args()
    if args.timeout <= 0:
        cli.error("--timeout phải lớn hơn 0")
    try:
        print(json.dumps(run(args), ensure_ascii=True))
    except (OSError, ValueError, sqlite3.Error) as exc:
        cli.exit(1, f"{exc}\n")
    except KeyboardInterrupt:
        cli.exit(130, "Batch tạm dừng. Dùng resume với Batch ID đã in.\n")


if __name__ == "__main__":
    main()
