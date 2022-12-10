def run(input_data: str, visualize=False):

    reg = {"X": 1}
    signal_strengths = 0
    display = ""

    def _noop():
        yield

    def _addx(V):
        yield
        yield
        reg["X"] += V


    def iter_instructions():
        for instr in input_data.splitlines():
            if instr == "noop":
                yield from _noop()
            else:  # addx
                yield from _addx(int(instr.rsplit()[-1]))

    for cycle, _ in enumerate(iter_instructions(), start=1):
        if (cycle - 20 % 40) == 0:
            signal_strengths += cycle * reg["X"]

        draw_pos = (cycle - 1) % 40
        if draw_pos == 0:
            display += "\n"
        if (reg["X"] - 1) <= draw_pos <= (reg["X"] + 1):
            display += "#"
        else:
            display += "."

    print(f"Part one: {signal_strengths}")
    print(f"Part two: \n{display}")
