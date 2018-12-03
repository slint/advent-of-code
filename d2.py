"""Day 2: Inventory Management System

https://adventofcode.com/2018/day/2
"""

from pathlib import Path
from collections import Counter
from functools import reduce
import operator


INPUT = Path('input.txt').read_text().splitlines()


def prod(it):
    return reduce(operator.mul, it, 1)


if __name__ == "__main__":

    # Look ma' I can write FP nonsense now!
    res = prod(reduce(
        lambda s, c: (s[0] + (2 in c), s[1] + (3 in c)),
        map(lambda c: c.values(), map(Counter, INPUT)),
        (0, 0)
    ))
    print(f'Answer 1: {res}')

    pos_let = list(map(set, map(enumerate, INPUT)))
    for idx_i, i in enumerate(pos_let):
        for j in pos_let[idx_i:]:
            if len(i - j) == 1:
                word = ''.join(x for _, x in sorted(i & j))
                print(f'Answer 2: {word}')
