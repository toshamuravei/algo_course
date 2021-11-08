import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from test_lib.test_runner import TestRunner


def measure_string_length(string_to_measure) -> int:
    return str(len(string_to_measure))

if __name__ == "__main__":
    test_data_dir = os.getcwd() + "/test_data"
    runner = TestRunner(dir_name=test_data_dir)
    runner.run_tests(measure_string_length)

    ascii_table_result = runner.render_as_ascii_table()
    result_file = os.getcwd() + "/result.txt"
    runner.write_to_file(ascii_table_result, result_file)
    print(ascii_table_result)

