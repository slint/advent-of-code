from pathlib import Path
from collections import defaultdict, Counter
import re

INPUT = '240298-784956'
lower, upper = map(int, INPUT.split('-'))

valid = 0
for p in range(lower, upper + 1):
    s = str(p)
    if not all(s[i] <= s[i + 1] for i in range(len(s) - 1)):
        continue

    repeating_digits = re.findall(r'((\d)\2+)', s)
    doubles = [d for m, d in repeating_digits if len(m) == 2]
    has_groups = any((d in doubles and len(m) == 4) for m, d in repeating_digits)
    if doubles and not has_groups:
        print(s)

    if doubles and not has_groups:
        valid += 1
print(valid)
