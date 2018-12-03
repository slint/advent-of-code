"""Day 3: No Matter How You Slice It

https://adventofcode.com/2018/day/3
"""

from pathlib import Path
from collections import namedtuple, defaultdict
from itertools import product

Claim = namedtuple('Claim', ('id', 'pos', 'size'))


INPUT = Path('input.txt').read_text().splitlines()


def blank_fabric(size=1000):
    return defaultdict(lambda: [0, set()])
    return dict.fromkeys(product(range(1, size + 1), range(1, size + 1)), 0)


def parse_claim(c):
    id, _, pos, size = c.split()
    return Claim(
        id[1:],
        tuple(map(int, pos[:-1].split(','))),
        tuple(map(int, size.split('x')))
    )


def apply_claim(fabric, c: Claim):
    overlapped = set()
    for x in range(c.size[0]):
        for y in range(c.size[1]):
            pos = c.pos[0] + 1 + x, c.pos[1] + 1 + y
            fabric[pos][0] += 1
            fabric[pos][1].add(c.id)
            overlapped |= fabric[pos][1]
    return overlapped if len(overlapped) > 1 else set()


if __name__ == "__main__":
    claims = [parse_claim(c) for c in INPUT]
    fabric = blank_fabric()

    non_overlapping_claim_ids = {c.id for c in claims}
    for c in claims:
        non_overlapping_claim_ids -= apply_claim(fabric, c)
    overlapped = sum(1 for _ in (filter(lambda v: v[0] >= 2, fabric.values())))
    print(overlapped)
    print(non_overlapping_claim_ids)
