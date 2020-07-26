from pathlib import Path
from itertools import product

INPUT = Path('input.txt').read_text()
# INPUT = """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""


INSTRUCTIONS = tuple(map(int, INPUT.split(',')))
MAGIC = 19690720

def run_program(input_val=None, noun=None, verb=None):
    memory = list(INSTRUCTIONS)
    last_output = None
    if noun:
        memory[1] = noun
    if verb:
        memory[2] = verb
    pos = 0
    while True:
        op = str(memory[pos]).zfill(5)
        opcode = int(op[-2:])
        if opcode == 1:     # add
            l_param, r_param, o_pos = memory[pos + 1: pos + 4]
            l_val = l_param if int(op[-3]) else memory[l_param]
            r_val = r_param if int(op[-4]) else memory[r_param]
            memory[o_pos] = l_val + r_val
            pos += 4
        elif opcode == 2:   # mult
            l_param, r_param, o_pos = memory[pos + 1: pos + 4]
            l_val = l_param if int(op[-3]) else memory[l_param]
            r_val = r_param if int(op[-4]) else memory[r_param]
            memory[o_pos] = l_val * r_val
            pos += 4
        elif opcode == 3:   # input
            o_pos = memory[pos + 1]
            memory[o_pos] = input_val
            pos += 2
        elif opcode == 4:   # output
            o_param = memory[pos + 1]
            o_val = o_param if int(op[-3]) else memory[o_param]
            last_output = o_val
            pos += 2
        elif opcode == 5:   # jump-if-true
            c_param, j_param = memory[pos + 1: pos + 3]
            c_val = c_param if int(op[-3]) else memory[c_param]
            j_val = j_param if int(op[-4]) else memory[j_param]
            pos = j_val if c_val else (pos + 3)
        elif opcode == 6:   # jump-if-false
            c_param, j_param = memory[pos + 1: pos + 3]
            c_val = c_param if int(op[-3]) else memory[c_param]
            j_val = j_param if int(op[-4]) else memory[j_param]
            pos = j_val if (not c_val) else (pos + 3)
        elif opcode == 7:   # less-than
            l_param, r_param, o_pos = memory[pos + 1: pos + 4]
            l_val = l_param if int(op[-3]) else memory[l_param]
            r_val = r_param if int(op[-4]) else memory[r_param]
            memory[o_pos] = 1 if l_val < r_val else 0
            pos += 4
        elif opcode == 8:   # equals
            l_param, r_param, o_pos = memory[pos + 1: pos + 4]
            l_val = l_param if int(op[-3]) else memory[l_param]
            r_val = r_param if int(op[-4]) else memory[r_param]
            memory[o_pos] = 1 if l_val == r_val else 0
            pos += 4
        elif opcode == 99:  # halt
            break
    return last_output


# for noun, verb in product(range(100), range(100)):
#     if run_program(noun, verb) == MAGIC:
#         print(noun, verb, 100 * noun + verb)

print(run_program(input_val=5))
