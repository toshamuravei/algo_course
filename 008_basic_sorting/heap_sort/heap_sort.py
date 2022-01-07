from typing import List


def _heapify(l: List[int], length: int, i: int) -> List[int]:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < length and l[largest] < l[left]:
        largest = left

    if right < length and l[largest] < l[right]:
        largest = right

    if largest != i:
        l[i], l[largest] = l[largest], l[i]

        _heapify(l, length, largest)


def heap_sort(l: List[int]) -> List[int]:

    for i in range((len(l) // 2) - 1, -1, -1):
        _heapify(l, len(l), i)

    for i in range(len(l) - 1, 0, -1):
        l[i], l[0] = l[0], l[i]
        _heapify(l, i, 0)

    return l

