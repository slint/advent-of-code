def _c(*rgb):
    return "\x1b[38;2;{};{};{}m".format(*rgb)


def _r():
    return "\x01\x1b[0m\x02"


def c(text, *rgb):
    return f"{_c(*rgb)}{text}{_r()}"


class Grid:
    class Col:
        def __init__(self, grid):
            self.grid = grid

        def __getitem__(self, index):
            pass

    class Row:
        def __init__(self, grid):
            self.grid = grid

        def __getitem__(self, index):
            pass

    class Cell:
        def __init__(self, grid, col, row):
            self.grid = grid
            self.row = row
            self.col = col

        @property
        def value(self):
            return self.grid.data[self.row][self.col]

        def _go_dir(self, dir):
            pass

        def __getattr__(self, key):
            if key in ("n", "s", "w", "e", "ne", "nw", "se", "sw"):
                return
            raise AttributeError(obj=self, name=key)

        @property
        def n(self):
            return self.grid[self.row, self.col - 1]

        @property
        def s(self):
            return self.grid[self.row, self.col + 1]

        @property
        def e(self):
            return self.grid[self.row + 1, self.col]

        @property
        def w(self):
            return self.grid[self.row - 1, self.col]



    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        if isinstance(index, tuple):
            row, col = index
            if col is None:
                return self.Row(self)
            if row is None:
                return self.Col(self.data[row][col])
            return self.Cell(self, row, col)
        else:
            return self.data[index]

    def rows(self):
        return

    def cols(self):
        pass
