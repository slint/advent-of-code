import sys
import math
from dataclasses import dataclass

input_data = open(sys.argv[1]).read()


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


PIPE_ASCII = {
    "|": "│",
    "-": "─",
    "J": "┘",
    "7": "┐",
    "L": "└",
    "F": "┌",
    ".": "▒",
}

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
                yield Cell(x, y, self)

    def __getitem__(self, pos: tuple[int, int]):
        x, y = pos
        # check bounds
        if not (0 <= y < self.height and 0 <= x < self.width):
            return None
        return Cell(x, y, self)

    def get_adjacent(self, pos: tuple[int, int]):
        x, y = pos
        return tuple(self[(x + dx, y + dy)] for dx, dy in DIRECTIONS)

    def print(self, highlight=()):
        for y, line in enumerate(self.data):
            print()
            for x, val in enumerate(line):
                val = PIPE_ASCII.get(val, val)
                if (x, y) in highlight:
                    print(
                        f"{Colors.OKGREEN}{val}{Colors.ENDC}",
                        end="",
                    )
                else:
                    print(val, end="")
        print()


@dataclass
class Cell:
    x: int
    y: int
    grid: Grid

    @property
    def value(self):
        return self.grid.data[self.y][self.x]

    @property
    def adjacent(self):
        return self.grid.get_adjacent((self.x, self.y))

    @property
    def north(self):
        pos = (self.x, self.y - 1)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def east(self):
        pos = (self.x + 1, self.y)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def south(self):
        pos = (self.x, self.y + 1)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def west(self):
        pos = (self.x - 1, self.y)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def northeast(self):
        pos = (self.x + 1, self.y - 1)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def southeast(self):
        pos = (self.x + 1, self.y + 1)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def southwest(self):
        pos = (self.x - 1, self.y + 1)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    @property
    def northwest(self):
        pos = (self.x - 1, self.y - 1)
        if self.grid[pos]:
            return Cell(*pos, self.grid)

    def __getitem__(self, direction):
        return getattr(self, direction)

    def __repr__(self) -> str:
        return f"<Cell({self.x}, {self.y}): {self.value} >"


grid = Grid([list(line) for line in input_data.splitlines()])


START = [cell for cell in grid.iter_values() if cell.value == "S"][0]

PIPE_TYPES = {
    "|": ("north", "south"),
    "-": ("east", "west"),
    "L": ("north", "east"),
    "J": ("north", "west"),
    "7": ("south", "west"),
    "F": ("south", "east"),
}

ORIENTATIONS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


def follow_pipe(origin, pipe_cell: Cell):
    original_cell = next_cell = pipe_cell
    visited = []
    while next_cell is not None:
        visited.append((next_cell.x, next_cell.y))
        pipe_directions = PIPE_TYPES.get(next_cell.value, ())
        if origin in pipe_directions:
            (destination,) = set(pipe_directions) - {origin}
            next_cell = next_cell[destination]
            origin = ORIENTATIONS[destination]
            if next_cell and next_cell.value == "S":
                # we found the loop
                return visited, original_cell
        else:
            # dead end
            return visited, None
    return visited, None


def part_1():
    for origin, cell in (
        ("south", START.north),
        ("west", START.east),
        ("north", START.south),
        ("east", START.west),
    ):
        if cell and cell.value in PIPE_TYPES:
            visited, end_cell = follow_pipe(origin, cell)
            grid.print(highlight=visited)
            print(math.ceil(len(visited) / 2))


def part_2():
    pass


part_1()
part_2()

