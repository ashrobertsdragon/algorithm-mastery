import operator
import re
from collections.abc import Callable
from functools import reduce

P1_SAMPLE = 4277556
P1 = 5335495999141
P2_SAMPLE = 3263827


OPERATIONS = {"+": operator.add, "*": operator.mul}


def read_file(file: str) -> tuple[list[str], list[str]]:
    with open(file, "r") as f:
        lines = f.readlines()

    operator_line = lines[-1].split()
    data_lines = lines[:-1]

    return data_lines, operator_line


def convert_data(data_lines: list[str]) -> list[list[int]]:
    return [
        [int(part) for part in line.split() if part != "\n"]
        for line in data_lines
    ]


def part_one(operators: list[str], lines: list[str]) -> int:
    rows = convert_data(lines)
    columns = list(map(list, zip(*rows)))

    return sum(
        (
            reduce(OPERATIONS[operation], column)
            for operation, column in zip(operators, columns)
        )
    )


def part_two(operators: list[str], rows: list[str]) -> int:
    tokens = [[m.span() for m in re.finditer(r"\S+", row)] for row in rows]
    number_columns = max(len(spans) for spans in tokens)

    columns = []

    for column_id in range(number_columns):
        parts = []
        starts = []
        max_width = 0
        for row, spans in zip(rows, tokens):
            if column_id < len(spans):
                start, end = spans[column_id]
                token = row[start:end]
                parts.append(token)
                starts.append(start)
            else:
                parts.append("")
                starts.append(None)
            max_width = max(max_width, len(parts[-1]))

        numeric_starts = [start for start in starts if start is not None]
        justify_right = len(set(numeric_starts)) > 1

        padded = (
            [p.rjust(max_width) for p in parts]
            if justify_right
            else [p.ljust(max_width) for p in parts]
        )

        transposed = list(zip(*padded))

        numbers = []
        for column in transposed:
            digits = "".join(
                character for character in column if character.isdigit()
            )
            numbers.append(int(digits) if digits else 0)

        numbers = numbers[::-1]

        columns.append(numbers)
    ops = {"+": operator.add, "*": operator.mul}
    return sum((reduce(ops[op], col) for op, col in zip(operators, columns)))


def run_algo(input: str, algo: Callable) -> int:
    figures, operators = read_file(input)
    return algo(operators, figures)
