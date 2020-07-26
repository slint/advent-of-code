from pathlib import Path
from collections import defaultdict

w1_instructions, w2_instructions = map(
    lambda l: l.split(','),
    Path('input.txt').read_text().splitlines()
)

OPS = {
    'R': lambda x, y: (x + 1, y),
    'L': lambda x, y: (x - 1, y),
    'U': lambda x, y: (x, y + 1),
    'D': lambda x, y: (x, y - 1),
}

def traverse_points(instructions):
    visited_points = set()
    x = y = 0
    for i in instructions:
        direction = i[0]
        distance = int(i[1:])
        for _ in range(distance):
            x, y = OPS[direction](x, y)
            yield x ,y

w1_locations = defaultdict(list)
w2_locations = defaultdict(list)

w1_steps = w2_steps = 0
min_steps = float('inf')
for w1_loc, w2_loc in zip(traverse_points(w1_instructions), traverse_points(w2_instructions)):
    w1_steps += 1
    w2_steps += 1
    w1_locations[w1_loc].append(w1_steps)
    w2_locations[w2_loc].append(w2_steps)

    if w1_loc in w2_locations:
        w2_cross_steps = w2_locations[w1_loc][0]
        min_steps = min(min_steps, w2_cross_steps + w1_steps)
    if w2_loc in w1_locations:
        w1_cross_steps = w1_locations[w2_loc][0]
        min_steps = min(min_steps, w1_cross_steps + w2_steps)


print (min_steps)
crossing_points = w1_locations.keys() & w2_locations.keys()

print(min(abs(x) + abs(y) for x, y in crossing_points))
