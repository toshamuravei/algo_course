import os
import sys
from copy import copy
from math import ceil, sqrt
from typing import List


root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_lib.test_runner import TestRunner


def recursive_fibo(n: str) -> int:
    n: int = int(n)
    base_fibo: List = [0, 1, 1]
    if n <= 2:
        return base_fibo[n]

    last = str(n - 1)
    pre_last = str(n - 2)

    return recursive_fibo(last) + recursive_fibo(pre_last)


def iterative_fibo(n: str) -> int:
    n: int = int(n)
    fibo_list: List = [0, 1]

    if n < len(fibo_list):
        return fibo_list[n]

    for i in range(2, n + 1):
        fibo_list[i % 2] = fibo_list[0] + fibo_list[1]

    return fibo_list[0] if fibo_list[0] > fibo_list[1] else fibo_list[1] # or just max(fibo_list)


def golden_ratio_fibo(n: str) -> int:
    n: int = int(n)
    first_n_fibo_numbers = [0, 1, 1, 2, 3, 5]
    if n < len(first_n_fibo_numbers):
        return first_n_fibo_numbers[n]

    golden_ratio = 1.61803398874989484

    try:
        fibo_num = ceil(((golden_ratio ** n)/sqrt(5)) + 0.5)
    except OverflowError:
        fibo_num = 0

    return fibo_num


class FiboMatrix:

    def __init__(self, item_00=1, item_01=1, item_10=1, item_11=0):
        self.value = [
            [item_00, item_01],
            [item_10, item_11]
        ]

    def __mul__(self, other):
        item_00 = self.value[0][0] * other.value[0][0] + self.value[0][1] * other.value[1][0]
        item_01 = self.value[0][0] * other.value[0][1] + self.value[0][1] * other.value[1][1]
        item_10 = self.value[1][0] * other.value[0][0] + self.value[1][1] * other.value[1][0]
        item_11 = self.value[1][0] * other.value[0][1] + self.value[1][1] * other.value[1][1]

        return self.__class__(item_00, item_01, item_10, item_11)

    def __pow__(self, power_number):
        power_number = int(power_number)
        if power_number == 0:
            return self.__class__(0, 0, 0, 0)

        quotient = power_number
        remainder = 0
        result = self.__class__(1, 0, 0, 1) # identity matrix
        count = 0

        while True:
            if quotient == 1 and remainder <= 1:
                result = result * self.square_n_times(copy(self), count)
                break

            quotient, remainder = divmod(quotient, 2)
            if remainder:
                result = result * self.square_n_times(copy(self), count)
            count += 1
        return result

    @staticmethod
    def square_n_times(matrix_to_power, n_of_squares):
        result = matrix_to_power
        for i in range(0, n_of_squares):
            result = result * result
        return result

    def __repr__(self):
        return f"{self.value[0][0]} {self.value[0][1]}\n{self.value[1][0]} {self.value[1][1]}"


def matrix_fibo(n: str) -> int:
    n: int = int(n)
    matrix = FiboMatrix() ** n
    return matrix.value[0][1]

if __name__ == "__main__":
    print(golden_ratio_fibo(64))
    test_data_dir = os.getcwd() + "/test_data"
    runner = TestRunner(dir_name=test_data_dir, run_until="test.8.in")

    funcs_to_run = [matrix_fibo, iterative_fibo, golden_ratio_fibo]
    results = runner.run_competitive(funcs_to_run)
    ascii_table_result = runner.render_ascii_competitive_results()
    result_file = os.getcwd() + "/result.txt"
    runner.write_to_file(ascii_table_result, result_file)
    print(ascii_table_result)


