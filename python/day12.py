from functools import reduce
import itertools
import sys
from collections import Counter

data = open(sys.argv[1]).read().splitlines()


REPORTS = []


for line in data:
    conditions, counts = line.split()
    counts = list(map(int, counts.split(",")))
    REPORTS.append((conditions, counts))


def condition_configs(conditions, counts):
    valid_cfgs = 0
    cfgs = list(itertools.product(".#", repeat=conditions.count("?")))
    for cfg in cfgs:
        new_cond = reduce(lambda res, c: res.replace("?", c, 1), cfg, conditions)
        cfg_counts = [len(g) for g in new_cond.split(".") if g]
        if cfg_counts == counts:
            valid_cfgs += 1
    return valid_cfgs


def part_1():
    total = 0
    for cond, counts in REPORTS:
        total += condition_configs(cond, counts)
    print(total)


def part_2():
    total = 0
    for idx, (cond, counts) in enumerate(REPORTS):
        print(idx)
        cond = cond * 5
        counts = counts * 5
        total += condition_configs(cond, counts)
    print(total)


part_1()
# part_2()
