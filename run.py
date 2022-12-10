#!/usr/bin/env python3

import sys
from pathlib import Path
import pkgutil
import importlib

if __name__ == "__main__":

    cli_args = list(sys.argv[1:])
    visualize = bool(cli_args.pop(cli_args.index("-v"))) if "-v" in cli_args else None

    args = iter(cli_args)
    day_num = next(args, None)
    input_data = Path(next(args, "input.txt")).read_text()

    if not day_num:
        day_module = max(m.name for m in pkgutil.iter_modules(["solutions"]))
    else:
        day_module = f"day{day_num}"

    print(f"Running {day_module}")
    print(f"=============\n")
    importlib.import_module(f"solutions.{day_module}").run(
        input_data, visualize=visualize
    )
