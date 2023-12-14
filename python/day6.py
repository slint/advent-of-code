import sys
from pathlib import Path

data = Path(sys.argv[1]).read_text().splitlines()

RACES = dict(zip(*[list(map(int, line.split()[1:])) for line in data]))
RACE = dict([tuple(int("".join(line.split()[1:])) for line in data)])


def race_result(speed, duration):
    return (duration - speed) * speed


def part_1():
    result = 1
    for duration, record in RACES.items():
        winning_races = len(
            [
                speed
                for speed in range(duration)
                if race_result(speed, duration) > record
            ]
        )
        result *= winning_races
    print(result)


def part_2():
    for duration, record in RACE.items():
        winning_races = len(
            [
                speed
                for speed in range(duration)
                if race_result(speed, duration) > record
            ]
        )
        print(winning_races)


part_1()
part_2()
