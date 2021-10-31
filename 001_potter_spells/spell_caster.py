import argparse
from copy import copy
from typing import Dict, List, Optional
from math import sqrt


class SpellConditionError(Exception):
    pass


class SpellCasterError(Exception):
    pass


_SPELL_CONDITION_MAP = {
    "01.jpg": lambda h, w: h < w,
    "02.jpg": lambda h, w: h == w,
    "03.jpg": lambda h, w: h + w == 24,
    "04.jpg": lambda h, w: h + w - 5 <= 24,
    "05.jpg": lambda h, w: w - 1 <= h * 2 <= w,
    "06.jpg": lambda h, w: w < 10 or h < 10,
    "07.jpg": lambda h, w: w > 15 and h > 15,
    "08.jpg": lambda h, w: h * w == 0,
    "09.jpg": lambda h, w: abs(h - w) >= 11,
    "10.jpg": lambda h, w: 0 < (w - h) <= (h + 1),
    "18.jpg": lambda w, h: (w * h) < (w + h),
    "19.jpg": lambda h, w: (h * w) * (w - 24) * (h - 24) == 0,
    "20.jpg": lambda h, w: (h + w) % 2 == 0,
    "22.jpg": lambda h, w: ((h * 10) + w) % 3 == 0,
    "23.jpg": lambda h, w: (h % 3) + (w % 2) == 0,
    "24.jpg": lambda h, w: (h == w) or (h + w == 26),
    "25.jpg": lambda h, w: (h % 6) * (w % 6) == 0
}

_SPELL_SIZE = 25


class SpellCaster:
    def __init__(self, true_spell_symbol: str="#", false_spell_symbol="."):
        self._condition_map: Dict = _SPELL_CONDITION_MAP
        self._spell_size: int = _SPELL_SIZE
        if self._spell_size != 25:
            _err_msg: str = "I'm young wizard and can create only 25 sized square spells!"
            raise SpellCasterError(_err_msg)

        self._true_spell_symbol: str = true_spell_symbol + " "
        self._false_spell_symbol: str = false_spell_symbol + " "


    def get_spell_letter(self, height: int, width: int, spell_name: str) -> str:
        if spell_name not in self._condition_map.keys():
            _err_msg: str = "I didn't invented such spell yet, Potter!"
            raise SpellConditionError(_err_msg)

        condition: bool = self._condition_map[spell_name](height, width)

        return self._true_spell_symbol if condition else self._false_spell_symbol


    def cast_spell(self, spell_name: Optional[str]=None) -> str:
        spell_string = ""
        if spell_name:
            for height in range(0, self._spell_size):
                for width in range(0, self._spell_size):
                    spell_string += self.get_spell_letter(height, width, spell_name)
                spell_string += "\n"
            return spell_string
        else:
            for s in self._condition_map.keys():
                spell_string = spell_string + "\n" + self.cast_spell(s)

        return spell_string



def main(spell_name: Optional[str]=None):
    caster = SpellCaster()
    print(caster.cast_spell(spell_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Wonderful spellcasting')
    parser.add_argument('--spell_name', help='Spell name which is actiually picture name, like 01.jpg', default=None)
    args = parser.parse_args()

    main(args.spell_name)

