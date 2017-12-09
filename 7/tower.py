"""Day 7: Recursive Circus."""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

with open(Path(__file__).parent / 'input.txt') as fp:
    puzzle_input = fp.read().strip()


def parse_tower_line(line: str) -> Tuple[str, int, List[str]]:
    parts = iter(line.split(' -> '))
    program, weight = next(parts).strip().split()
    above = next(parts, None)
    return (program, int(weight[1:-1]), above.split(', ') if above else None)


def parse_tower(tower_text: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    lookup: Dict[str, str] = {}
    programs: Dict[str, int] = {}
    for line in tower_text.splitlines():
        program, weight, above = parse_tower_line(line)
        programs[program] = weight
        for p in (above or []):
            programs.setdefault(p, None)
            lookup[p] = program
    return programs, lookup


def get_tower_bottom(programs, lookup) -> str:
    return set((programs.keys() - lookup.keys())).pop()


def find_tower_bottom(tower_text: str) -> str:
    return get_tower_bottom(*parse_tower(tower_text))


def test_tower():
    assert find_tower_bottom((
        'pbga (66)\n'
        'xhth (57)\n'
        'ebii (61)\n'
        'havc (66)\n'
        'ktlj (57)\n'
        'fwft (72) -> ktlj, cntj, xhth\n'
        'qoyq (66)\n'
        'padx (45) -> pbga, havc, qoyq\n'
        'tknk (41) -> ugml, padx, fwft\n'
        'jptl (61)\n'
        'ugml (68) -> gyxo, ebii, jptl\n'
        'gyxo (61)\n'
        'cntj (57)\n'
    )) == 'tknk'


def calculate_tower_weights(programs, lookup):
    bottom = get_tower_bottom(programs, lookup)
    rev_lookup = {}
    for k, v in lookup.items():
        rev_lookup.setdefault(v, set())
        rev_lookup[v].add(k)

    weights = {}

    def get_tower_weight(program):
        weight = programs[program]
        if program in rev_lookup:
            weight += sum(get_tower_weight(p) for p in rev_lookup[program])
        weights[program] = weight
        return weight
    get_tower_weight(bottom)
    return weights, rev_lookup


def find_unbalanced_tower(tower_text: str):
    programs, lookup = parse_tower(tower_text)
    weights, rev_lookup = calculate_tower_weights(programs, lookup)
    bottom = get_tower_bottom(programs, lookup)
    cur = bottom
    above = rev_lookup[cur]
    while True:
        cur_weights: defaultdict = defaultdict(list)
        for p in above:
            cur_weights[weights[p]].append(p)
        if len(cur_weights) <= 1:  # The problem is our program
            siblings = tuple(weights[p] for p in rev_lookup[lookup[cur]])
            return cur, programs[cur], siblings
        else:
            cur = next(v[0] for k, v in cur_weights.items() if len(v) == 1)
            above = rev_lookup[cur]


if __name__ == '__main__':
    print(f'tower_bottom_program: {find_tower_bottom(puzzle_input)}')
    print(f'unbalanced: {find_unbalanced_tower(puzzle_input)}')
