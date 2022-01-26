import string

import pytest

from boyer_moore.search import (
    boyer_moore_search,
    naive_search,
    naive_search_prefix_shift,
    naive_search_suffix_shift
)


TEXT_SIZE = 9
PATTERN_SIZE = 3



@pytest.fixture
def _pattern_text_answer():
    ALPHABET = [x for x in string.printable]


@pytest.fixture
def pattern_text_answer():
        return "abcde", "12nnfabcd,..fabc0rjq42abcdeasfabcde", [22, 30]


def test_naive_search(pattern_text_answer):
    pattern, text, answer = pattern_text_answer
    result = naive_search(text, pattern)
    assert result == answer


def test_naive_search_prefix_shift(pattern_text_answer):
    pattern, text, answer = pattern_text_answer
    result = naive_search_prefix_shift(text, pattern)
    assert result == answer


def test_naive_search_suffix_shift(pattern_text_answer):
    pattern, text, answer = pattern_text_answer
    result = naive_search_suffix_shift(text, pattern)
    assert result == answer


def test_boyer_moore_search(pattern_text_answer):
    pattern, text, answer = pattern_text_answer
    result = boyer_moore_search(text, pattern)
    assert result == answer

