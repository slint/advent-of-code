import math

ENDC = "\033[0m"
GREEN = "\033[92m"


def run(input_data: str):
    T = [list(map(int, l)) for l in input_data.splitlines()]
    cols = len(T)
    rows = len(T[0])

    visible = set()
    for col_idx, row in enumerate(T):
        prev_high_tree = -1
        for row_idx, t in enumerate(row):
            if t > prev_high_tree:
                visible.add((col_idx, row_idx))
                prev_high_tree = t

        prev_high_tree = -1
        for row_idx in reversed(range(len(row))):
            t = row[row_idx]
            if t > prev_high_tree:
                visible.add((col_idx, row_idx))
                prev_high_tree = t

    for row_idx in range(rows):
        prev_high_tree = -1
        for col_idx in range(len(T)):
            t = T[col_idx][row_idx]
            if t > prev_high_tree:
                visible.add((col_idx, row_idx))
                prev_high_tree = t

        prev_high_tree = -1
        for col_idx in reversed(range(len(T))):
            t = T[col_idx][row_idx]
            if t > prev_high_tree:
                visible.add((col_idx, row_idx))
                prev_high_tree = t

    def _score(col, row):
        h = T[col][row]

        def _visible_trees(tree_slice):
            res = 0
            for t in tree_slice:
                if t < h:
                    res += 1
                elif t == h:
                    res += 1
                    break
                else:
                    break
            return res

        top_score = _visible_trees([c[row] for c in reversed(T[:col])])
        bottom_score = _visible_trees([c[row] for c in T[(col + 1) :]])
        right_score = _visible_trees(T[col][(row + 1) :])
        left_score = _visible_trees(reversed(T[col][:row]))
        return math.prod((top_score, bottom_score, right_score, left_score))

    highest_score = -1
    highest_score_tree = (0, 0)
    for row_idx in range(rows):
        for col_idx in range(len(T)):
            score = _score(col_idx, row_idx)
            highest_score_tree = (col_idx, row_idx)
            highest_score = max(highest_score, score)

    # Pretty-print trees
    for col_idx, row in enumerate(T):
        for row_idx, t in enumerate(row):
            t = T[col_idx][row_idx]
            if (col_idx, row_idx) in visible:
                print(f"{GREEN}{t}{ENDC} ", end="")
            else:
                print(f"{t} ", end="")
        print()

    print(f"Part one: {len(visible)}")
    print(f"Part two: {highest_score} ({highest_score_tree})")
