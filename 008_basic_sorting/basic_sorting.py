import os
import time
from datetime import datetime
from random import randint
from typing import Dict, Callable, List

from texttable import Texttable

from bubble_sort import bubble_sort
from heap_sort import heap_sort
from insertion_sort import insertion_sort, insertion_sort_optimized
from quick_sort import quick_sort, quick_sort_improved
from merge_sort import merge_sort
from selection_sort import selection_sort
from shell_sort import shell_sort, shell_sort_sedgewick_82_gap, shell_sort_knuth_gap



SORTING_ALGORITHMS = {
    "bubble_sort": bubble_sort,
    "insertion_sort": insertion_sort,
    "insetion_sort_optimized": insertion_sort_optimized,
    "shell_sort": shell_sort,
    "shell_sort_knuth_gap": shell_sort_knuth_gap,
    "shell_sort_sedgewick_82": shell_sort_sedgewick_82_gap,
    "heap_sort": heap_sort,
    "selection_sort": selection_sort,
    "quick_sort": quick_sort,
    "quick_sort_improved": quick_sort_improved
}


def create_random_list(size: int) -> List:
    l = [randint(0, size) for i in range(0, size)]
    return l

def create_random_digits_list(size: int) -> List:
    l = [randint(0, 9) for i in range(0, size)]
    return l

def create_reversed_list(size: int) -> List:
    l = [i for i in range(size, 0, -1)]
    return l

def create_almost_sorted_list(size: int) -> List:
    l = [i for i in range(0, size)]
    temp = l[0]
    l[0] = l[-1]
    l[-1] = temp
    return l


def create_test_suite(list_fabric: Callable) -> Dict:
    test_suite = {
        "10^0": [1,],
    }
    for i in range(1, 7):
        test_suite[f"10^{i}"] = list_fabric(10**i)
    return test_suite

def run_test_suite(suite: Dict, sort_func: Callable) -> Dict:
    results = {k: 0.0 for k in suite.keys()}

    for k, v in suite.items():
        if len(v) > 100000:
            continue
        start = time.time()
        sort_func(v)
        end = time.time()
        results[k] = end - start

    return results


def run_tests(sort_func: Callable) -> Dict:

    lists_map = {
        "random": create_random_list,
        "random_digits": create_random_digits_list,
        "reversed": create_reversed_list,
        "almost_sorted": create_almost_sorted_list
    }

    results = {}

    for k, v in lists_map.items():
        test_suite = create_test_suite(v)
        results[k] = run_test_suite(test_suite, sort_func)

    return results

def bulk_run() -> Dict:

    results = {}

    for k, v in SORTING_ALGORITHMS.items():
        if not v:
            continue
        results[k] = run_tests(v)
    return results


def render_results_to_ascii_table(res: Dict) -> str:
    lists = ["random", "random_digits", "reversed", "almost_sorted"]
    sizes = ["10^0", "10^1", "10^2", "10^3", "10^4", "10^5", "10^6"]

    result_string = ""

    for l in lists:
        rows_to_draw = []
        header = "\n\n" + l + "\n"
        result_string += header
        header_row = ["sorting_algorithm",]
        algo_rows = []
        for s in sizes:
            header_row.append(s)

        for k, v in res.items():
            algo_row = [k,]
            for v_k, v_v in v[l].items():
                algo_row.append(v_v)

            algo_rows.append(algo_row)

        rows_to_draw = [header_row, *algo_rows]

        table = Texttable()
        table.set_cols_align(("c", "c", "c", "c", "c", "c", "c", "c"))
        table.set_cols_valign(("m", "m", "m", "m", "m", "m", "m", "m"))
        table.set_cols_dtype(("t", "f", "f", "f", "f", "f", "f", "f"))
        table.set_precision(6)
        table.add_rows(rows_to_draw)

        table_string = table.draw()
        result_string = result_string + "\n" + table_string + "\n"

    return result_string


def read_test_file(filename: str) -> List[int]:
#sorting-tests/0.random/test.1.out
    l = []
    with open(filename, "r") as f:
        for i in range(0, 2):
            if i == 0:
                size = int(f.readline())
                if size > 10**7:
                    continue
            if i == 1:
                l = f.readline()
                l = [int(x) for x in l.split(" ")]
    return l


def write_output_file(filename: str, l: List[int]) -> str:
    count = 0
    with open(filename, "w") as f:
        for i in l:
            if count < len(l):
                f.write(f"{i} ")
            else:
                f.write(f"{i}")
            count += 1


def get_all_input_files(directory_name: str) -> List[str]:
    files = []
    for f in os.listdir(directory_name):
        if f.endswith(".in"):
            files.append(f)
    return files


def run_test_files(sorting_algorithm):
    _DIRECTORIES = ["0.random", "1.digits", "2.sorted", "3.revers"]

    for d in _DIRECTORIES:
        d = "sorting-tests/" + d
        files = get_all_input_files(d)
        for f in files:
            print(f"Running test on {sorting_algorithm.__name__} and {d}/{f}...\n")
            l = read_test_file(d + "/" + f)
            output_name = f"{sorting_algorithm.__name__}-{d}-{f}.out".replace("/", "-")
            if len(l) > 0:
                write_output_file(output_name, sorting_algorithm(l))
            else:
                print(f"Won't test file {d}/{f}")

def syntetic_tests():
    results = bulk_run()
    report_string = render_results_to_ascii_table(results)
    meta_data = "Results written at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
    report_string = meta_data + report_string

    with open("results_report.txt", "w") as f:
        f.write(report_string)

if __name__ == "__main__":
    for k, v in SORTING_ALGORITHMS.items():
        run_test_files(v)
