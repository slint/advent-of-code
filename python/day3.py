import sys
from pathlib import Path
import string

input_data = Path(sys.argv[1]).read_text()

data = [list(l) for l in input_data.splitlines()]

HEIGHT = len(data) - 1
WIDTH = len(data[0]) - 1

NUMS = "".join(map(str, range(0, 10)))
NOT_SYMBOL = NUMS + "."

NUM_POSITIONS = {
    # (y, (x_s, x_e)): num
}
POS_TO_NUM = {
    # (x, y): (y, (x_s, x_e))
}

DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1),
)

def _add_num_pos(y, num_start, num_end):
    for x in range(num_start, num_end + 1):
        POS_TO_NUM[(x, y)] = (y, (num_start, num_end))


def _build_maps():
    num_start = None
    num = ""
    for y, line in enumerate(data):
        if num:
            num_end = WIDTH
            NUM_POSITIONS[(y - 1, (num_start, num_end))] = int(num)
            _add_num_pos(y - 1, num_start, num_end)
            num_start = None
            num = ""
            
        for x, val in enumerate(line):
            if val.isdigit():
                if not num:
                    num_start = x
                num += val
            else:
                # end of number
                if num:
                    num_end = x - 1
                    NUM_POSITIONS[(y, (num_start, num_end))] = int(num)
                    _add_num_pos(y, num_start, num_end)
                    num_start = None
                    num = ""


_punct_trans = str.maketrans(string.punctuation, len(string.punctuation) * ' ')
def clean_punct(s):
    return s.translate(_punct_trans)


def _adj_chars(x, y):
    top_y = max(0, y-1)
    bottom_y = min(HEIGHT, y+1)
    left_x = max(0, x-1)
    right_x = min(WIDTH, x+1)

    top = data[top_y][x]
    top_right = data[top_y][right_x]
    right = data[y][right_x]
    bottom_right = data[bottom_y][right_x]
    bottom = data[bottom_y][x]
    bottom_left = data[bottom_y][left_x]
    left = data[y][left_x]
    top_left = data[top_y][left_x]

    return (
        top_left, top, top_right, 
        left, right,
        bottom_left, bottom, bottom_right,
    )

def _adj_is_symbol(x, y):
    return any(c not in NOT_SYMBOL for c in _adj_chars(x, y))


def _adj_num_count(x, y):
    (
        top_left, top, top_right, 
        left, right,
        bottom_left, bottom, bottom_right,
    ) = _adj_chars(x, y)

    top_nums = len(clean_punct(top_left + top + top_right).split())
    bottom_nums = len(clean_punct(bottom_left + bottom + bottom_right).split())

    # left_nums = len(clean_punct(top_left + left, bottom_left).replace(" ", ""))
    # right_nums = len(clean_punct(top_right + right + bottom_right).replace(" ", ""))
    right_nums = int(right.isdigit())
    left_nums = int(left.isdigit())
    return (top_nums + bottom_nums + left_nums + right_nums)

def _get_full_adj_nums(x, y):
    (
        top_left, top, top_right, 
        left, right,
        bottom_left, bottom, bottom_right,
    ) = _adj_chars(x, y)
    
    

def part_1():
    total = 0
    is_part_number = False
    num = ""
    for y in range(len(data)):
        if num and is_part_number:
            total += int(num)

        is_part_number = False
        num = ""

        for x in range(len(data[y])):
            char = data[y][x]
            if char.isdigit():
                num += char
                is_part_number = is_part_number or _adj_is_symbol(x, y)
            else:
                # end of number
                if num and is_part_number:
                    total += int(num)
                num = ""
                is_part_number = False
    print(total)


def part_2():
    total = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            char = data[y][x]
            if char == "*" and _adj_num_count(x, y) == 2:
                num_ids = list({
                    POS_TO_NUM[(x + dx, y + dy)] 
                    for dx, dy in DIRECTIONS
                    if POS_TO_NUM.get((x + dx, y + dy))
                })
                total += NUM_POSITIONS[num_ids[0]] * NUM_POSITIONS[num_ids[1]]

    print(total)


print(input_data)
_build_maps()
print(POS_TO_NUM)
print(NUM_POSITIONS)
part_1()
part_2()
