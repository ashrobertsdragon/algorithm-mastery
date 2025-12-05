from collections import deque
from collections.abc import Callable, Generator
from functools import cache
from typing import TypeAlias


P1_SAMPLE = 13
P1 = 1505
P2_SAMPLE = 43

Grid: TypeAlias = list[list[str]]
GridTuple: TypeAlias = tuple[tuple[str, ...], ...]
Point: TypeAlias = tuple[int, int]
Neighbors: TypeAlias = dict[Point, str]
Nodes: TypeAlias = dict[Point, dict[str, bool | int]]


DIRECTIONS: set[Point] = {
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, 1),
    (1, 1),
    (1, -1),
    (-1, -1),
}


def read_input(
    file: str,
) -> tuple[Grid, GridTuple]:
    with open(file, "r") as f:
        lines = f.readlines()
    grid = [[char for char in line.strip()] for line in lines]
    as_tuple = tuple(map(tuple, grid))
    return grid, as_tuple


@cache
def get_dimensions(grid: GridTuple) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def is_valid_point(x: int, y: int, grid_tuple: GridTuple) -> bool:
    height, width = get_dimensions(grid_tuple)
    return 0 <= x < width and 0 <= y < height


def check_neighbors(
    x: int, y: int, grid: Grid, grid_tuple: GridTuple, too_many: int
) -> bool:
    rolls = 0
    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy
        if is_valid_point(new_x, new_y, grid_tuple) and grid[new_y][new_x] in [
            "@",
            "x",
        ]:
            rolls += 1
    return rolls < too_many


def part_one(grid: Grid, as_tuple: GridTuple) -> int:
    height, width = get_dimensions(as_tuple)
    too_many = 4
    atttainable = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "@" and check_neighbors(
                x, y, grid, as_tuple, too_many
            ):
                grid[y][x] = "x"
                atttainable += 1

    return atttainable


def part_two_naive(grid: Grid, as_tuple: GridTuple) -> int:
    height, width = get_dimensions(as_tuple)
    too_many = 4
    removed = 0
    while True:
        old_removed = removed
        for y in range(height):
            for x in range(width):
                if grid[y][x] == "@" and check_neighbors(
                    x, y, grid, as_tuple, too_many
                ):
                    grid[y][x] = "."
                    removed += 1

        if old_removed == removed:
            return removed


def count_neighbors(x: int, y: int, grid: Grid, grid_tuple: GridTuple) -> int:
    height, width = get_dimensions(grid_tuple)
    count = 0
    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy
        if (
            0 <= new_x < width
            and 0 <= new_y < height
            and grid[new_y][new_x] == "@"
        ):
            count += 1
    return count


def walk_edges(
    x: int,
    y: int,
    degree: list,
    removed: list,
    grid_tuple: GridTuple,
    just_right: int,
) -> Generator[Point, None, None]:
    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy
        if (
            not is_valid_point(new_x, new_y, grid_tuple)
            or not degree[new_y][new_x]
            or removed[new_y][new_x]
        ):
            continue
        degree[new_y][new_x] -= 1
        if degree[new_y][new_x] == just_right:
            yield (new_x, new_y)


def part_two_clean(grid: Grid, as_tuple: GridTuple) -> int:
    too_many = 4
    height, width = get_dimensions(as_tuple)
    degree = [[0] * width for _ in range(height)]
    removed = [[False] * width for _ in range(height)]
    queue: deque[Point] = deque()

    for y in range(height):
        for x in range(width):
            if grid[y][x] == ".":
                continue
            count = count_neighbors(x, y, grid, as_tuple)
            degree[y][x] = count
            removed[y][x] = False
            if count < too_many:
                queue.append((x, y))

    total = 0
    while queue:
        x, y = queue.popleft()
        if removed[y][x]:
            continue
        removed[y][x] = True
        total += 1
        for edge in walk_edges(x, y, degree, removed, as_tuple, too_many - 1):
            queue.append(edge)

    return total


def part_two(grid: Grid, as_tuple: GridTuple) -> int:
    too_many = 4
    height, width = len(grid[0]), len(grid)
    degree = [[0] * width for _ in range(height)]
    removed = [[False] * width for _ in range(height)]
    queue: deque[Point] = deque()

    for y in range(height):
        for x in range(width):
            if grid[y][x] == ".":
                continue
            count = 0
            for dx, dy in DIRECTIONS:
                new_x = x + dx
                new_y = y + dy
                if (
                    0 <= new_x < width
                    and 0 <= new_y < height
                    and grid[new_y][new_x] == "@"
                ):
                    count += 1
            degree[y][x] = count
            if count < too_many:
                queue.append((x, y))

    total = 0
    while queue:
        x, y = queue.popleft()
        if removed[y][x]:
            continue
        removed[y][x] = True
        total += 1
        for dx, dy in DIRECTIONS:
            new_x = x + dx
            new_y = y + dy
            if (
                0 <= new_x < width
                and 0 <= new_y < height
                and not removed[new_y][new_x]
            ):
                degree[new_y][new_x] -= 1

                if degree[new_y][new_x] == too_many - 1:
                    queue.append((new_x, new_y))

    return total


def run_algo(input: str, algo: Callable) -> int:
    grid, as_tuple = read_input(input)
    return algo(grid, as_tuple)
