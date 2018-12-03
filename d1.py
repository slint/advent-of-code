"""Day 1: Chronal Calibration

https://adventofcode.com/2018/day/1
"""

from pathlib import Path
from itertools import cycle

INPUT = Path('input.txt').read_text().splitlines()

if __name__ == "__main__":
    nums = list(map(int, INPUT))
    sum_of_nums = sum(nums)
    print(f'Answer 1: {sum_of_nums}')

    total = 0
    encountered = {total}
    for n in cycle(nums):
        total += n
        if total in encountered:
            print(f'Answer 2: {total}')
            break
        else:
            encountered.add(total)
