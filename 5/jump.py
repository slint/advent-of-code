"""Day 5: A Maze of Twisty Trampolines, All Alike."""

from pathlib import Path
from typing import Callable, Iterator, List, Tuple


InstrInfo = Tuple[int, List[int]]
InstrTransform = Callable[[int], int]


with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def parse_instructions(instructions_text: str) -> List[int]:
    return [int(i) for i in instructions_text.splitlines() if i]


def add_one(instr: int) -> int:
    return instr + 1


def some_logic(instr):
    return (instr - 1) if instr >= 3 else (instr + 1)


def run_instructions(
        instructions_text: str,
        instr_transform: InstrTransform=None) -> Iterator[InstrInfo]:
    instr_transform = instr_transform or add_one
    cur_pos = 0
    instructions = parse_instructions(instructions_text)
    while 0 <= cur_pos <= len(instructions) - 1:
        yield cur_pos, instructions
        cur_instr = instructions[cur_pos]
        instructions[cur_pos] = instr_transform(instructions[cur_pos])
        cur_pos += cur_instr


def count_steps(instructions: str,
                instr_transform: InstrTransform=None) -> int:
    return len(list(run_instructions(instructions, instr_transform)))


def test_count_steps():
    assert count_steps('0\n3\n0\n1\n-3\n') == 5


def test_count_steps_some_logic():
    assert count_steps('0\n3\n0\n1\n-3\n', some_logic) == 10


if __name__ == '__main__':
    print(f'count_steps_1: {count_steps(puzzle_input)}')
    print(f'count_steps_2: {count_steps(puzzle_input, some_logic)}')
