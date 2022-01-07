from typing import List


def selection_sort(l: List[int]) -> List[int]:
    for i in range(0, len(l)):
        m_idx = i

        for j in range(i + 1, len(l)):
            if l[m_idx] > l[j]:
                m_idx = j

        l[m_idx], l[i] = l[i], l[m_idx]

    return l

