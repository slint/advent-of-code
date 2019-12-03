from pathlib import Path

lines = list(map(int, Path('input.txt').read_text().splitlines()))

print(sum(int(l / 3) - 2 for l in lines))

total = 0
for l in lines:
    f = 0
    t = l
    while t > 6:
        t = int(t / 3) - 2
        f += t
    total += f

print(total)
