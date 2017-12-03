"""Day 3 spiral memory."""

from collections import namedtuple
from enum import Enum
from itertools import cycle, islice, takewhile
from pathlib import Path
from typing import Iterator, NamedTuple, Tuple

with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


class Position(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


VECTORS = {
    Direction.RIGHT: (1, 0),
    Direction.UP: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.DOWN: (0, -1),
}


MEMORY_PORT = Position(0,0)


def get_spiral_directions() -> Iterator[Direction]:
    return cycle(
        [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN])


def gen_spiral() -> Iterator[Position]:
    spiral_directions = get_spiral_directions()
    steps_left = step = 0
    cur_pos = MEMORY_PORT
    yield cur_pos
    while True:
        if not steps_left:  # change direction
            direction = next(spiral_directions)
            step += 1 if direction in (Direction.RIGHT, Direction.LEFT) else 0
            steps_left = step
        steps_left -= 1
        xd, yd = VECTORS[direction]
        cur_pos = Position(cur_pos.x + xd, cur_pos.y + yd)
        yield cur_pos


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(b.x - a.x) + abs(b.y - a.y)


def slot_pos(slot_num: int) -> Position:
    return next(islice(gen_spiral(), slot_num - 1, None))


def memory_steps(slot_num: int) -> int:
    return manhattan_distance(slot_pos(slot_num), MEMORY_PORT)


def get_position_neighbors(pos: Position) -> Tuple[Position, ...]:
    return (
        Position(pos.x - 1, pos.y + 1), Position(pos.x, pos.y + 1),
        Position(pos.x + 1, pos.y + 1), Position(pos.x + 1, pos.y),
        Position(pos.x + 1, pos.y - 1), Position(pos.x, pos.y - 1),
        Position(pos.x - 1, pos.y - 1), Position(pos.x - 1, pos.y),
    )

def gen_slot_values() -> Iterator[Tuple[int, Position, int]]:
    discovered = {MEMORY_PORT: 1}
    for slot_num, pos in enumerate(gen_spiral()):
        if pos in discovered:
            yield slot_num, pos, discovered[pos]
        else:
            neighbors = get_position_neighbors(pos)
            val = sum(discovered[n] for n in neighbors if n in discovered)
            discovered[pos] = val
            yield slot_num, pos, val


def memory_init_value(limit: int) -> int:
    return next(val for _, __, val in gen_slot_values() if val > limit)


def test_memory_steps():
    test_data = ((1, 0), (12, 3), (23, 2), (1024, 31))
    assert all(memory_steps(inp) == res for inp, res in test_data)


def test_memory_init_value():
    test_data = (
        (1, 2), (2, 4), (4, 5), (5, 10), (10, 11), (11, 23), (23, 25),
        (25, 26), (26, 54), (54, 57), (57, 59), (59, 122), (122, 133),
        (133, 142), (142, 147), (147, 304), (330, 351), (351, 362), (362, 747),
        (747, 806))
    assert all(memory_init_value(inp) == res for inp, res in test_data)


if __name__ == '__main__':
    print(f'memory_steps: {memory_steps(int(puzzle_input))}')
    print(f'memory_init_value: {memory_init_value(int(puzzle_input))}')
