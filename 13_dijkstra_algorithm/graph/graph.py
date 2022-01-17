from random import randint
from typing import List, Tuple


WITH_NEGATIVE_WEIGHT_RANGE = (-51, 49)
POSITIVE_WEIGHT_RANGE = (1, 100)


def get_adjacency_list(size: int) -> List[List[int]]:
    adjacency_list = [[] for x in range(0, size)]

    for i in range(0, size):
        n_adjacent = randint(0, size - 1)

        adjacent_vertecies = [
            randint(0, size - 1) for x in range(0, n_adjacent)
        ]
        adjacent_vertecies = list(set(adjacent_vertecies))
        adjacent_vertecies = [x for x in adjacent_vertecies if x != i]
        adjacency_list[i] += adjacent_vertecies

        for x in adjacency_list[i]:
            adjacency_list[x].append(i)

    for i in range(0, len(adjacency_list)):
        adjacency_list[i] = list(set(adjacency_list[i]))
        adjacency_list[i] = [x for x in adjacency_list[i] if x != i]
        adjacency_list[i] = sorted(adjacency_list[i])

    return adjacency_list


def get_edges_weights(
        adjacency_list: List,
        allow_negative_weight: bool = False
) -> List[List[int]]:
    edges_weights = [[None for x in i] for i in adjacency_list]

    for i in range(0, len(adjacency_list)):
        for j in range(0, len(adjacency_list[i])):
            adjacent_vertex = adjacency_list[i][j]

            if allow_negative_weight:
                weight = randint(*WITH_NEGATIVE_WEIGHT_RANGE) + 1
            else:
                weight = randint(*POSITIVE_WEIGHT_RANGE)

            if edges_weights[i][j] is None:
                edges_weights[i][j] = weight

            reverse_vertex_idx = adjacency_list[adjacent_vertex].index(i)
            if edges_weights[adjacent_vertex][reverse_vertex_idx] is None:
                edges_weights[adjacent_vertex][reverse_vertex_idx] = weight

    return edges_weights
