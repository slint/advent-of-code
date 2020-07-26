from pathlib import Path
from collections import defaultdict

INPUT = [l.split(')') for l in Path('input.txt').read_text().splitlines()]

ORBITS = defaultdict(list)

for a, b in INPUT:
    ORBITS[a].append(b)

print(max(len(v) for v in ORBITS.values()))
