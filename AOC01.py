import math
from collections.abc import Callable, Generator
from itertools import accumulate

P1_SAMPLE = 3
P1 = 969
P2_SAMPLE = 6

DIRECTION: dict[str, int] = {"L": -1, "R": +1}


def iterate_combos(file: str) -> Generator[str, None, None]:
    with open(file) as f:
        for line in f:
            yield line.strip()


def rotate(current: int, move: str) -> int:
    direction = move[0]
    value = int(move[1:])
    return (current + DIRECTION[direction] * value) % 100


def part_one(start: int, combos: Generator[str, None, None]) -> int:
    z = 0
    for val in accumulate(combos, rotate, initial=start):
        if val == 0:
            z += 1
    return z


def part_two(current: int, combos: Generator[str, None, None]) -> int:
    z = 0
    for move in combos:
        direction = move[0]
        value = int(move[1:])

        delta = DIRECTION[direction] * value
        new = current + delta

        shift = max(DIRECTION[direction], 0)
        z += abs(
            math.floor((new - shift) / 100)
            - math.floor((current - shift) / 100)
        )

        current = new
    return z


def run_algo(input: str, algo: Callable) -> int:
    start = 50
    combos = iterate_combos(input)
    return algo(start, combos)
