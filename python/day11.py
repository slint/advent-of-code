import itertools
import sys

from utils import Grid

data = [list(line) for line in open(sys.argv[1]).read().splitlines()]

grid = Grid(data)


def expand(n=1):
    rows_expand = []
    cols_expand = []
    for row in grid.rows:
        if {c.value for c in row} == {"."}:
            rows_expand.append(row[0].y)

    for col in grid.cols:
        if {c.value for c in col} == {"."}:
            cols_expand.append(col[0].x)

    print(rows_expand, cols_expand)

    for y in reversed(rows_expand):
        print(y)
        new_row = list(grid.data[y])
        for idx in range(n):
            if idx % 10000 == 0:
                print(idx)
            grid.data.insert(y, new_row)

    for x in reversed(cols_expand):
        print(x)
        for line in grid.data:
            for idx in range(n):
                if idx % 10_000 == 0:
                    print(idx)
                line.insert(x, ".")


def distance(c1, c2):
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)


def part_1():
    expand()
    galaxies = [c for c in grid.iter() if c.value == "#"]
    galaxy_pairs = list(itertools.combinations(galaxies, 2))
    total = 0
    for g1, g2 in galaxy_pairs:
        dist = distance(g1, g2)
        total += dist
    print(total)


def part_2():
    expand(n=1_000_000)
    galaxies = [c for c in grid.iter() if c.value == "#"]
    galaxy_pairs = list(itertools.combinations(galaxies, 2))
    total = 0
    for g1, g2 in galaxy_pairs:
        dist = distance(g1, g2)
        total += dist
    print(total)


# part_1()
part_2()
