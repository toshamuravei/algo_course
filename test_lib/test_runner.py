import os
from datetime import datetime
from typing import Callable, Dict, Iterable, List, Optional

from texttable import Texttable

from .test_case import TestCase


TEST_CASE_INDEX_CHAR_POS = 5
TEST_CASE_IDX_SHIFT = 2
TEST_CASE_MIN_FILENAME_LENGTH = 5
TEST_DATA_DIR_NAME = 'test_data/'
RUN_UNTIL_BIG_INT = 9999


class RunnerError(Exception):
    pass

class NoTestResultsError(RunnerError):
    pass


class TestRunner:

    def __init__(self, dir_name=TEST_DATA_DIR_NAME, test_case_cls=TestCase, run_until=None):
        self.data_dir = dir_name
        if run_until:
            self.run_until = self.get_test_case_index(run_until)
        else:
            self.run_until = RUN_UNTIL_BIG_INT
        self.test_case_class = test_case_cls
        self.test_case_collection = self.build_test_case_collection()
        self.full_run_results = None

    def get_test_case_index(self, test_case_filename):
        assert isinstance(test_case_filename, str) == True
        assert len(test_case_filename) > TEST_CASE_MIN_FILENAME_LENGTH

        idx_pos = TEST_CASE_INDEX_CHAR_POS

        if test_case_filename[idx_pos + 1].isnumeric():
            return int(test_case_filename[idx_pos:idx_pos+TEST_CASE_IDX_SHIFT])
        else:
            return int(test_case_filename[idx_pos])

    def build_test_case_collection(self):
        test_collection = []

        tmp_collection = self.gather_tmp_test_data()

        for test_name in sorted(tmp_collection.keys()):
            test_case = self.test_case_class(
                test_name,
                self.data_dir + "/" + tmp_collection[test_name]["in"],
                self.data_dir + "/" + tmp_collection[test_name]["out"]
            )
            test_collection.append(test_case)

        return test_collection

    def gather_tmp_test_data(self) -> dict:
        is_test_file = lambda x: x if (x.endswith(".in") or x.endswith(".out")) else False
        is_small_enough = lambda x: self.get_test_case_index(x) <= self.run_until
        test_names = filter(lambda x: is_test_file(x), os.listdir(self.data_dir))
        test_names = filter(lambda x: is_small_enough(x), test_names)
        test_names = list(set(map(lambda x: x[:-3] if x.endswith(".in") else x[:-4], test_names)))
        tmp_collection = {test_name: {} for test_name in test_names}

        for filename in os.listdir(self.data_dir):
            # skip too heavy tests
            if is_test_file(filename) and self.run_until:
                test_case_index = self.get_test_case_index(filename)
                if test_case_index > self.run_until:
                    continue

            if filename.endswith(".in"):
                test_name = filename[:-3]
                tmp_collection[test_name]["in"] = filename
            elif filename.endswith(".out"):
                test_name = filename[:-4]
                tmp_collection[test_name]["out"] = filename

        return tmp_collection

    def run_tests(
            self,
            func_to_test: Callable,
            func_args: Optional[Iterable]=None,
            func_kwargs: Optional[Dict]=None
    ) -> Dict:

        func_args = func_args or ()
        func_kwargs = func_kwargs or {}
        test_results = []

        for test_case in self.test_case_collection:
            test_result = test_case.run(func_to_test, func_args, func_kwargs)
            test_results.append(self.format_result(test_result))

        self.full_run_results = test_results
        return test_results

    def run_competitive(
            self,
            callable_list: List[Callable],
            func_args: Optional[Iterable]=None,
            func_kwargs: Optional[Dict]=None
    ) -> Dict:

        competetive_results = {}
        for func in callable_list:
            competetive_results[func.__name__] = self.run_tests(func, func_args, func_kwargs)

        self.full_run_results = competetive_results
        return competetive_results

    def format_result(self, result: Dict) -> Dict:
        result_dict = {
            "result_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "result": result
        }
        return result_dict

    # TODO: move to separate class
    def render_results_as_raw_text(self) -> str:
        self.check_for_empty_results()

        all_results_string = ""
        for result in self.full_run_results:
            all_results_string = all_results_string + self.render_single_as_raw_text(result) + "\n\n"
        return all_results_string

    # TODO: move to separate class
    def _render_single_as_raw_text(self, result):
        test_res = result.get("result")

        test_name = "Test name: " + test_res["test_name"] + "\n"
        test_status = "Test passed: " + str(test_res["is_passed"]) + "\n"
        exec_time = "Executed in: " + test_res["execution_time"] + " seconds" + "\n"
        rude_memory_usage = "Memory used on execution: " + test_res["rude_mem_usage"] + "\n"

        return test_name + test_status + exec_time + rude_memory_usage

    # TODO: move to separate class
    def render_as_ascii_table(self) -> str:
        self.check_for_empty_results()

        table = Texttable()
        table.set_cols_align(("c", "c", "c", "c", "c"))
        table.set_cols_valign(("m", "m", "m", "m", "m"))
        table.set_cols_dtype(["t", "t", "f", "f", "t"])
        table.set_precision(6)

        rows_to_add = [["Test Name", "Status", "Executed in (sec)", "Memory used (Mb)", "Details"],]
        for res in self.full_run_results:
            test_res = res.get("result")
            res_list = [
                test_res["test_name"],
                test_res["is_passed"],
                test_res["execution_time"],
                test_res["rude_mem_usage"],
                test_res["details"]
            ]
            rows_to_add.append(res_list)

        table.add_rows(rows_to_add)

        return table.draw()

    def render_ascii_competitive_results(self) -> str:
        self.check_for_empty_results()

        table = Texttable()
        table.set_cols_align(("c", "c", "c", "c", "c"))
        table.set_cols_valign(("m", "m", "m", "m", "m"))
        table.set_cols_dtype(["t", "t", "f", "f", "t"])
        table.set_precision(6)

        rows_to_add = []
        for k, v in self.full_run_results.items():
            test_func_header = [" ", " ", k, " ", " "]
            test_results_header = ["Test Name", "Status", "Executed in (sec)", "Memory used (Mb)", "Details"]
            rows_to_add.append(test_func_header)
            rows_to_add.append(test_results_header)

            for res in v:
                test_res = res.get("result")
                res_list = [
                    test_res["test_name"],
                    test_res["is_passed"],
                    test_res["execution_time"],
                    test_res["rude_mem_usage"],
                    test_res["details"]
                ]
                rows_to_add.append(res_list)

        table.add_rows(rows_to_add)

        return table.draw()

    def check_for_empty_results(self) -> None:
        if not self.full_run_results or len(self.full_run_results) == 0:
            raise NoTestResultsError("Can't render results, cause there is no results. Run tests first")

    def write_to_file(self, string_to_write: str, filepath: str):
        meta_data = "Results written at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
        string_to_write = meta_data + string_to_write

        with open(filepath, "w") as result_file:
            result_file.write(string_to_write)

