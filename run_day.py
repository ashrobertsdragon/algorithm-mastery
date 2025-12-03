import sys
from importlib import import_module


def p1_sample() -> bool:
    file = f"{BASE}_sample.txt"
    algo = MODULE.part_one
    output = MODULE.run_algo(file, algo)
    print(output)
    return output == MODULE.P1_SAMPLE


def p2_sample() -> bool:
    file = f"{BASE}_sample.txt"
    algo = MODULE.part_two
    output = MODULE.run_algo(file, algo)
    print(output)
    return output == MODULE.P2_SAMPLE


def run_part_two() -> None:
    if p2_sample():
        print("Part 2 sample passed")
        part_2_answer = MODULE.run_algo(f"{BASE}_input.txt", MODULE.part_two)
        print(f"Part 2 answer: {part_2_answer}")
        return
    print("Part 2 sample failed")


def run_part_one() -> None:
    if p1_sample():
        print("Part 1 sample passed")
        part_1_answer = MODULE.run_algo(f"{BASE}_input.txt", MODULE.part_one)
        print(f"Part 1 answer: {part_1_answer}")
        if part_1_answer == MODULE.P1:
            run_part_two()
        return
    print("Part 1 sample failed")


def load_globals(day: str):
    global MODULE
    global BASE
    BASE = f"AOC{day}"
    MODULE = import_module(BASE)


def main():
    day = sys.argv[1]
    load_globals(day)
    run_part_one()


if __name__ == "__main__":
    main()
