import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from bits_count import count_bits_logical_mul
from test_lib.test_case import MultiResultTestCase
from test_lib.test_runner import TestRunner


INT_64_MASK = 18446744073709551615
INT_64_LEFT_COLUMN = 72340172838076673
INT_64_RIGHT_COLUMN = 9259542123273814144
INT_64_UPPER_ROW = 18374686479671623680
INT_64_LOWER_ROW = 255
INT_64_BOARD_BORDER_MASK = 18411139144890810879
INT_64_DOUBLE_LEFT_COLUMN = 217020518514230019
INT_64_DOUBLE_RIGHT_COLUMN = 13889313184910721216


def idx_to_board_position(idx: str) -> int:
    idx: int = int(idx)
    return 2 ** idx


def king_walk(position):
    # check left upper corner: king_walk(72057594037927936)
    position = idx_to_board_position(position)

    up_down = position >> 8 | position << 8
    left_right = position << 1 | position >> 1
    left_diag = position >> 7 | position << 7
    right_diag = position >> 9 | position << 9

    possible_walk = up_down | left_right | left_diag | right_diag
    possible_walk = possible_walk & INT_64_MASK

    is_on_left_edge = position & INT_64_LEFT_COLUMN > 0
    is_on_right_edge = position & INT_64_RIGHT_COLUMN > 0

    if is_on_left_edge:
        possible_walk = possible_walk & (INT_64_MASK ^ INT_64_RIGHT_COLUMN)
        return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))
    elif is_on_right_edge:
        possible_walk = possible_walk & (INT_64_MASK ^ INT_64_LEFT_COLUMN)
        return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))
    else:
        return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))


def bishop_walk(position, on_queen_service=False):
    if not on_queen_service:
        position = idx_to_board_position(position)

    upper_right = position
    upper_left = position
    lower_right = position
    lower_left = position

    while upper_left & (INT_64_LEFT_COLUMN | INT_64_UPPER_ROW) < 1:
        upper_left = upper_left | (upper_left << 7)

    while lower_left & (INT_64_LOWER_ROW | INT_64_LEFT_COLUMN) < 1:
        lower_left = lower_left | (lower_left >> 9)

    while upper_right & (INT_64_UPPER_ROW | INT_64_RIGHT_COLUMN) < 1:
        upper_right = upper_right | (upper_right << 9)

    while lower_right & (INT_64_LOWER_ROW | INT_64_RIGHT_COLUMN) < 1:
        lower_right = lower_right | (lower_right >> 7)

    possible_walk = (upper_left | lower_left | upper_right | lower_right) & INT_64_MASK

    if on_queen_service:
        return possible_walk

    return (str(count_bits_logical_mul(possible_walk ^ position)), str(possible_walk ^ position))


def rook_walk(position, on_queen_service=False):
    if not on_queen_service:
        position = idx_to_board_position(position)

    up = position
    down = position
    right = position
    left = position

    while up & INT_64_UPPER_ROW <= 1:
        up =  up | up << 8

    while down & INT_64_LOWER_ROW < 1:
        down = down | down >> 8

    while right & INT_64_RIGHT_COLUMN <= 1:
        right = right | right << 1

    while left & INT_64_LEFT_COLUMN < 1:
        left = left | left >> 1

    possible_walk = (up | down | left | right) & INT_64_MASK

    if on_queen_service:
        return possible_walk

    return (str(count_bits_logical_mul(possible_walk ^ position)), str(possible_walk ^ position))


def queen_walk(position):
    position = idx_to_board_position(position)

    like_rook = rook_walk(position, True)
    like_bishop = bishop_walk(position, True)

    possible_walk = (like_rook | like_bishop) ^ position

    return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))


def knight_walk(position):
    position = idx_to_board_position(position)

    upper_left = position << 6 | position << 15
    upper_right = position << 10 | position << 17
    lower_left = position >> 6 | position >> 15
    lower_right = position >> 10 | position >> 17

    possible_walk = upper_left | upper_right | lower_left | lower_right
    possible_walk = possible_walk & INT_64_MASK

    is_on_left_edge = position & INT_64_DOUBLE_LEFT_COLUMN > 0
    is_on_right_edge = position & INT_64_DOUBLE_RIGHT_COLUMN > 0

    if is_on_left_edge:
        possible_walk = possible_walk & (INT_64_MASK ^ INT_64_DOUBLE_RIGHT_COLUMN)
        return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))
    elif is_on_right_edge:
        possible_walk = possible_walk & (INT_64_MASK ^ INT_64_DOUBLE_LEFT_COLUMN)
        return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))

    return (str(count_bits_logical_mul(possible_walk)), str(possible_walk))



def main():
    pieces_data_map = {
        "knight": knight_walk,
        "king": king_walk,
        "bishop": bishop_walk,
        "rook": rook_walk,
        "queen": queen_walk
    }
    common_ascii_table = ""

    for k, v in pieces_data_map.items():
        test_data_dir = os.getcwd() + "/test_data/" + k
        runner = TestRunner(dir_name=test_data_dir, test_case_cls=MultiResultTestCase)
        runner.run_tests(v)
        ascii_str_result = "\n\n" + f"{v.__name__}\n" + runner.render_as_ascii_table()
        common_ascii_table += ascii_str_result

    print(common_ascii_table)
    result_file = os.getcwd() + "/result.txt"
    runner.write_to_file(common_ascii_table, result_file)


if __name__ == "__main__":
    main()
