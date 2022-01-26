from typing import List


def naive_search(text: str, pattern: str) -> List[int]:
    match_indecies = []
    pattern_length = len(pattern)
    text_length = len(text)

    for i in range(text_length - pattern_length + 1):
        j = 0

        while (j < pattern_length):
            if (text[i + j] != pattern[j]):
                break
            j += 1

        if j == pattern_length:
            match_indecies.append(i)
    return match_indecies


def naive_search_prefix_shift(text: str, pattern: str) -> List[int]:
    match_indecies = []
    pattern_length = len(pattern)
    text_length = len(text)
    text_cursor = 0

    while text_cursor <= text_length - pattern_length:

        for pattern_cursor in range(0, pattern_length):
            if text[text_cursor + pattern_cursor] != pattern[pattern_cursor]:
                break
            pattern_cursor += 1

        if pattern_cursor == 0:
            text_cursor += 1
            continue

        if pattern_cursor == pattern_length:
            match_indecies.append(text_cursor)

        text_cursor += pattern_cursor

    return match_indecies


class Shifter:
    ALPHABET_LENGTH = 128

    def __init__(self, pattern: str):
        max_shift = len(pattern)
        self.shifts = [max_shift for i in range(0, self.ALPHABET_LENGTH)]
        self.update_shifts_with_pattern(pattern)

    def update_shifts_with_pattern(self, pattern: str) -> None:
        for char_idx in range(0, len(pattern)):
            char = pattern[char_idx]
            char_shift = abs((1 + char_idx) - len(pattern))
            self.shifts[ord(char)] = char_shift

        last_char_ord = ord(pattern[-1])
        self.shifts[last_char_ord] = len(pattern)

    def get_shift_from_char(self, char) -> int:
        return self.shifts[ord(char)]


def naive_search_suffix_shift(text: str, pattern: str) -> List[int]:
    match_indecies = []
    pattern_length = len(pattern)
    text_length = len(text)
    shifter: Shifter = Shifter(pattern)
    i = pattern_length - 1

    while i <= text_length - pattern_length:
        j = pattern_length - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            match_indecies.append(i)

        shift_char = text[i + pattern_length - 1]
        i += shifter.get_shift_from_char(shift_char)

    return match_indecies


def boyer_moore_search(text: str, pattern: str) -> List[int]:
    return []

