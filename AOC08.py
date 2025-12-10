from collections.abc import Callable
import math
import heapq
from itertools import combinations
from pathlib import Path
from typing import TypeAlias


X: TypeAlias = int
Y: TypeAlias = int
Z: TypeAlias = int
PointIndex: TypeAlias = int
Axis: TypeAlias = int
Point: TypeAlias = tuple[X, Y, Z]
IndexedPoint: TypeAlias = tuple[PointIndex, Point]
Distance: TypeAlias = float
Neighbor: TypeAlias = tuple[Distance, PointIndex]


P1_SAMPLE = 40
P1 = 97384
P2_SAMPLE = 25272


def read_file(input: str) -> list[tuple[int, ...]]:
    with open(input, "r") as f:
        lines = f.readlines()
    return [tuple(map(int, line.split(","))) for line in lines]


def dfs(graph: dict[PointIndex, list[PointIndex]]) -> list[int]:
    visited = set()
    sizes: list[int] = []

    for neighbor in graph:
        if neighbor in visited:
            continue
        stack = [neighbor]
        visited.add(neighbor)
        size = 0
        while stack:
            node_a = stack.pop()
            size += 1
            for node in graph[node_a]:
                if node not in visited:
                    visited.add(node)
                    stack.append(node)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def build_graph(
    pairs: list[tuple[Distance, PointIndex, PointIndex]], number_points: int
) -> dict[PointIndex, list[PointIndex]]:
    graph = {i: [] for i in range(number_points)}
    for _, node_a, node_b in pairs:
        graph[node_a].append(node_b)
        graph[node_b].append(node_a)
    return graph


def k_smallest_pairs(points: dict[PointIndex, Point], k: int):
    distances = [
        (math.dist(node_a, node_b), node_a_index, node_b_index)
        for (node_a_index, node_a), (node_b_index, node_b) in combinations(
            points.items(), 2
        )
    ]
    return heapq.nsmallest(k, distances)


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.circuits = size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        y_root, x_root = (
            (x_root, y_root)
            if self.rank[x_root] < self.rank[y_root]
            else (y_root, x_root)
        )

        self.parent[y_root] = x_root
        self.rank[x_root] += 1
        self.circuits -= 1


def part_one(lines: list[Point], max_pairs: int) -> int:
    num_points = len(lines)
    indexed = dict(enumerate(lines))

    pairs = k_smallest_pairs(indexed, max_pairs)
    graph = build_graph(pairs, num_points)

    circuits = dfs(graph)

    largest = sorted(circuits, reverse=True)[:3]
    return math.prod(largest)


def part_two(lines: list[Point], max_circuits: int) -> int:
    num_points = len(lines)
    indexed = dict(enumerate(lines))

    pairs = k_smallest_pairs(indexed, max_circuits)
    uf = UnionFind(num_points)

    for _, node_a, node_b in pairs:
        uf.union(node_a, node_b)
        if uf.circuits > 1:
            continue
        node_a_x = indexed[node_a][0]
        node_b_x = indexed[node_b][0]

        return node_a_x * node_b_x
    raise RuntimeError


def run_algo(input: str, algo: Callable) -> int:
    lines = read_file(input)
    n = len(lines)
    n_squared = n * (n - 1) // 2
    max_circuits_map = {
        part_one: {"sample": 10, "input": 1000},
        part_two: {"sample": n_squared, "input": n_squared},
    }
    max_circuits = max_circuits_map[algo][Path(input).stem.split("_")[1]]

    return algo(lines, max_circuits)
