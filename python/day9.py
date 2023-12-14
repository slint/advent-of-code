import itertools
import sys

data = open(sys.argv[1]).read().splitlines()

REPORTS = [list(map(int, d.split())) for d in data]


def build_sequences(report):
    result = [report]
    cur_seq = report
    while set(cur_seq) != {0}:
        next_seq = [b - a for a, b in itertools.pairwise(cur_seq)]
        result.append(next_seq)
        cur_seq = next_seq
    return result


def extrapolate(sequences: list[list[int]]):
    for idx, (bottom_seq, top_seq) in enumerate(
        itertools.pairwise(reversed(sequences))
    ):
        if idx == 0:
            bottom_seq.append(0)
        new_val = top_seq[-1] + bottom_seq[-1]
        top_seq.append(new_val)


def extrapolate_previous(sequences: list[list[int]]):
    for idx, (bottom_seq, top_seq) in enumerate(
        itertools.pairwise(reversed(sequences))
    ):
        if idx == 0:
            bottom_seq.insert(0, 0)
        new_val = top_seq[0] - bottom_seq[0]
        top_seq.insert(0, new_val)


def part_1():
    total = 0
    for r in REPORTS:
        sequences = build_sequences(r)
        extrapolate(sequences)
        total += sequences[0][-1]
    print(total)


def part_2():
    total = 0
    for r in REPORTS:
        sequences = build_sequences(r)
        extrapolate_previous(sequences)
        total += sequences[0][0]
    print(total)


part_1()
part_2()
