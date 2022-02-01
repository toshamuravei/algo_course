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


class SuffixShifter:
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
    shifter: SuffixShifter = SuffixShifter(pattern)
    i = 0

    while i <= text_length - pattern_length:
        j = pattern_length - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            match_indecies.append(i)

        shift_char = text[i + pattern_length - 1]
        i += shifter.get_shift_from_char(shift_char)

    return match_indecies


class BoyerMoorePreprocessing:
    ALPHABET_LENGTH = 128

    def __init__(self, pattern):
        self.pattern = pattern
        self.bad_chars_table = self._init_bad_character_table(pattern)
        self.good_suffix_table = self._init_good_suffix_table()

    def _init_bad_character_table(self, pattern):
        bad_chars = [len(pattern) for i in range(0, self.ALPHABET_LENGTH)]

        for char_idx in range(0, len(pattern)):
            char = pattern[char_idx]
            char_shift = abs((1 + char_idx) - len(pattern))
            bad_chars[ord(char)] = char_shift

        last_char_ord = ord(pattern[-1])
        bad_chars[last_char_ord] = len(pattern)
        return bad_chars

    def _init_good_suffix_table(self) -> List[int]:
        table = [None] * len(self.pattern)
        last_prefix_pos = len(self.pattern)
        last_pattern_idx = len(self.pattern) - 1

        for i in range(last_pattern_idx, -1, -1):
            if self._is_prefix(i + 1):
                last_prefix_pos = i + 1
            table[last_pattern_idx - i] = last_prefix_pos - i + last_pattern_idx

        for i in range(0, last_pattern_idx):
            suffix_len = self._max_suffix_len(i)
            table[suffix_len] = last_pattern_idx - i + suffix_len

        return table

    def _is_prefix(self, prefix_pos) -> bool:
        j = 0
        for i in range(prefix_pos, len(self.pattern)):
            if self.pattern[i] != self.pattern[j]:
                return False
            j += 1
        return True

    def _max_suffix_len(self, suffix_pos) -> int:
        suffix_len = 0
        i = suffix_pos
        j = len(self.pattern) - 1
        while i >= 0 and self.pattern[i] == self.pattern[j]:
            suffix_len += 1
            i -= 1
            j -= 1
        return suffix_len

    def get_max_shift(self, shift: int, text_char: int, pattern_pos: int) -> int:
        pattern_last_idx = len(self.pattern) - 1
        suffix_shift = self.good_suffix_table[pattern_last_idx - pattern_pos]
        bad_char_shift = self.bad_chars_table[ord(text_char)]
        return max(bad_char_shift, shift, suffix_shift)

    def get_max_shift_on_match(self, shift: int) -> int:
        pattern_last_idx = len(self.pattern) - 1
        suffix_shift = self.good_suffix_table[pattern_last_idx] - 1
        print(f"\nDeciding on match shift: choosing between shift: {shift} and gs: {suffix_shift}")
        return max(suffix_shift, shift)


def boyer_moore_search(text: str, pattern: str) -> List[int]:
    match_indecies = []
    pattern_length = len(pattern)
    text_length = len(text)
    text_cursor = 0
    preprocessing = BoyerMoorePreprocessing(pattern)

    while text_cursor < text_length - pattern_length + 1:
        shift = 1
        mismatched = False
        for pattern_cursor in range(pattern_length - 1, -1, -1):
            pattern_char = pattern[pattern_cursor]
            text_char = text[text_cursor + pattern_cursor]
            print(f"Comparing: pattern: {pattern_char} - text: {text_char}")
            if pattern_char != text_char:
                shift = preprocessing.get_max_shift(
                    shift,
                    text_char,
                    pattern_cursor
                )
                mismatched = True
                break
        if not mismatched:
            match_indecies.append(text_cursor)
            shift = preprocessing.get_max_shift_on_match(shift)
        print(f"\n Shifting {text_cursor} on {shift}\n")
        text_cursor += shift

    return match_indecies

