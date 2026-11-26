import pytest

from tuhoc.library.models import parse_dictation_fields
from tuhoc.library.text_split import split_sentences


@pytest.mark.parametrize(('body', 'sentences'), [
    ('Em đi học. Bạn có đi không? Có!', ['Em đi học.', 'Bạn có đi không?', 'Có!']),
    ('  Một…Hai?!\r\n\nBa\rBốn  ', ['Một…', 'Hai?!', 'Ba', 'Bốn']),
    ('“Chào em!” She is Dr. Lan. It costs 3.14 dollars.',
     ['“Chào em!”', 'She is Dr. Lan.', 'It costs 3.14 dollars.']),
    ('\t \n ', []),
    ('Không có dấu chấm', ['Không có dấu chấm']),
])
def test_split_sentences(body, sentences):
    assert split_sentences(body) == sentences


def test_old_dictation_editor_format():
    assert parse_dictation_fields('One answer\n\nOther answer', "he is | he's\nStandalone") == {
        'accepted_variants': ['One answer', 'Other answer', 'Standalone'],
        'equivalences': [['he is', "he's"]],
    }
