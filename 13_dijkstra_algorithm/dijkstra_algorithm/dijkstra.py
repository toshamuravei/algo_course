from queue import PriorityQueue
from typing import List, Tuple

LARGE_INT = 999999

def _get_neighbours_and_weights(vertex, adjacency_list, edges):
    neighbours = adjacency_list[vertex]
    associated_edges = edges[vertex]
    neighbours_edges = list(zip(neighbours, associated_edges))
    neighbours_edges_prioritized = sorted(
        neighbours_edges,
        key = lambda x: x[1],
        reverse = True
    )
    return neighbours_edges_prioritized


def dijkstra_algorithm(
        adjacency_list: List[List[int]],
        edges: List[List[int]]
) -> List[int]:
    START_VERTEX = 0
    visited_vertecies = []
    weighted_paths = [None for x in adjacency_list]
    weighted_paths[START_VERTEX] = 0

    queue_list = [(START_VERTEX, 0)]
    p_queue = PriorityQueue()
    p_queue.put((0, START_VERTEX))

    while not p_queue.empty():
        current_distance, current_vertex = p_queue.get()
        visited_vertecies.append(current_vertex)

        neighbours_and_weights = _get_neighbours_and_weights(
            current_vertex,
            adjacency_list,
            edges
        )
        for neighbour, weight in neighbours_and_weights:
            if neighbour not in visited_vertecies:
                current_cost = weighted_paths[neighbour] or LARGE_INT
                new_cost = weighted_paths[current_vertex] + weight
                if new_cost < current_cost:
                    p_queue.put((new_cost, neighbour))
                    weighted_paths[neighbour] = new_cost

    return weighted_paths

