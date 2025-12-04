from collections.abc import Callable, Generator


P1_SAMPLE = 357
P1 = 17445
P2_SAMPLE = 3121910778619


def read_input(file: str) -> Generator[list[int], None, None]:
    with open(file, "r") as f:
        for line in f:
            yield [int(i) for i in line.strip()]


def part_one(lines: Generator[list[int], None, None]) -> int:
    total = 0
    for line in lines:
        best = 0
        num = 0
        for digit in line:
            if best:
                num = max(num, best * 10 + digit)
            best = max(best, digit)

        total += num
    return total


def get_k_largest(digits: list[int], k: int) -> int:
    remove = len(digits) - k
    stack: list[int] = []

    for digit in digits:
        while stack and remove > 0 and stack[-1] < digit:
            stack.pop()
            remove -= 1
        stack.append(digit)

    if remove:
        stack = stack[:-remove]

    return int("".join(map(str, stack[:k])))


def part_two(lines: Generator[list[int], None, None]) -> int:
    total = 0
    for line in lines:
        total += get_k_largest(line, 12)
    return total


def run_algo(input: str, algo: Callable) -> int:
    return algo(read_input(input))
