#!/usr/bin/env python3

import sys
from pathlib import Path
import pkgutil
import importlib

if __name__ == "__main__":
    args = iter(sys.argv[1:])
    day_num = next(args, None)
    input_data = Path(next(args, "input.txt")).read_text()

    if not day_num:
        day_module = max(m.name for m in pkgutil.iter_modules(["solutions"]))
    else:
        day_module = f"day{day_num}"

    importlib.import_module(f"solutions.{day_module}").run(input_data)
