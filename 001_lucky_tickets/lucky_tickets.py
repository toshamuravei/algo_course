import os
import sys
from typing import List

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_lib.test_runner import TestRunner


def get_next_list(previous_list: List) -> List:
    """
    Dynamically get next combinations list depending on given.
    Assuming that next list is always 9 items longer.
    """
    new_list_length: int = len(previous_list) + 9
    new_list: List = [0 for i in range(0, new_list_length)]
    for new_list_idx in range(0, new_list_length):
        sum_combinations: int = 0
        for i in range(0, 10): # every next list is exactly 9 items "longer"
            # evade python's negative indexing
            if (new_list_idx - i) in range(0, len(previous_list)):
                sum_combinations += previous_list[new_list_idx - i]
            else:
                continue
        new_list[new_list_idx] = sum_combinations
    return new_list


def count_lucky_tickets(num: str) -> int:
    """
    Counting lucky tickets as sum of squares of lucky coumbinations
    numbers, calculated in get_next_list().
    """
    num: int = int(num)
    combinations_list: List = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,] # default single (double: A-B) digit ticket
    lucky_count: int = 0
    for i in range(0, (num - 1)):
        combinations_list = get_next_list(combinations_list)
    for combination in combinations_list:
        lucky_count += combination ** 2
    return lucky_count


if __name__ == "__main__":
    test_data_dir = os.getcwd() + "/test_data"
    runner = TestRunner(dir_name=test_data_dir)
    runner.run_tests(count_lucky_tickets)

    ascii_table_result = runner.render_as_ascii_table()
    result_file = os.getcwd() + "/result.txt"
    runner.write_to_file(ascii_table_result, result_file)
    print(ascii_table_result)

