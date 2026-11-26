"""Chấm chính tả theo từ, dùng chung cho bài cũ và thư viện."""
import re
import unicodedata
from difflib import SequenceMatcher


# Dấu thanh kiểu cũ (hoà, khoẻ, thuỷ) và kiểu mới (hòa, khỏe, thủy) đều đúng chính tả.
# Chỉ đổi ở âm tiết mở kết thúc bằng oa/oe/uy; không đụng "qu", "oai", "huỳnh"...
_OLD_TONE_STYLE=re.compile('(?<!q)([ou])([aey])([\u0300\u0301\u0303\u0309\u0323])(?![\\w\u0300-\u036f])')
_VALID_OLD_PAIRS={('o','a'),('o','e'),('u','y')}


def _tone_new_style(match):
    first,second,tone=match.groups()
    if (first,second) not in _VALID_OLD_PAIRS:return match.group(0)
    return first+tone+second


def text_tokens(text):
    text=unicodedata.normalize('NFD',str(text)).casefold()
    text=unicodedata.normalize('NFC',_OLD_TONE_STYLE.sub(_tone_new_style,text))
    return re.findall(r'[^\W_]+',text,flags=re.UNICODE)


def _canonical_tokens(text, equivalences):
    """Replace explicitly authorized equivalent phrases with one comparison token.

    Sort by length so a longer expression wins over an overlapping short one.
    No automatic contraction expansion: e.g. 'he\'s' may mean 'he has'.
    """
    tokens=text_tokens(text)
    groups=[]
    for index, group in enumerate(equivalences or []):
        if not isinstance(group,(list,tuple)) or len(group)<2:
            continue
        for phrase in group:
            phrase_tokens=text_tokens(phrase)
            if phrase_tokens:
                groups.append((phrase_tokens, f'__equiv_{index}__'))
    groups.sort(key=lambda x:len(x[0]),reverse=True)
    output=[];i=0
    while i<len(tokens):
        found=next(((v,len(t)) for t,v in groups if tokens[i:i+len(t)]==t),None)
        if found:
            output.append(found[0]);i+=found[1]
        else:
            output.append(tokens[i]);i+=1
    return output


def check_dictation(expected, given, accepted_variants=None, equivalences=None):
    """Accent-sensitive word comparison, punctuation and casing ignored."""
    # A whole-answer variant is an alternative reference text; the highest score wins.
    candidates=[expected]+list(accepted_variants or [])
    if len(candidates)>1:
        results=[check_dictation(ref,given,equivalences=equivalences) for ref in candidates]
        best=max(results,key=lambda r:(r['passed'],r['score'],-len(r['issues'])))
        return dict(best, accepted_reference=candidates[results.index(best)])
    reference=_canonical_tokens(expected,equivalences)
    actual=_canonical_tokens(given,equivalences)
    matcher=SequenceMatcher(a=reference,b=actual,autojunk=False)
    correct=sum(block.size for block in matcher.get_matching_blocks())
    total=max(len(reference),len(actual),1)  # từ viết thừa cũng bị tính
    issues=[]
    for tag,a,b,c,d in matcher.get_opcodes():
        if tag=='equal':continue
        issues.append({'kind':tag,'expected':' '.join(reference[a:b]),'written':' '.join(actual[c:d])})
    return {'score':round(100*correct/total,1),'matched':correct,'total':len(reference),'issues':issues,
            'passed':len(reference)>0 and reference==actual}
