"""Split Vietnamese and English prose into draft reading segments."""
import re

_BOUNDARY = re.compile(r"""[.!?…]+[”’"')\]]*|\r\n?|\n""")
_ABBREVIATIONS = frozenset({'mr', 'mrs', 'ms', 'dr', 'prof', 'th.s', 'ts', 'pgs', 'tp'})


def split_sentences(text):
    """Keep ending punctuation and quotes, and treat each new line as a boundary."""
    sentences = []
    start = 0
    for match in _BOUNDARY.finditer(text):
        end = match.end()
        if match.group() == '.' and end < len(text):
            before = text[start:match.start()]
            if before and before[-1].isdigit() and text[end].isdigit():
                continue
            preceding_word = before.rsplit(maxsplit=1)[-1].casefold() if before.strip() else ''
            if preceding_word in _ABBREVIATIONS and text[end:].lstrip():
                continue
        sentence = text[start:end].strip()
        if sentence:
            sentences.append(sentence)
        start = end
    tail = text[start:].strip()
    if tail:
        sentences.append(tail)
    return sentences
