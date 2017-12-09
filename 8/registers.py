"""Day 8: I Heard You Like Registers."""

from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, Iterator, Tuple

Registers = Dict[str, int]
Comparison = Callable[[Registers], bool]
Transformation = Callable[[Registers], None]
Instruction = Tuple[str, Comparison, Transformation]


with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


CMP_OPS = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
}


def prase_instructions(instructions_text: str) -> Iterator[Instruction]:
    for instr in instructions_text.splitlines():
        left, right = instr.strip().split(' if ')
        src, op, val = left.split()
        cmp_src, cmp_op, cmp_val = right.split()

        def _compare(registers: Registers) -> bool:
            return CMP_OPS[cmp_op](registers[cmp_src], int(cmp_val))

        def _transform(registers: Registers) -> None:
            registers[src] += (1 if op == 'inc' else -1) * int(val)

        yield instr, _compare, _transform


def process_instructions(instructions_text: str) -> Tuple[Registers, int]:
    registers: defaultdict = defaultdict(int)
    current_max = 0
    for instr, comp, transform in prase_instructions(instructions_text):
        if comp(registers):
            transform(registers)
        current_max = max(max(registers.values()), current_max)
    return registers, current_max


def find_largest_register(instructions_text: str) -> Tuple[int, int]:
    registers, max_value = process_instructions(instructions_text)
    return max(registers.values()), max_value


def test_largest_register():
    assert find_largest_register(
        'b inc 5 if a > 1\n'
        'a inc 1 if b < 5\n'
        'c dec -10 if a >= 1\n'
        'c inc -20 if c == 10\n') == (1, 10)


if __name__ == '__main__':
    print(f'largest_register_values: {find_largest_register(puzzle_input)}')
