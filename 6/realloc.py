"""Day 6: Memory Reallocation."""

import itertools
import re
from pathlib import Path
from typing import List, Tuple

Memory = List[int]


with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def parse_memory(text: str) -> Memory:
    return [int(b) for b in re.split(r'\s+', text)]


def realloc(memory: Memory) -> Memory:
    max_index = memory.index(max(memory))
    blocks = memory[max_index]
    memory[max_index] = 0
    for i in range(blocks):
        memory[(max_index + i + 1) % len(memory)] += 1
        blocks -= 1
    return memory


def find_loop(memory_text: str) -> Tuple[int, int]:
    memory = parse_memory(memory_text)
    states = {tuple(memory): 0}
    for i in itertools.count():
        memory = realloc(memory)
        if tuple(memory) in states:
            return (i + 1), (i + 1) - states[tuple(memory)]
        else:
            states[tuple(memory)] = i + 1
    return None, None


def test_realloc():
    assert find_loop('0 2 7 0') == (5, 4)


if __name__ == '__main__':
    print(f'loop_1: {find_loop(puzzle_input)}')
