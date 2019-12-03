from pathlib import Path
from itertools import product

INSTRUCTIONS = tuple(map(int, Path('input.txt').read_text().split(',')))
MAGIC = 19690720

def run_program(noun, verb):
    memory = list(INSTRUCTIONS)
    memory[1] = noun
    memory[2] = verb
    pos = 0
    while True:
        opcode = memory[pos]
        if opcode == 1:
            l_pos, r_pos, o_pos = memory[pos + 1: pos + 4]
            memory[o_pos] = memory[l_pos] + memory[r_pos]
        elif opcode == 2:
            l_pos, r_pos, o_pos = memory[pos + 1: pos + 4]
            memory[o_pos] = memory[l_pos] * memory[r_pos]
        elif opcode == 99:
            break
        pos += 4
    return memory[0]


for noun, verb in product(range(100), range(100)):
    if run_program(noun, verb) == MAGIC:
        print(noun, verb, 100 * noun + verb)
