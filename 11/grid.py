"""Day 11: Hex Ed."""

from pathlib import Path
from typing import List, Iterator, Tuple
from functools import reduce

with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


class HexPosition:
    x: int = 0
    y: int = 0
    z: int = 0

    def __repr__(self) -> str:
        return f'(S-N:{self.x} SW-NE:{self.y} NW/SE:{self.z})'


DIRECTION_MAP = {
    'n': (0, 1, -1),
    's': (0, -1, 1),
    'ne': (1, 0, -1),
    'sw': (-1, 0, 1),
    'se': (1, -1, 0),
    'nw': (-1, 1, 0),
}


def parse_directions(text: str) -> Iterator[str]:
    return (d.strip() for d in text.split(','))


def distance_from_center(pos: HexPosition) -> int:
    return (abs(-pos.x) + abs(-pos.y) + abs(-pos.z)) // 2


def direction_reducer(pos: HexPosition, direction: str) -> HexPosition:
    delta = DIRECTION_MAP[direction]
    pos.x += delta[0]
    pos.y += delta[1]
    pos.z += delta[2]
    return pos


def apply_directions(directions: Iterator[str]) -> Tuple[HexPosition, int]:
    pos = HexPosition()
    max_distance = 0
    for step in directions:
        pos = direction_reducer(pos, step)
        max_distance = max(max_distance, distance_from_center(pos))
    return pos, max_distance


def parse_and_apply(text: str) -> Tuple[HexPosition, int]:
    directions = parse_directions(text)
    return apply_directions(directions)


if __name__ == '__main__':
    pos, max_distance = parse_and_apply(puzzle_input)
    print(f'{pos}, current distance from center: {distance_from_center(pos)}, '
          f'max dist: {max_distance}')
