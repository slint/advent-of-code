import sys
from pathlib import Path
import bisect

data = Path(sys.argv[1]).read_text().split("\n\n")

SEEDS = list(map(int, data[0].split(": ")[1].split()))
MAT_MAP = {}
MAPS = {}
MAP_RANGES = {}



def _parse_map(m: str):
    title, *mappings = m.splitlines()
    # <src>-to-<dst> map:
    title, _ = title.split()
    src, dst = title.split("-to-")
    print(f"parsing {src=} to {dst=}")

    # <dst_start> <src_start> <length>
    mappings = [tuple(map(int, m.split())) for m in mappings]
    mat_mapping = {}
    for dst_start, src_start, length in mappings:
        mat_mapping[range(src_start, src_start + length)] = dst_start

    MAT_MAP[src] = dst
    MAPS[(src, dst)] = mat_mapping
    MAP_RANGES[(src, dst)] = sorted(mat_mapping.keys(), key=lambda r: (r.start, r.stop))


for m in data[1:]:
    _parse_map(m)


def resolve_mat(src_val, src):
    dst = MAT_MAP.get(src)
    if not dst:
        return src_val

    res = None
    mat_map = MAPS[(src, dst)]
    # speed-up the lookup...
    for src_range, dst_start in mat_map.items():
        if src_val in src_range:
            res = dst_start + (src_val - src_range.start)
            break
    if res is None:
        res = src_val

    return resolve_mat(res, dst)


def part_1():
    print(min(resolve_mat(s, "seed") for s in SEEDS))


def part_2():
    locations = []
    for offset in range(0, len(SEEDS), 2):
        seed_start, count = SEEDS[offset : offset + 2]
        print(f"checking {seed_start}-{seed_start + count}")
        for s in range(seed_start, seed_start + count):
            locations.append(resolve_mat(s, "seed"))
    print(min(locations))


part_1()
part_2()
