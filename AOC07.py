from collections.abc import Callable


P1_SAMPLE = 21
P1 = 1687
P2_SAMPLE = 40


def read_file(input: str) -> list[list[str]]:
    with open(input, "r") as f:
        lines: list[str] = f.readlines()

    return [list(line.strip()) for line in lines]


def part_one(lines: list[list[str]]) -> int:
    start = lines[0].index("S")
    beams = {start}
    total = 0
    for line in lines[1:]:
        new = set()

        for index in beams:
            move = 1 if line[index] == "^" else 0
            new.add(index - move)
            new.add(index + move)
            total += move

        beams = new

    return total


def part_two(lines: list[list[str]]) -> int:
    width = len(lines[0])
    dp = [0] * width
    dp[lines[0].index("S")] = 1

    for line in lines[1:]:
        next_dp = [0] * width
        for index, count in enumerate(dp):
            if count == 0:
                continue
            if line[index] == "^":
                next_dp[index - 1] += count
                next_dp[index + 1] += count
            else:
                next_dp[index] += count
        dp = next_dp

    return sum(dp)


def run_algo(input: str, algo: Callable) -> int:
    lines = read_file(input)
    return algo(lines)
