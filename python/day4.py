import sys
from collections import Counter
from pathlib import Path

data = Path(sys.argv[1]).read_text().splitlines()

CARDS = []
for line in data:
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    _, nums = line.split(": ")
    win_nums, card_nums = map(lambda s: set(s.split()), nums.split(" | "))
    CARDS.append(len(win_nums & card_nums))


def part_1():
    print(sum(2 ** (m - 1) for m in CARDS if m > 0))


def part_2():
    print(CARDS)
    card_counts = Counter(range(len(CARDS)))
    for card_idx, matches in enumerate(CARDS):
        copies = card_counts[card_idx]
        total_copies = sum(card_counts.values())
        print(f"{card_idx=}, {matches=}, {copies=}, {total_copies=}")

        if matches > 0:
            start_card_idx = card_idx + 1
            end_card_idx = min(start_card_idx + matches, len(CARDS))
            won_copies = {c: copies for c in range(start_card_idx, end_card_idx)}
            print(won_copies)
            card_counts.update(won_copies)
    print(sum(card_counts.values()))


part_1()
part_2()
