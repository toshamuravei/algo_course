from typing import Callable, List


def _shell_sort(l: List[int], gaps_generator: Callable) -> List[int]:
    gaps = [g for g in gaps_generator(len(l))]
    for g in gaps:
        for i in range(g, len(l), 1):
            j = i
            delta = j - g
            while delta >= 0 and l[delta] > l[j]:
                l[delta], l[j] = l[j], l[delta]
                j = delta
                delta = j - g
    return l


def ciura_generator(length: int) -> int:
    gaps = [1750, 701, 301, 132, 57, 23, 10, 4, 1]
    for g in gaps:
        yield g


def sedgewick_82_generator(length: int) -> int:
    i = 1
    g = 1
    gaps = [1,]
    while g < length:
        g = (4 ** i) + (3 * (2 ** (i - 1))) + 1
        i += 1
        gaps.append(g)

    gaps.reverse()
    for g in gaps:
        yield g


def knuth_generator(length: int) -> int:
    i = 0
    g = 1
    gaps = []
    while g < length // 3:
        g = ((3 ** i) - 1) // 2
        i += 1
        gaps.append(g)

    gaps.reverse()
    for g in gaps:
        yield g


def shell_generator(length: int) -> int:
    g = length // 2
    while g > 0:
        yield g
        g //= 2


def shell_sort(l: List[int]) -> List[int]:
    l = _shell_sort(l, shell_generator)
    return l


def shell_sort_ciura_gap(l: List[int]) -> List[int]:
    l = _shell_sort(l, ciura_generator)
    return l


def shell_sort_knuth_gap(l: List[int]) -> List[int]:
    l = _shell_sort(l, knuth_generator)
    return l


def shell_sort_sedgewick_82_gap(l: List[int]) -> List[int]:
    l = _shell_sort(l, sedgewick_82_generator)
    return l

