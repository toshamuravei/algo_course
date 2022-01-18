import pytest

from primitive_queue.queue import PrimitivePriorityQueue


@pytest.fixture
def values_to_put_and_to_get():
    return {
        "to_put": [(5, 4), (5, 6), (5, 1), (1, 2), (1, 1), (3, 12), (2, 8)],
        "to_get": [2, 1, 8, 12, 4, 6, 1]
    }


def test_primitive_priority_queue(values_to_put_and_to_get):
    values_to_put = values_to_put_and_to_get["to_put"]
    expected_to_get = values_to_put_and_to_get["to_get"]

    queue = PrimitivePriorityQueue()
    for priority, value in values_to_put:
        queue.enqueue(priority, value)

    real_result = []
    while not queue.empty():
        real_result.append(queue.dequeue())

    assert expected_to_get == real_result

