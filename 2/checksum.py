"""Day 2 table checksum."""

import re
from typing import Callable, List
from pathlib import Path

IntTableRow = List[int]
IntTable = List[IntTableRow]


with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def _parse_table(table_string: str) -> IntTable:
    return [list(map(int, re.split(r'\s+', line.strip())))
            for line in table_string.splitlines() if line.strip()]


def checksum(table_string: str,
             line_hash: Callable[[IntTableRow], int]=None) -> int:
    return sum(line_hash(line) for line in _parse_table(table_string))


def max_min_diff(line: IntTableRow) -> int:
    return max(line) - min(line)


def evenly_divisible_result(line: IntTableRow) -> int:
    sorted_values = sorted(line)
    while True:
        a = sorted_values.pop()
        for b in sorted_values:
            if a % b == 0:
                return a // b


def test_checksum_max_min_diff():
    assert checksum(
        '5 1 9 5\n'
        '7 5 3\n'
        '2 4 6 8\n', max_min_diff) == 18


def test_checksum_evenly_divisible_result():
    assert checksum(
        '5 9 2 8\n'
        '9 4 7 3\n'
        '3 8 6 5\n', evenly_divisible_result) == 9


if __name__ == '__main__':
    print(f'checksum 1: {checksum(puzzle_input, max_min_diff)}')
    print(f'checksum 2: {checksum(puzzle_input, evenly_divisible_result)}')
