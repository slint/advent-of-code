from copy import deepcopy

def run(input_data: str):
    stacks_data, instructions = map(str.splitlines, input_data.split("\n\n"))

    num_stacks = len(stacks_data[-2].split())
    stacks = [[] for _ in range(num_stacks)]
    for line in reversed(stacks_data[:-1]):
        for idx, stack in enumerate(stacks):
            crate = line[idx * 4 + 1]
            if crate.strip():
                stack.append(crate)

    new_stacks = deepcopy(stacks)

    for instr in instructions:
        count, src, dst = map(int, instr.split()[1::2])
        for _ in range(count):
            stacks[dst - 1].append(stacks[src - 1].pop())

        src_stack = new_stacks[src -1]
        dst_stack = new_stacks[dst -1]

        dst_stack.extend(src_stack[-count:])
        del src_stack[-count:]

    top_crates = [stack[-1] for stack in stacks]
    top_crates_new = [stack[-1] for stack in new_stacks]

    print(f"Part one: {''.join(top_crates)}")
    print(f"Part two: {''.join(top_crates_new)}")
