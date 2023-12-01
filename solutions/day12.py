import colorsys
from utils import c

MIN_H = 0
MAX_H = 100
NUM = 24

COLOR_MAP = {
    chr(ord('a') + idx): tuple(map(lambda v: int(v * 255), colorsys.hsv_to_rgb(h / 100, 1, 1)))
    for idx, h in enumerate(range(MIN_H, MAX_H, (MAX_H - MIN_H) // NUM))
}


def run(input_data: str, visualize=False):
    if visualize:
        for v in input_data:
            if v in COLOR_MAP:
                print(c(v, *COLOR_MAP[v]), end="")
            else:
                print(v, end="")

    START = None
    END = None
    _T = []
    for row_idx, line in enumerate(input_data.splitlines()):
        row = []

        for col_idx, value in enumerate(line):
            row.append(value)
            if value == 'S':
                START = row_idx, col_idx
            if value == 'E':
                END = row_idx, col_idx
        _T.append(row)

    T = Grid(_T)
    print(T[START])
    print(T[END])
    # print(f"Part one: {input_data}")
    # print(f"Part two: {input_data}")
