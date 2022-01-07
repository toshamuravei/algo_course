import pudb
from typing import List


def _swap(source_list: List, idx_a: int, idx_b: int) -> None:
    temp = source_list[idx_a]
    source_list[idx_a] = source_list[idx_b]
    source_list[idx_b] = temp


def bs(l: List, f: int, t: int, val: int) -> int:
    """
    Preposition:
    l - sorted list
    f - 'from', lower border of search
    t - 'to', upper border of search
    f < t - at first (non recursive) call
    val - integer, which place (index) would be found in l

    Postposition:
    l wouldn't be changed, at the end function returns int (index)
    of val, where it should be placed at l
    """
    if len(l) == 0:
        return 0

    if len(l) == 1:
        return 0 if l[0] > val else 1

    # edge case: we either at the end of list or at 0 index
    if f > t:
        if val > l[-1]:
            return len(l)
        if val < l[0]:
            return 0

    g = (f + t) // 2

    if l[g] == val:
        return g + 1

    if l[g] > val > l[g-1]:
        return g
    elif l[g] > val:
        # shift left
        return bs(l, f, g-1, val)
    elif l[g] < val:
        # shift right
        return bs(l, g+1, t, val)


def insertion_sort(list_to_sort: List) -> List[int]:
    for i in range(1, len(list_to_sort)):
        j = i
        while j > 0 and list_to_sort[j - 1] > list_to_sort[j]:
            _swap(list_to_sort, j - 1, j)
            j -= 1
    return list_to_sort


def insertion_sort_optimized(l: List) -> List[int]:
    for i in range(1, len(l)):
        if l[i] < l[i - 1]:
            p = bs(l[0:i], 0, i-1, l[i])
            if p != i:
                e = l[i]
                del l[i]
                l.insert(p, e)
    return l
