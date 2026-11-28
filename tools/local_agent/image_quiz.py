"""Image quiz recognition, answer mapping and independent review requests."""

import json
import re
from io import BytesIO

from PIL import Image

from tools.fixtures.build_image_quiz_drafts import select_answer

SUPPORTED = {"image_sentence_fill", "listening_image_choice"}
RULE_VERSION = 5
PROMPT_CONTRACT_VERSION = 2


def obj(**fields):
    return {"type": "object", "properties": fields, "required": list(fields),
            "additionalProperties": False}


def array(items):
    return {"type": "array", "items": items}


STRING = {"type": "string"}
INDEX = {"anyOf": [{"type": "integer"}, {"type": "null"}]}
BOX = array({"type": "integer"})
VISION = obj(type=STRING, prompt=STRING, blank_text=STRING, options=array(STRING),
             crop=BOX, choices=array(obj(label=STRING, crop=BOX)), uncertainty=STRING)
ANSWER = obj(answer_index=INDEX, evidence=STRING)
REVIEW = obj(differences=array(STRING), evidence=STRING)


def validate(value, schema):
    """Validate the small JSON Schema subset used by the prompts."""
    if "anyOf" in schema:
        if value is None:
            return
        validate(value, schema["anyOf"][0])
        return
    kind = schema["type"]
    expected = {"object": dict, "array": list, "string": str, "integer": int,
                "null": type(None)}[kind]
    if type(value) is not expected:
        raise ValueError(f"JSON không đúng kiểu {kind}.")
    if kind == "object":
        fields = schema["properties"]
        if value.keys() != fields.keys():
            raise ValueError("JSON thiếu trường hoặc có trường ngoài schema.")
        for key, field in fields.items():
            validate(value[key], field)
    elif kind == "array":
        for item in value:
            validate(item, schema["items"])


RECOGNIZE = """Transcribe the exercise. prompt is the instruction only. Types:
image_sentence_fill: one pictured one-word blank. Put sentence with one .... in blank_text, text options in source order in options, artwork in crop, and choices=[].
listening_image_choice: audio plus image options. Each choices item contains visible label (or "") and artwork crop in source order. Set blank_text="", options=[], crop=[] unless there is separate prompt art.
Otherwise type=unsupported, describe interaction in uncertainty and leave unused fields empty.
Boxes [left,top,right,bottom] use normalized 0–1000 coordinates, excluding UI, captions and controls.
Do not guess or solve. uncertainty="" when transcription is clear; otherwise state the specific ambiguity briefly."""
SOLVE = """Determine the zero-based answer for this image and transcribed draft. Give concise evidence from visible facts that uniquely identify the answer. A learner's selection alone is insufficient. Return null with a reason if uncertain."""
CHECK = """Independently compare draft to image. Inspect exact wording, option order, labels, every crop (normalized 0–1000), added or missing content, and type. List specific differences or uncertainties, including unverified crops. Check proposed answer evidence. Preserve supplied answers and report clear contradictions. Audio is not provided. Give brief concrete evidence of your checks even if differences=[]."""


def pixel_box(box, size):
    if len(box) != 4 or any(not 0 <= value <= 1000 for value in box):
        raise ValueError("Vùng cắt không đúng hệ tọa độ 0–1000.")
    return [round(value * dimension / 1000) for value, dimension in zip(box, size * 2)]


def pixel_draft(draft, size):
    return {
        **draft,
        "crop": pixel_box(draft["crop"], size) if draft["crop"] else [],
        "choices": [{**choice, "crop": pixel_box(choice["crop"], size)}
                    for choice in draft["choices"]],
    }


def inspect_geometry(draft, size):
    width, height = size
    boxes = [choice["crop"] for choice in draft["choices"]]
    if draft["crop"]:
        boxes.append(draft["crop"])
    for box in boxes:
        if len(box) != 4:
            raise ValueError("Vùng cắt cần bốn tọa độ.")
        left, top, right, bottom = box
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise ValueError("Vùng cắt nằm ngoài ảnh hoặc rỗng.")
        if (left, top, right, bottom) == (0, 0, width, height):
            raise ValueError("Vùng cắt chứa toàn bộ ảnh câu hỏi.")
    if len({tuple(box) for box in boxes}) != len(boxes):
        raise ValueError("Vùng cắt trùng nhau.")


