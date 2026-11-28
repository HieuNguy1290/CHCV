"""Portable, append-only exchange for Lesson/Level questions."""
from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import tempfile
from uuid import uuid4
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

from tuhoc.exercises.matching_widget import IMAGE_PREFIX, parse_pairs
from tuhoc.storage.safe_storage import commit_json
from tuhoc.studio.question_layout_store import validate_layout


EXTENSION = ".tuhoc-pack"
FORMAT = "tuhoc-questions-v1"
TOPIC_FORMAT = "tuhoc-topic-questions-v1"
LESSON_FORMAT = "tuhoc-topic-lessons-v1"
LESSON_KINDS = ("lessons", "blocks", "reading", "vocab")
MAX_MANIFEST = 8 * 1024**2
MAX_ASSET = 32 * 1024**2
MAX_TOTAL = 128 * 1024**2
MAX_ITEMS = 5000
SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp",
            ".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".opus"}
ASSET_NAME = re.compile(r"media/[0-9a-f]{64}\.[a-z0-9]+")
UUID = re.compile(r"[0-9a-f]{32}")


def _json(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, allow_nan=False).encode("utf-8")


def _digest(data):
    return sha256(data).hexdigest()


def _public(value):
    if isinstance(value, dict):
        return {key: _public(item) for key, item in value.items()
                if not key.startswith("_") and key != "shared_source"}
    if isinstance(value, list):
        return [_public(item) for item in value]
    return value


def _media(question, replace):
    """Rewrite the actual persisted media fields, including legacy option forms."""
    result = _public(question)
    for key in ("image", "audio"):
        if result.get(key):
            result[key] = replace(result[key])
    kind = result.get("type")
    if kind in ("image_multi_choice", "listening_image_choice"):
        if result.get("image_options"):
            result["image_options"] = [
                {**option, "image": replace(option["image"])}
                if isinstance(option, dict) else {"image": replace(option)}
                for option in result["image_options"]
            ]
        if result.get("options"):
            result["options"] = [replace(value) for value in result.get("options") or []]
        if isinstance(result.get("answer"), str) and result.get("answer"):
            result["answer"] = replace(result["answer"])
    if kind == "matching":
        options = result.get("options") or []
        pairs = parse_pairs(options)
        if len(pairs) != len(options):
            raise ValueError("Câu nối cặp có lựa chọn không hợp lệ.")

        def replace_token(token):
            if token.startswith(IMAGE_PREFIX):
                return IMAGE_PREFIX + replace(token[len(IMAGE_PREFIX):])
            return token

        result["options"] = [
            f"{replace_token(left)} = {replace_token(right)}" for left, right in pairs
        ]
        if result.get("answer") == " | ".join(options):
            result["answer"] = " | ".join(result["options"])
    return result


def _check_question(question):
    from tuhoc.lessons.level_flow import QUESTION_TYPES

    if not isinstance(question, dict):
        raise ValueError("Câu hỏi trong gói phải là đối tượng JSON.")
    kind = question.get("type")
    if kind not in QUESTION_TYPES:
        raise ValueError(f"Dạng bài không hỗ trợ: {kind}")
    if not isinstance(question.get("id"), str) or not question["id"].strip():
        raise ValueError("Câu hỏi thiếu mã.")
    if kind != "picture_missing_letters" and (
        not isinstance(question.get("prompt"), str) or not question["prompt"].strip()
    ):
        raise ValueError(f"Câu {question['id']} thiếu nội dung.")
    if not (question.get("answer") or question.get("blank_answers")):
        raise ValueError(f"Câu {question['id']} thiếu đáp án.")
    for key in ("options", "image_options"):
        if question.get(key) is not None and not isinstance(question[key], list):
            raise ValueError(f"Câu {question['id']} có danh sách lựa chọn không hợp lệ.")
    if kind in ("choice", "picture_choice", "listening_choice"):
        options = question.get("options") or []
        if len(options) < 2 or any(not isinstance(option, str) or not option.strip() for option in options):
            raise ValueError(f"Câu {question['id']} cần ít nhất hai lựa chọn.")
    if kind == "matching" and len(parse_pairs(question.get("options"))) < 2:
        raise ValueError(f"Câu {question['id']} cần ít nhất hai cặp nối.")
    if kind in ("listening_choice", "listening_fill", "listening_image_choice", "audio_multi_select") and not question.get("audio"):
        raise ValueError(f"Câu {question['id']} thiếu âm thanh.")
    if kind in ("picture_choice", "picture_missing_letters", "image_multi_select", "image_write_answer", "image_underline_choice") and not question.get("image"):
        raise ValueError(f"Câu {question['id']} thiếu ảnh.")
    if kind in ("image_multi_choice", "listening_image_choice"):
        options = question.get("image_options") or []
        if options and any(not (item.get("image") if isinstance(item, dict)
                               else isinstance(item, str) and item.strip()) for item in options):
            raise ValueError(f"Câu {question['id']} có lựa chọn ảnh không hợp lệ.")
        count = len(options or (question.get("options", []) if kind == "image_multi_choice" else []))
        if count < 2:
            raise ValueError(f"Câu {question['id']} cần ít nhất hai lựa chọn ảnh.")
    if kind == "listening_image_choice":
        from tuhoc.exercises.listening_image_extension import validate
        validate(question)
    if kind in ("image_multi_select", "text_multi_select", "audio_multi_select"):
        from tuhoc.exercises.multi_select_extension import validate
        validate(question)
    if question.get("layout") is not None:
        validate_layout(question["layout"])


