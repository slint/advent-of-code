from dataclasses import dataclass

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


# fmt: off
DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
)
# fmt: on


class Grid:
    def __init__(self, data, render_map=None):
        self.data = data
        self.render_map = render_map or {}

    def iter(self):
        for y, line in enumerate(self.data):
            for x in range(len(line)):
                yield Cell(x, y, self)

    @property
    def width(self):
        return max(len(line) for line in self.data)

    @property
    def height(self):
        return len(self.data)

    @property
    def rows(self):
        res = []
        for y in range(self.height):
            res.append([Cell(x, y, self) for x in range(self.width)])
        return res

    @property
    def cols(self):
        res = []
        for x in range(self.width):
            res.append([Cell(x, y, self) for y in range(self.height)])
        return res

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
                val = self.render_map.get(val, val)
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

