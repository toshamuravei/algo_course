import os
import sys
from copy import copy
from math import ceil, sqrt
from typing import List

from texttable import Texttable


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_lib.test_runner import TestRunner
from test_lib.test_case import MultiArgumentTestCase


def simple_iterative_power(number: str, power_value: str) -> int:
    power_value, number = int(power_value), float(number)

    res: int = 1.0
    for p in range(1, power_value + 1):
        res = number * res
    return str(res)


def power_of_two_with_multiplication(number: str, power_value: str):
    power_value, number = int(power_value), float(number)
    if power_value == 0:
        return str(1.0)

    is_next_square_needed = lambda x: x * x <= power_value

    result = number
    power_of_two = 1

    while True:
        if not is_next_square_needed(power_of_two):
            break

        power_of_two = power_of_two * 2
        result *= result

    iterative_power = power_value - power_of_two
    if iterative_power:
        return str(result * float(simple_iterative_power(number, iterative_power)))
    else:
        return str(result)


def power_as_expansion_of_powers_of_two(number: str, power_value: str):
    power_value, number = int(power_value), float(number)
    if power_value == 0:
        return str(1.0)

    def square_n_times(number, n_of_squares):
        result = number
        for i in range(0, n_of_squares):
            result = result * result
        return result


    quotient = power_value
    remainder = 0
    result = 1
    count = 0

    while True:
        if quotient == 1 and remainder <= 1:
            result = result * square_n_times(number, count)
            break

        quotient, remainder = divmod(quotient, 2)
        if remainder:
            result = result * square_n_times(number, count)
        count += 1
    return str(result)


if __name__ == "__main__":
    test_data_dir = os.getcwd() + "/test_data"
    runner = TestRunner(
        dir_name=test_data_dir,
        test_case_cls=MultiArgumentTestCase,
        run_until="test.7.in")

    funcs_to_run = [
        simple_iterative_power,
        power_of_two_with_multiplication,
        power_as_expansion_of_powers_of_two
    ]

    results = runner.run_competitive(funcs_to_run)
    ascii_table_result = runner.render_ascii_competitive_results()
    result_file = os.getcwd() + "/result.txt"
    runner.write_to_file(ascii_table_result, result_file)
    print(ascii_table_result)