@contextmanager
def _locked(library):
    library.mkdir(parents=True, exist_ok=True)
    with (library / ".question-packages.lock").open("a+b") as lock:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def _family(library, scope):
    path = library / "question_package_sender.json"
    with _locked(library):
        if path.exists():
            sender = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(sender, str) or not UUID.fullmatch(sender):
                raise ValueError("Không đọc được mã người gửi trên máy này.")
        else:
            sender = uuid4().hex
            commit_json({path: sender})
    return _digest(_json([sender, scope]))


def _topic_metadata(topic):
    from tuhoc.ui.theme_config import validate

    if not isinstance(topic, dict):
        raise ValueError("Thông tin chủ đề không hợp lệ.")
    code, title = topic.get("code"), topic.get("title")
    count = topic.get("max_level", 10)
    default = topic.get("default_lessons", 10)
    overrides = topic.get("lesson_counts", {})
    if (not isinstance(code, str) or not code.strip() or len(code) > 200
            or not isinstance(title, str) or not title.strip() or len(title) > 120
            or type(count) is not int or not 1 <= count <= 200
            or type(default) is not int or not 1 <= default <= 200
            or not isinstance(overrides, dict)):
        raise ValueError("Tên, mã hoặc số Level/Lesson của chủ đề không hợp lệ.")
    result = {"code": code, "title": title, "max_level": count,
              "default_lessons": default, "lesson_counts": overrides}
    icon, color = topic.get("icon"), topic.get("color")
    if isinstance(icon, str) and len(icon) <= 12:
        result["icon"] = icon
    if isinstance(color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        result["color"] = color
    validate([result])
    return result


def _topic_position(row, topic):
    try:
        level = int(str(row["level"]))
        lesson = int(str(row.get("lesson") or 1))
    except (KeyError, ValueError) as exc:
        raise ValueError(f"Mục {row.get('id') or row.get('title', '')} có Level hoặc Lesson không hợp lệ.") from exc
    allowed = int(topic["lesson_counts"].get(str(level), topic["default_lessons"]))
    if row.get("theme") != topic["code"] or not 1 <= level <= topic["max_level"] or not 1 <= lesson <= allowed:
        raise ValueError(f"Mục {row.get('id') or row.get('title', '')} nằm ngoài cấu trúc chủ đề.")
    return level, lesson


def collect_assets(resolve_media):
    assets, seen_paths = {}, {}
    total_size = 0

    def collect(value):
        nonlocal total_size
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tham chiếu tệp đính kèm không hợp lệ.")
        if value not in seen_paths:
            source = resolve_media(value)
            if not source:
                raise ValueError(f"Không tìm thấy tệp đính kèm: {value}")
            source = Path(source)
            suffix = source.suffix.lower()
            if suffix not in SUFFIXES:
                raise ValueError(f"Định dạng tệp đính kèm không hỗ trợ: {suffix}")
            with source.open("rb") as file:
                payload = file.read(MAX_ASSET + 1)
            if not 0 < len(payload) <= MAX_ASSET:
                raise ValueError(f"Tệp rỗng hoặc quá lớn: {source.name}")
            name = f"media/{_digest(payload)}{suffix}"
            if name not in assets:
                total_size += len(payload)
                if total_size > MAX_TOTAL or len(assets) >= MAX_ITEMS:
                    raise ValueError("Gói có quá nhiều tệp hoặc vượt giới hạn dung lượng.")
                assets[name] = payload
            seen_paths[value] = name
        return seen_paths[value]

    return assets, collect


def rewrite_media_fields(record, replace, fields):
    result = _public(record)
    for key in fields:
        if result.get(key):
            result[key] = replace(result[key])
    return result


def _lesson_content(content, topic, language, replace):
    from tuhoc.lessons.image_children import validate_block

    if not isinstance(content, dict) or set(content) - set(LESSON_KINDS):
        raise ValueError("Nội dung bài học không hợp lệ.")
    result = {}
    count = 0
    for kind in LESSON_KINDS:
        rows = content.get(kind, [])
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError("Danh sách nội dung bài học không hợp lệ.")
        count += len(rows)
        if count > MAX_ITEMS:
            raise ValueError("Gói có quá nhiều mục bài học.")
        result[kind] = []
        for row in rows:
            level, lesson = _topic_position(row, topic)
            cleaned = rewrite_media_fields(
                row, replace, ("image", "audio", "title_audio", "content_audio", "sound", "audio_file"),
            )
            cleaned.update(level=level, lesson=lesson)
            if kind == "vocab" and (not cleaned.get("word") or (language == "en" and not cleaned.get("meaning"))):
                raise ValueError("Mục từ vựng thiếu từ hoặc nghĩa.")
            if kind == "blocks":
                cleaned["order"] = int(str(cleaned.get("order") or 1))
                if cleaned["order"] < 1:
                    raise ValueError("Thứ tự khối bài học không hợp lệ.")
                problems = validate_block(cleaned)
                if problems:
                    raise ValueError(problems[0])
            result[kind].append(cleaned)
    return result


def export_package(path, data_dir, language, scope, title, author, questions, resolve_media, *,
                   topic=None, lesson_content=None):
    if len(questions) > MAX_ITEMS or (not questions and lesson_content is None):
        raise ValueError(f"Gói phải có từ 1 đến {MAX_ITEMS} câu hỏi.")
    title, author = title.strip(), author.strip()
    if not title or len(title) > 120 or len(author) > 100 or language not in ("en", "vi"):
        raise ValueError("Tên gói, tác giả hoặc môn học không hợp lệ.")
    assets, collect = collect_assets(resolve_media)

    topic = _topic_metadata(topic) if topic is not None else None
    rows = []
    for question in questions:
        _check_question(question)
        packed = _media(question, collect)
        _check_question(packed)
        if topic is not None:
            packed["level"], packed["lesson"] = _topic_position(packed, topic)
        rows.append(packed)
    rows.sort(key=lambda row: row["id"])
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Gói có mã câu hỏi trùng nhau.")
    document = {
        "format": TOPIC_FORMAT if topic is not None else FORMAT,
        "language": language, "title": title, "author": author,
        "family": _family(Path(data_dir) / "content_library", scope), "questions": rows,
    }
    if topic is not None:
        document["topic"] = topic
    if lesson_content is not None:
        if topic is None:
            raise ValueError("Gói bài học cần một chủ đề.")
        content = _lesson_content(lesson_content, topic, language, collect)
        if not any(content.values()):
            raise ValueError("Chủ đề chưa có nội dung bài học để xuất.")
        document.update(format=LESSON_FORMAT, lesson_content=content)
    write_archive(path, document, assets)


def write_archive(path, document, assets):
    manifest = _json(document)
    if len(manifest) > MAX_MANIFEST:
        raise ValueError("Nội dung câu hỏi vượt giới hạn dung lượng.")
    path = Path(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        staged = Path(stream.name)
    try:
        with ZipFile(staged, "w", ZIP_DEFLATED) as archive:
            archive.writestr("manifest.json", manifest)
            for name, payload in assets.items():
                archive.writestr(name, payload)
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


@dataclass
class QuestionPackage:
    title: str
    author: str
    language: str
    family: str
    revision: str
    questions: list
    assets: dict
    topic: dict | None = None
    lesson_content: dict | None = None


def read_archive(path):
    try:
        if Path(path).stat().st_size > MAX_TOTAL + MAX_MANIFEST + 4 * 1024**2:
            raise ValueError("Gói vượt giới hạn dung lượng.")
        with ZipFile(path) as archive:
            members = archive.infolist()
            names = {item.filename for item in members}
            if len(names) != len(members) or "manifest.json" not in names or len(names) > MAX_ITEMS + 1:
                raise ValueError("Danh mục tệp trong gói không hợp lệ.")
            assets = {}
            total = 0
            for item in members:
                name = item.filename
                limit = MAX_MANIFEST if name == "manifest.json" else MAX_ASSET
                total += item.file_size
                if not 0 < item.file_size <= limit or total > MAX_TOTAL + MAX_MANIFEST:
                    raise ValueError("Gói vượt giới hạn dung lượng hoặc có tệp rỗng.")
                if name != "manifest.json":
                    if not ASSET_NAME.fullmatch(name) or Path(name).suffix not in SUFFIXES:
                        raise ValueError("Gói chứa đường dẫn tệp đính kèm không hợp lệ.")
                    payload = archive.read(item)
                    if _digest(payload) != Path(name).stem:
                        raise ValueError("Tệp đính kèm bị hỏng hoặc đã thay đổi.")
                    assets[name] = payload
            manifest = json.loads(archive.read("manifest.json"))
        return manifest, assets
    except (BadZipFile, RuntimeError, NotImplementedError) as exc:
        raise ValueError("Không đọc được gói.") from exc


def read_package(path):
    try:
        manifest, assets = read_archive(path)
        if not isinstance(manifest, dict) or manifest.get("format") not in (FORMAT, TOPIC_FORMAT, LESSON_FORMAT):
            raise ValueError("Định dạng gói bài tập không hỗ trợ.")
        is_lesson = manifest["format"] == LESSON_FORMAT
        is_topic = manifest["format"] != FORMAT
        if is_topic != ("topic" in manifest):
            raise ValueError("Thông tin chủ đề trong gói không hợp lệ.")
        title, author, language, family, rows = (
            manifest.get(key) for key in ("title", "author", "language", "family", "questions")
        )
        if (not isinstance(title, str) or not title.strip() or len(title) > 120
                or not isinstance(author, str) or len(author) > 100 or language not in ("en", "vi")
                or not isinstance(family, str) or not re.fullmatch(r"[0-9a-f]{64}", family)
                or not isinstance(rows, list) or len(rows) > MAX_ITEMS or (not rows and not is_lesson)):
            raise ValueError("Thông tin gói bài tập không hợp lệ.")
        referenced = set()

        def check_ref(ref):
            if not isinstance(ref, str) or ref not in assets:
                raise ValueError(f"Gói thiếu tệp đính kèm: {ref}")
            referenced.add(ref)
            return ref

        checked = []
        topic = _topic_metadata(manifest["topic"]) if is_topic else None
        content = None
        if is_lesson:
            content = _lesson_content(manifest.get("lesson_content"), topic, language, check_ref)
            if not any(content.values()):
                raise ValueError("Gói chưa có nội dung bài học.")
        for row in rows:
            _check_question(row)
            packed = _media(row, check_ref)
            if topic is not None:
                packed["level"], packed["lesson"] = _topic_position(packed, topic)
            checked.append(packed)
        if referenced != set(assets) or len({row["id"] for row in checked}) != len(checked):
            raise ValueError("Gói có tệp không sử dụng hoặc mã câu hỏi bị trùng.")
        ordered = sorted(checked, key=lambda row: row["id"])
        payload = [topic, ordered, content] if is_lesson else ordered if topic is None else [topic, ordered]
        revision = _digest(_json(payload))
        return QuestionPackage(title, author, language, family, revision, checked, assets, topic, content)
    except (BadZipFile, KeyError, TypeError, RuntimeError, RecursionError, NotImplementedError) as exc:
        raise ValueError("Không đọc được gói bài tập.") from exc


def _existing(path, kind="questions"):
    from tuhoc.lessons.level_flow import load_rows

    rows = (json.loads(path.read_text(encoding="utf-8-sig")) if path.exists()
            else load_rows(path.parent.parent, kind, None))
    if not isinstance(rows, list):
        raise ValueError("Danh sách bài tập hiện tại không hợp lệ.")
    return rows


def _status(package, rows):
    versions = []
    for row in rows:
        source = row.get("shared_source") if isinstance(row, dict) else None
        if isinstance(source, dict) and source.get("family") == package.family:
            versions.append(source.get("revision"))
    return "duplicate" if package.revision in versions else "update" if versions else "new"


def package_status(package, data_dir):
    if package.lesson_content is not None:
        from tuhoc.ui.theme_config import load
        return _status(package, load(data_dir))
    return _status(package, _existing(Path(data_dir) / "content_library" / "level_questions.json"))


def import_package(package, data_dir, language, theme, level, lesson, *, allow_update=False):
    from tuhoc.ui.theme_config import lesson_count, max_level, tuples

    if package.topic is not None:
        raise ValueError("Gói chủ đề cần được nhập thành chủ đề mới.")
    if package.language != language:
        raise ValueError("Hãy mở đúng môn học của gói trước khi nhập.")
    if (theme not in {item[0] for item in tuples(data_dir)}
            or not 1 <= level <= max_level(data_dir, theme)
            or not 1 <= lesson <= lesson_count(data_dir, theme, level)):
        raise ValueError("Chủ đề, Level hoặc Lesson đích không hợp lệ.")
    return _import(package, data_dir, (theme, level, lesson), allow_update=allow_update)[0]


def suggested_topic_title(package):
    suffix = f" · từ {package.author}" if package.author else " · Chia sẻ"
    return package.topic["title"] + suffix


def import_topic_package(package, data_dir, language, *, allow_update=False, topic_title=None):
    if package.topic is None:
        raise ValueError("Tệp này là gói bài tập theo Lesson.")
    if package.language != language:
        raise ValueError("Hãy mở đúng môn học của gói trước khi nhập.")
    title = topic_title.strip() if topic_title else suggested_topic_title(package)
    if not title:
        title = suggested_topic_title(package)
    return _import(package, data_dir, None, allow_update=allow_update, topic_title=title)


def _import(package, data_dir, placement, *, allow_update, topic_title=None):
    from tuhoc.ui import theme_config

    library = Path(data_dir) / "content_library"
    question_path = library / "level_questions.json"
    with _locked(library):
        current = _existing(question_path)
        lesson_pack = package.lesson_content is not None
        catalog = theme_config.load(data_dir) if package.topic is not None else None
        status = _status(package, catalog if lesson_pack else current)
        if status == "duplicate":
            return 0, None
        if status == "update" and not allow_update:
            raise ValueError("Gói đã có phiên bản trước. Hãy xác nhận nhập bản mới.")
        topic = package.topic
        source = {"title": package.title, "author": package.author,
                  "family": package.family, "revision": package.revision}
        changes = {}
        if topic is not None:
            theme = f"shared-{uuid4().hex}"
            base_title = topic_title
            titles = {entry["title"].casefold() for entry in catalog}
            title = base_title
            number = 2
            while title.casefold() in titles:
                title = f"{base_title} ({number})"
                number += 1
            changes[theme_config.path_for(data_dir)] = [
                *catalog, {**topic, "code": theme, "title": title, "shared_source": source},
            ]
        else:
            theme, level, lesson = placement
        media_dir = library / "media" / f"shared-{uuid4().hex}"
        written = []
        filenames = {}
        try:
            if package.assets:
                media_dir.mkdir(parents=True)
                for number, (ref, payload) in enumerate(sorted(package.assets.items()), 1):
                    name = f"{number}{Path(ref).suffix}"
                    filenames[ref] = name
                    target = media_dir / name
                    written.append(target)
                    target.write_bytes(payload)
            def media_ref(ref):
                return f"media/{media_dir.name}/{filenames[ref]}"

            additions = []
            for row in package.questions:
                if topic is not None:
                    level, lesson = _topic_position(row, topic)
                copied = _media(row, media_ref)
                copied.update(
                    id=f"shared-{uuid4().hex}", theme=theme, level=level, lesson=lesson,
                    shared_source=source,
                )
                additions.append(copied)
            if additions:
                changes[question_path] = current + additions
            lesson_count = 0
            if lesson_pack:
                for kind, rows in _lesson_content(package.lesson_content, topic, language=package.language,
                                                  replace=media_ref).items():
                    if not rows:
                        continue
                    target = library / f"level_{kind}.json"
                    for row in rows:
                        row.update(theme=theme, id=f"shared-{uuid4().hex}")
                    changes[target] = _existing(target, kind) + rows
                    lesson_count += len(rows)
            commit_json(changes)
        except Exception:
            for target in written:
                target.unlink(missing_ok=True)
            if package.assets and media_dir.is_dir():
                media_dir.rmdir()
            raise
    return len(additions) + lesson_count, theme
