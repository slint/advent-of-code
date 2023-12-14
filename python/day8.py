import itertools
import math
import sys

data = open(sys.argv[1]).read().splitlines()

DIRECTIONS = data[0]
NODES: dict[str, tuple[str, str]] = {}

for line in data[2:]:
    node, options = line.split(" = ")
    left, right = options.strip("()").split(", ")
    NODES[node] = (left, right)


def walk_node(cur_node, direction):
    left, right = NODES[cur_node]
    if direction == "L":
        cur_node = left
    else:
        cur_node = right
    return cur_node


def steps_to_z(node) -> int:
    for step, direction in enumerate(itertools.cycle(DIRECTIONS), start=1):
        node = walk_node(node, direction)
        if node.endswith("Z"):
            return step


def part_1():
    cur_node = "AAA"
    for step, direction in enumerate(itertools.cycle(DIRECTIONS), start=1):
        cur_node = walk_node(cur_node, direction)
        if cur_node == "ZZZ":
            print(step)
            break


def part_2():
    node_steps_to_z = [steps_to_z(n) for n in NODES if n.endswith("A")]
    print(math.lcm(*node_steps_to_z))


part_1()
part_2()
