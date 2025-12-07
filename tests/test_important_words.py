
from tests.conftest import pytest, patch, Mock

from src.important_words import word_search

@pytest.mark.parametrize(
    'args, expected',
    [
        (
                ["this is a sentence that is separated by spaces that has at least one word that is found at least three times",
                2],
                ['is', 'that', 'at', 'least']
        ),
        (
                ["this is a sentence that is separated by spaces that has at least one word that is found at least three times",
                3],
                ['is', 'that']
        )

    ]
)
def test_word_search(args, expected):
    result = word_search(args[0], args[1])
    assert result == expected