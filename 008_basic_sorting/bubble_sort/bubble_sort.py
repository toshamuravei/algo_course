from typing import List


def _sort_iteration(l: List, to_range: int) -> bool:
    swapped = False
    for i in range(1, to_range):
        if l[i-1] > l[i]:
            l[i-1], l[i] = l[i], l[i-1]
            swapped = True
    return swapped


def bubble_sort(list_to_sort: List) -> None:
    n_iterations = len(list_to_sort)
    while n_iterations > 1:
        swapped: bool = _sort_iteration(list_to_sort, n_iterations)
        if not swapped:
            break
        n_iterations -= 1

    return list_to_sort

