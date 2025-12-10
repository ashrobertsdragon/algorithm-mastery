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


def dfs(graph: dict[PointIndex, list[PointIndex]]) -> list[PointIndex]:
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


def k_smallest_pairs(points: list[IndexedPoint], k: int):
    distances = [
        (math.dist(node_a, node_b), node_a_index, node_b_index)
        for (node_a_index, node_a), (node_b_index, node_b) in combinations(
            points, 2
        )
    ]
    return heapq.nsmallest(k, distances)


def part_one(lines: list[Point], max_pairs: int) -> int:
    num_points = len(lines)
    indexed = list(enumerate(lines))

    pairs = k_smallest_pairs(indexed, max_pairs)
    graph = build_graph(pairs, num_points)
    circuits = dfs(graph)

    largest = sorted(circuits, reverse=True)[:3]
    return math.prod(largest)


def part_two(lines: list[list[str]], max_circuits: int) -> int: ...


def run_algo(input: str, algo: Callable) -> int:
    lines = read_file(input)
    max_circuits_map = {"sample": 10, "input": 1000}
    max_circuits = max_circuits_map[Path(input).stem.split("_")[1]]

    return algo(lines, max_circuits)
