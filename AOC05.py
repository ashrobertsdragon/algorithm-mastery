from collections.abc import Callable
from typing import TypeAlias


NumberRange: TypeAlias = tuple[int, ...]

P1_SAMPLE = 3
P1 = 712
P2_SAMPLE = 14


def read_file(file: str) -> tuple[list[NumberRange], list[int]]:
    with open(file, "r") as f:
        parts = f.read().split("\n\n")
        ranges = [
            tuple(map(int, part.split("-"))) for part in parts[0].split("\n")
        ]
        values = [int(part) for part in parts[1].split("\n")]
        ranges.sort(key=lambda r: (r[0], r[1]))
        values.sort()
        return ranges, values


def part_one(ranges: list[NumberRange], values: list[int]) -> int:
    valid = 0
    for value in values:
        for lo, hi in ranges:
            if lo <= value <= hi:
                valid += 1
                break
    return valid


def part_two(ranges, values) -> int:
    merged = []
    for r in ranges:
        if not merged:
            merged.append(r)
            continue
        last_start, last_end = merged[-1]
        start, end = r
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append(r)
    total = sum(end - start + 1 for start, end in merged)
    return total


def run_algo(input: str, algo: Callable) -> int:
    ranges, values = read_file(input)
    return algo(ranges, values)
