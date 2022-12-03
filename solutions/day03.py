from collections import Counter
from itertools import islice

GROUP_SIZE = 3

def _priority(c):
    return ord(c) - (96 if 'a' <= c <= 'z' else 38)


def batched(iterable, n):
    it = iter(iterable)
    while (batch := list(islice(it, n))):
        yield batch


def run(input_data: str):
    priorities_sum = 0
    badge_priorities_sum = 0
    for elves_group in batched(input_data.splitlines(), GROUP_SIZE):
        group_common = None
        for rucksack in elves_group:
            mid = len(rucksack) // 2
            first, second = Counter(rucksack[:mid]), Counter(rucksack[mid:])
            common = first & second
            item = list(common.keys())[0]
            priorities_sum += _priority(item)

            if group_common is None:
                group_common = first | second
            else:
                group_common &= first | second
        badge = list(group_common.keys())[0]
        badge_priorities_sum += _priority(badge)

    print(f"Part one: {priorities_sum}")
    print(f"Part two: {badge_priorities_sum}")

