import sys
from pathlib import Path
import string


# fmt: off
DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
)
# fmt: on


class Grid:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def iter_values(self):
        for y, line in enumerate(self.data):
            for x, val in enumerate(line):
                yield ((x, y), val)

    def __getitem__(self, pos: tuple[int, int]):
        x, y = pos
        # check bounds
        if not (0 < y < self.height and 0 < x < self.width):
            return ""
        return self.data[y][x]

    def get_adjacent(self, pos: tuple[int, int]):
        x, y = pos
        return tuple(
            ((x_ret := x + dx, y_ret := y + dy), self[(x_ret, y_ret)])
            for dx, dy in DIRECTIONS
        )


input_data = Path(sys.argv[1]).read_text()
grid = Grid([list(line) for line in input_data.splitlines()])


NUMBER_POSITIONS = {
    # ((x_start, x_end), y): num
}
POSITION_TO_NUMBER = {
    # (x, y): ((x_start, x_end), y)
}


def _register_number(x_start, x_end, y, val):
    key = ((x_start, x_end), y)
    NUMBER_POSITIONS[key] = val
    for x in range(x_start, x_end + 1):
        POSITION_TO_NUMBER[(x, y)] = key


number_start = None
number = ""
for (x, y), char in grid.iter_values():
    if char.isdigit():
        if not number:
            number_start = x
        number += char
    else:
        # end of number
        if number:
            _register_number(number_start, x - 1, y, int(number))
            number_start = None
            number = ""
    # end of line also ends the number
    if number and x == (grid.width - 1):
        _register_number(number_start, x, y, int(number))
        number_start = None
        number = ""


def has_adjacent_symbol(x, y):
    return any(c not in (string.digits + ".") for _, c in grid.get_adjacent((x, y)))


def part_1():
    total = 0
    for ((x_start, x_end), y), num in NUMBER_POSITIONS.items():
        if any(has_adjacent_symbol(x, y) for x in range(x_start, x_end + 1)):
            total += num
    print(total)


def part_2():
    total = 0
    for (x, y), char in grid.iter_values():
        if char == "*":
            adjacent_numbers = {
                num_key
                for (adj_x, adj_y), _ in grid.get_adjacent((x, y))
                if (num_key := POSITION_TO_NUMBER.get((adj_x, adj_y)))
            }
            if len(adjacent_numbers) == 2:
                num_a_key, num_b_key = list(adjacent_numbers)
                num_a_val = NUMBER_POSITIONS[num_a_key]
                num_b_val = NUMBER_POSITIONS[num_b_key]
                total += num_a_val * num_b_val

    print(total)


part_1()
part_2()
