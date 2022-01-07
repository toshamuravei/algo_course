import os
import sys
from math import ceil, sqrt

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_lib.test_runner import TestRunner


def is_prime_simple(number):
    for i in range(2, number):
        if number % i == 0:
            return False
    return True


def iterative_primes(until_number: str) -> int:
    until_number: int = int(until_number)
    how_many_primes = 0
    for i in range(2, until_number + 1):
        if is_prime_simple(i):
            how_many_primes += 1

    return how_many_primes

def is_prime_iterative(number):
    if number == 2:
        return True

    if number % 2 == 0:
        return False

    sqrt_number = ceil(sqrt(number)) + 1

    for i in range(3, sqrt_number, 2):
        if number % i == 0:
            return False
    return True


def iterative_primes(until_number: str) -> int:
    until_number: int = int(until_number)
    primes = []
    how_many_primes = 0

    for i in range(2, until_number + 1):
        if is_prime_optimized(i):
            how_many_primes += 1

    return how_many_primes


def is_prime_optimized(number, primes):
    number = int(number)
    sqrt_number = ceil(sqrt(number)) + 1
    counter = 0

    while primes[counter] <= sqrt_number:
        if number % primes[counter] == 0:
            return False
        counter += 1
        if counter >= len(primes):
            break
    return True


def optimized_primes(number):
    number = int(number)
    how_many_primes = 1
    primes = [2,]

    if number < 2:
        return 0

    for i in range(3, number + 1, 2):
        if is_prime_optimized(i, primes):
            primes.append(i)
            how_many_primes += 1

    return how_many_primes


def eratosthenes_sieve(number):
    number = int(number)
    how_many_32_bit_chunks = ceil((number / 2) / 32)
    odd_dividers = [0 for chunk in range(0, how_many_32_bit_chunks)]
    dividers = [False for i in range(0, number + 1)]
    primes_count = 0

    for i in range(2, number + 1):
        if not dividers[i]:
            primes_count += 1
            if i <= ceil(sqrt(number)):
                for d in range(i * i, number + 1, i):
                    dividers[d] = True

    return primes_count


def eratosthenes_sieve_mem_optimized(number):
    number = int(number)
    odd_dividers = [0 for i in range(0, ceil(number / 32))]
    primes_count = 0

    def get_bit_idx(integer):
        return integer % 32

    def get_int_storage(integer):
        storage_idx = ceil(integer / 32) - 1
        return odd_dividers[storage_idx]

    def set_int_storage(integer, value):
        storage_idx = ceil(integer / 32) - 1
        odd_dividers[storage_idx] = value

    def get_bit(integer, bit_idx):
        return bool(integer >> bit_idx & 1)

    def set_bit(integer, bit_idx):
        return integer | (1 << bit_idx)

    for i in range(2, number + 1):
        is_set = get_bit(get_int_storage(i), get_bit_idx(i))
        if not is_set:
            primes_count += 1
            if i <= ceil(sqrt(number)):
                for d in range(i * i, number + 1, i):
                    bit_idx = get_bit_idx(d)
                    int_storage = get_int_storage(d)
                    new_int_storage = set_bit(int_storage, bit_idx)
                    set_int_storage(d, new_int_storage)

    return primes_count


def euler_sieve(number):
    number = int(number)
    numbers = [0 for i in range(0, number + 1)]
    primes = []

    for i in range(2, number + 1):
        if numbers[i] == 0:
            numbers[i] = i
            primes.append(i)

        for p in primes:
            if p > numbers[i] or p * i > number:
                break
            numbers[p * i] = p
    return str(len(primes))


def main():
    primes_func_map = {
        "euler_sieve": euler_sieve,
        "eratosthenes_sieve": eratosthenes_sieve,
        "eratosthenes_sienve_mem_optimizied": eratosthenes_sieve_mem_optimized,
        "optimized_primes": optimized_primes,
    }
    common_ascii_table = ""
    for k, v in primes_func_map.items():
        test_data_dir = os.getcwd() + "/test_data"
        runner = TestRunner(
            dir_name=test_data_dir,
            run_until="test.9.in")
        runner.run_tests(v)
        ascii_str_result = "\n\n" + f"{v.__name__}\n" + runner.render_as_ascii_table()
        common_ascii_table += ascii_str_result

    print(common_ascii_table)
    result_file = os.getcwd() + "/result.txt"
    runner.write_to_file(common_ascii_table, result_file)


if __name__ == "__main__":
    #print(euler_sieve(100))
    #print(eratosthenes_sieve_mem_optimized(100))
    main()

