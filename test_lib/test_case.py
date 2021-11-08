import os
import time
from typing import Callable, Dict, Iterable

from memory_profiler import memory_usage


class ReadFileError(Exception):
    pass


class TestCase:
    """
    Simple test case class that gather some plain text out & in data.
    'Testing' is implemented as given Callable run with self.in_data as
    first arg, and comparing result with self.out_data.
    In process of execution class measures time (as delta between time
    before & after) and memory consumption.

    (ATTENTION!) Memory consumption measuring should be done in a relative
    way. For now it is done as PROCESS memory consumption, which is
    obviously not as clear as memory measurment of a single function run.
    """

    def __init__(self, name: str, in_file: str, out_file: str):
        self.name = name
        self.in_data = self.read_file_plain(in_file)
        self.out_data = self.read_file_plain(out_file)

    def read_file_plain(self, filename: str) -> str:
        f = open(filename, "r")
        lines = f.readlines()
        if lines:
            return lines[0].strip()
        else:
            raise ReadFileError(f"File named {filename} is empty!")

    def _run_test(self, testing_func: Callable, args: Iterable, kwargs: Dict) -> Dict:
        args = (self.in_data, *args)
        real_result = testing_func(*args, **kwargs)
        test_status = str(real_result) == self.out_data
        test_result = {
            "test_name": self.name,
            "is_passed": "PASSED" if test_status else "FAILED",
            "details": self._get_test_run_details(real_result, test_status)
        }
        return test_result

    # TODO: move those strings into class constants or something
    def _get_test_run_details(self, test_result: str, test_status: bool) -> str:
        test_passed_details = "-"
        test_failed_details = f"Expected result: {self.out_data}\n Real result: {test_result}"
        return test_passed_details if test_status else test_failed_details

    # TODO: separate memory measurement and make it relative
    def _gather_metrics(self, testing_func: Callable, args: Iterable, kwargs: Dict) -> Dict:
        # run test & measure execution time
        start = time.time()
        result = self._run_test(testing_func, args, kwargs)
        end = time.time()
        _metric_execution_time = ("{:.6f}".format(end - start))
        result["execution_time"] = _metric_execution_time

        # run test & measure memory used
        inaccurate_mem_usage = memory_usage((testing_func, (self.in_data, *args), kwargs))
        inaccurate_mem_usage = sum(inaccurate_mem_usage)/len(inaccurate_mem_usage)
        _metric_rude_mem_usage = ("{:.6f}".format(inaccurate_mem_usage))
        result["rude_mem_usage"] = _metric_rude_mem_usage

        return result

    def run(self, testing_func: Callable, func_args: Iterable, func_kwargs: Dict) -> Dict:
        return self._gather_metrics(testing_func, func_args, func_kwargs)