def options_for(draft):
    if not draft["prompt"].strip():
        raise ValueError("Thiếu câu dẫn.")
    if draft["type"] == "image_sentence_fill":
        options = draft["options"]
        if (draft["choices"] or not draft["crop"] or len(options) < 2
                or any(not option.strip() for option in options)
                or len({option.strip() for option in options}) != len(options)
                or len(re.findall(r"\.{3,}", draft["blank_text"])) != 1
                or not re.search(r"(?<![\w.])\.{3,}(?![\w.])", draft["blank_text"])):
            raise ValueError("Câu điền cần hình, một ô trống và các lựa chọn riêng biệt.")
        return options
    if draft["options"] or draft["blank_text"] or not 2 <= len(draft["choices"]) <= 6:
        raise ValueError("Câu nghe cần từ hai đến sáu ảnh lựa chọn.")
    return [choice["label"] for choice in draft["choices"]]


def supplied_answer(options, value):
    if type(value) is str:
        matches = [index for index, label in enumerate(options) if label == value]
        if len(matches) != 1:
            raise ValueError("Đáp án cung cấp không khớp duy nhất một lựa chọn.")
        value = matches[0]
    select_answer(options, value)
    return {"answer_index": value, "evidence": "Đáp án do người dùng cung cấp."}


def evaluate(row, image, supplied, stage, *, require_supplied=False):
    with Image.open(BytesIO(image)) as source:
        if source.format != "PNG":
            raise ValueError("Tệp nguồn có đuôi .png nhưng nội dung không phải PNG.")
        size = source.size
    draft = stage("vision", VISION, RECOGNIZE, {"source_pixels": size})
    if draft["type"] not in SUPPORTED:
        return "unsupported", draft, draft["uncertainty"] or draft["type"] or "Dạng chưa được nhận diện."

    if draft["type"] == "image_sentence_fill":
        # Some responses repeat the same text options in the image-only field.
        # Keep the ordered text options when the labels agree exactly.
        if [choice["label"] for choice in draft["choices"]] == draft["options"]:
            draft = {**draft, "choices": []}
        draft = {**draft, "blank_text": re.sub(r"\.{3,}", "....", draft["blank_text"])}

    answer = {"answer_index": None, "evidence": "Chưa có căn cứ đáp án."}
    issues = []
    converted = {}
    try:
        converted = pixel_draft(draft, size)
        inspect_geometry(converted, size)
        options = options_for(draft)
        if draft["type"] == "image_sentence_fill" and (
            row["audio"] or re.search(r"\b(?:listen(?:ing)?|nghe)\b", draft["prompt"], re.IGNORECASE)
        ):
            raise ValueError("Dạng điền từ này sẽ bỏ phần nghe. Cần xác minh dạng bài từ nguồn.")
        if draft["type"] == "listening_image_choice" and not row["media_valid"]:
            raise ValueError(row["media_issue"])
        if supplied is not None:
            answer = supplied_answer(options, supplied)
        elif require_supplied:
            raise ValueError("Chưa có đáp án cho câu này trong file người dùng cung cấp.")
        elif draft["type"] == "image_sentence_fill":
            answer = stage("answer", ANSWER, SOLVE, draft)
        if answer["answer_index"] is None or not answer["evidence"].strip():
            raise ValueError(answer["evidence"] if answer["answer_index"] is None
                             and answer["evidence"].strip() else "Thiếu căn cứ đáp án.")
        select_answer(options, answer["answer_index"])
    except ValueError as exc:
        issues.append(str(exc))

    review = stage("review", REVIEW, CHECK, {
        "source_pixels": size, "draft": draft, "answer": answer,
        "supplied": supplied, "audio": row["audio"], "media_sha256": row["media_sha256"],
    })
    issues.extend(review["differences"])
    if draft["uncertainty"].strip():
        issues.append(draft["uncertainty"])
    if not review["evidence"].strip():
        issues.append("Thiếu căn cứ đối chiếu.")
    notes = " | ".join(filter(None, [answer["evidence"], review["evidence"], *issues]))
    return ("needs_review" if issues else "passed",
            {**converted, "answer_index": answer["answer_index"]}, notes)
