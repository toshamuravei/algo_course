from typing import List


def _count_sort(l: List[int], radix:int) -> List[int]:
    n = len(l)

    res = [0] * n

    count = [0] * 10

    for i in range(0, n):
        index = l[i] // radix
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = l[i] // radix
        res[count[index % 10] - 1] = l[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(0, n):
        l[i] = res[i]

    return l


    return [1, 2, 3]

def radix_sort(l: List[int]) -> List[int]:
    max_i = max(l)

    radix = 1
    while max_i / radix > 0:
        l = _count_sort(l, radix)
        radix *= 10
    return l

