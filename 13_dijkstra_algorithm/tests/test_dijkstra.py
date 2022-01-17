import pytest

from dijkstra_algorithm.dijkstra import dijkstra_algorithm


class TestDijkstraAlgorithm():

    @pytest.fixture
    def test_graph1(self, request):
        vertecies = [
            [1, 6],
            [0, 2, 6, 7],
            [1, 3, 4],
            [2, 4, 5],
            [2, 3, 5, 7, 8],
            [3, 4, 8],
            [0, 1, 7],
            [1, 4, 6, 8],
            [4, 5, 7]
        ]
        edges = [
            [4, 7],
            [4, 9, 11, 20],
            [9, 6, 2],
            [6, 10, 5],
            [2, 10, 15, 1, 5],
            [5, 15, 12],
            [7, 11, 1],
            [20, 1, 1, 3],
            [5, 12, 3]
        ]
        expected_result = [
            0,
            4,
            11,
            17,
            9,
            22,
            7,
            8,
            11
        ]
        return vertecies, edges, expected_result

    @pytest.fixture
    def test_graph2(self, request):
        vertecies = [
            [1, 2],
            [0, 2, 3, 4],
            [0, 1, 5],
            [1, 4],
            [1, 3, 6],
            [2, 6],
            [4, 5]
        ]
        edges = [
            [2, 5],
            [2, 2, 1, 3],
            [5, 6, 2],
            [1, 4],
            [3, 4, 9],
            [2, 7],
            [9, 7]
        ]
        expected_result = [
            0,
            2,
            4,
            3,
            5,
            6,
            13
        ]
        return vertecies, edges, expected_result

    @pytest.mark.parametrize("graph", ["test_graph1", "test_graph2"])
    def test_dijkstra_algoritm(self, graph, request):
        graph = request.getfixturevalue(graph)
        vertecies, edges, expected_result = graph
        result = dijkstra_algorithm(vertecies, edges)
        assert result == expected_result

