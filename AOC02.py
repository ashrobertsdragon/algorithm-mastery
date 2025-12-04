from collections.abc import Callable, Generator
from dataclasses import dataclass


P1_SAMPLE = answer = 1227775554
P1 = 32976912643
P2_SAMPLE = 4174379265


@dataclass(slots=True)
class NumberRange:
    lower_num: str
    upper_num: str


def parse_ranges(file: str) -> list[NumberRange]:
    ranges = []
    with open(file) as f:
        ranges = [NumberRange(*line.split("-")) for line in f.read().split(",")]
    return ranges


def is_even_length(number: str) -> bool:
    return not len(number) % 2


def normalize_length(number: str, upper_bound: bool = False) -> str:
    length = len(number)
    if is_even_length(number):
        return number
    return number[0] + "0" * (length - 1) if upper_bound else "1" + "0" * length


def get_left_side(number: str) -> int:
    middle = len(number) // 2
    normalized_middle = middle if is_even_length(number) else middle + 1
    return int(number[:normalized_middle])


def part_one(ranges: list[NumberRange]) -> int:
    invalid = 0
    for number_range in ranges:
        lower_num = normalize_length(number_range.lower_num)
        upper_num = normalize_length(number_range.upper_num, upper_bound=True)
        bottom = get_left_side(lower_num)
        top = get_left_side(upper_num)
        for number in range(bottom, top + 1):
            potential = int(str(number) * 2)
            if (
                int(number_range.lower_num)
                <= potential
                <= int(number_range.upper_num)
            ):
                invalid += potential
    return invalid


def periodic_numbers_generator(length: int) -> Generator[int, None, None]:
    seen = set()
    for repeat in range(2, length + 1):
        if length % repeat:
            continue
        chunk = length // repeat
        start = 10 ** (chunk - 1)
        end = 10**chunk
        for chunk in range(start, end):
            num = str(chunk) * repeat
            if num in seen:
                continue
            seen.add(num)
            yield int(num)


def part_two(ranges: list[NumberRange]) -> int:
    invalid = 0
    for number_range in ranges:
        low_length = len(number_range.lower_num)
        high_length = len(number_range.upper_num)
        for length in range(low_length, high_length + 1):
            for number in periodic_numbers_generator(length):
                if (
                    int(number_range.lower_num)
                    <= number
                    <= int(number_range.upper_num)
                ):
                    invalid += number
    return invalid


def run_algo(file: str, algo: Callable) -> int:
    """Run the algorithm on the values in the file."""
    ranges = parse_ranges(file)
    answer = algo(ranges)
    print(answer)
    return answer
