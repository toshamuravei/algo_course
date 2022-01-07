from typing import List


def _ordering_merge_lists(left_l: List[int], right_l: List[int]) -> List[int]:
    merged_l = [None] * (len(left_l) + len(right_l))
    common_idx = 0
    left_idx = 0
    right_idx = 0

    while left_idx < len(left_l) and right_idx < len(right_l):
        if left_l[left_idx] <= right_l[right_idx]:
            merged_l[common_idx] = left_l[left_idx]
            left_idx += 1
        else:
            merged_l[common_idx] = right_l[right_idx]
            right_idx += 1
        common_idx += 1

    if left_idx < len(left_l):
        merged_l += left_l

    if right_idx < len(right_l):
        merged_l += right_l

    return merged_l


def merge_sort(l: List[int]) -> List[int]:
    if len(l) <= 1:
        return l

    div_idx = len(l) // 2
    left_l, right_l = l[:div_idx], l[div_idx:]

    left_l = merge_sort(left_l)
    right_l = merge_sort(right_l)

    merged_l = _ordering_merge_lists(left_l, right_l)

    for i in range(0, len(l)):
        l[i] = merged_l[i]

    return l

def external_merge_sort(l:List[int]) -> List[int]:
    """
    Сгенерировать бинарный файл, который содержит N целых, 16-битных чисел (от 0 до 65535),
    по 2 байта на каждое число. Реализовать алгоритм внешеней сортировки MergeSort и применить
    его для сортировки созданного файла.
    """
    return [1, 2, 3]
