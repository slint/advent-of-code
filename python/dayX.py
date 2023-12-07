import sys
from pathlib import Path

data = Path(sys.argv[1]).read_text().splitlines()

