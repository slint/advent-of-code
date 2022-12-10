import math
import itertools
from time import sleep

ENDC = "\033[0m"
COLORS = [f"\033[{c}m" for c in list(range(31, 38)) + list(range(91, 97))]

ADJ_DIST = math.sqrt(2)

# Missing pairwise from Python 3.9...
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def _draw(items):
    cols = int(max(abs(y) for _, y in items) * 2) + 10
    rows = int(max(abs(x) for x, _ in items) * 2) + 10

    # Clear the screen
    print("\033[H\033[J", end="")
    for col_idx in range(-cols // 2, cols // 2):
        for row_idx in range(-rows // 2, rows // 2):
            if (col_idx, row_idx) in items:
                print(items[(col_idx, row_idx)], end="")
            else:
                print("o", end="")
            print(" ", end="")
        print()


def is_adj(a, b):
    return math.dist(a, b) <= ADJ_DIST


def run(input_data: str, knot_count=10, visualize=False):
    moves = [l.split() for l in input_data.splitlines()]
    visit_counts = [set() for _ in range(10)]

    knots = [[0, 0] for _ in range(knot_count)]

    for direction, length in moves:
        move_head = knots[0]
        for _ in range(int(length)):
            if direction == "U":
                move_head[1] += 1
            if direction == "R":
                move_head[0] += 1
            if direction == "D":
                move_head[1] -= 1
            if direction == "L":
                move_head[0] -= 1

            for head, tail in pairwise(knots):
                dist = math.dist(head, tail)
                if not is_adj(head, tail):
                    # Tail has to move
                    if dist > 2:
                        # diagonal move
                        if head[0] > tail[0]:
                            tail[0] += 1
                        else:
                            tail[0] -= 1
                        if head[1] > tail[1]:
                            tail[1] += 1
                        else:
                            tail[1] -= 1
                    else:
                        # orthogonal move
                        if head[0] > tail[0]:
                            tail[0] += 1
                        elif head[0] < tail[0]:
                            tail[0] -= 1
                        if head[1] > tail[1]:
                            tail[1] += 1
                        elif head[1] < tail[1]:
                            tail[1] -= 1

            for idx, vc in enumerate(visit_counts):
                vc.add(tuple(knots[idx]))

        if visualize:
            _draw(
                items={
                    tuple(k): f'{COLORS[idx]}{"H" if idx == 0 else idx}{ENDC}'
                    for idx, k in enumerate(knots)
                }
            )
            sleep(0.1)

    print(f"Part one: {len(visit_counts[1])}")
    print(f"Part two: {len(visit_counts[-1])}")
