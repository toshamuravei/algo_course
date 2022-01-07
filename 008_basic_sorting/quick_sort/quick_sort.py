from typing import List, Optional


def _split(l: List[int], _from: int, _to: int) -> int:
    pivot_idx = _from
    pivot = l[pivot_idx]

    while _from < _to:

        while _from < len(l) and l[_from] <= pivot:
            _from += 1

        while l[_to] > pivot:
            _to -= 1

        if _from < _to:
            l[_from], l[_to] = l[_to], l[_from]

    l[_to], l[pivot_idx] = l[pivot_idx], l[_to]
    return _to


def _split_improved(l: List[int], _L, _R):
    a = _L - 1
    p = l[_R]

    for i in range(_L, _R+1):
        if l[i] <= p:
            a += 1
            l[a], l[i] = l[i], l[a]

    return a


def quick_sort_improved(l, _from=None, _to=None):
    if _from is None or _to is None:
        _from, _to = 0, len(l) - 1

    if _from < _to:
        p = _split_improved(l, _from, _to)
        quick_sort(l, _from, p - 1)
        quick_sort(l, p + 1, _to)

    return l

def quick_sort(l: List[int], _from: Optional[int]=None, _to: Optional[int]=None) -> List[int]:
    # initial, non-recursive call
    if _from is None or _to is None:
        _from, _to = 0, len(l) - 1

    if _from < _to:
        p_idx: int = _split(l, _from, _to)

        quick_sort(l, _from, p_idx - 1)
        quick_sort(l, p_idx + 1, _to)

    return l

