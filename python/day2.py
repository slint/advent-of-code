import sys
from functools import reduce
from pathlib import Path

data = Path(sys.argv[1]).read_text().splitlines()

BAG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def draw_counts(draw):
    return {d.split()[1]: int(d.split(" ")[0]) for d in draw}


def is_valid_draw(draw):
    return all(cube_count <= BAG[cube_color] for cube_color, cube_count in draw.items())


def part_1():
    total = 0
    for line in data:
        game_id, cube_stats = line.split(": ")
        game_id = int(game_id.split()[1])
        cube_stats = [draw_counts(c.split(", ")) for c in cube_stats.split("; ")]
        if all(is_valid_draw(c) for c in cube_stats):
            total += game_id

    print(f"Part 1: {total = }")


def part_2():
    total = 0
    for line in data:
        game_id, cube_stats = line.split(": ")
        game_id = int(game_id.split()[1])
        cube_stats = [draw_counts(c.split(", ")) for c in cube_stats.split("; ")]
        max_cubes = {}
        for draw in cube_stats:
            for cube_color, cube_count in draw.items():
                max_cubes[cube_color] = max(max_cubes.get(cube_color, 0), cube_count)

        total += reduce(lambda acc, item: acc * item, max_cubes.values(), 1)

    print(f"Part 2: {total = }")


part_1()
part_2()
