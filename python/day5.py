import itertools
import sys

data = open(sys.argv[1]).read().split("\n\n")

SEEDS = list(map(int, data[0].split(": ")[1].split()))
MATERIALS_MAP = {
    # <src>: <dst>
    # e.g. "seed": "soil"
}
MAPS = {
    # (<src>, <dst>): {<src_range>: <dst_range>, ...}
    # e.g. ("seed", "soil"): {range(98, 100): range(50, 52), range(50, 98): range(52, 100)}
}


def _parse_map(m: str):
    title, *mappings = m.splitlines()
    # <src>-to-<dst> map:
    title, _ = title.split()
    src, dst = title.split("-to-")

    # <dst_start> <src_start> <length>
    mappings = [tuple(map(int, m.split())) for m in mappings]
    mat_mapping = {}
    for dst_start, src_start, length in mappings:
        src_range = range(src_start, src_start + length)
        dst_range = range(dst_start, dst_start + length)
        mat_mapping[src_range] = dst_range

    MATERIALS_MAP[src] = dst
    MAPS[(src, dst)] = mat_mapping


for m in data[1:]:
    _parse_map(m)


def match_range(val: range, options: list[range]) -> dict[range, range | None]:
    res: dict[range, range | None] = {}

    current = val
    options = sorted(options, key=lambda r: (r.start, r.stop))
    for o in options:
        # starts before option
        if current.start < o.start:
            # ends before option
            if current.stop < o.start:
                # safe to stop completely
                break

            # add outside part
            res[range(current.start, o.start)] = None
            # add inside part
            res[range(o.start, min(current.stop, o.stop))] = o

            # if leftover, update current
            if current.stop > o.stop:
                current = range(o.stop, current.stop)
            else:
                current = None
                break

        # start inside option
        if o.start <= current.start < o.stop:
            # fully contained in option
            if current.stop <= o.stop:
                res[current] = o
                current = None
                break

            # add inside part
            res[range(current.start, min(current.stop, o.stop))] = o
            # update leftover
            if current.stop > o.stop:
                current = range(o.stop, current.stop)
            else:
                current = None
                break

    # fill in the rest
    if current:
        res[current] = None

    return res


def resolve_mat_range(src_range: range, src_material: str) -> list[range]:
    dst_material = MATERIALS_MAP.get(src_material)
    if not dst_material:
        return [src_range]

    dst_ranges = []
    mat_map = MAPS[(src_material, dst_material)]
    range_matches = match_range(src_range, list(mat_map.keys()))
    for src_range_part, src_range_part_match in range_matches.items():
        if src_range_part_match is None:
            dst_range_part = src_range_part
        else:
            dst_map = mat_map[src_range_part_match]
            delta = dst_map.start - src_range_part_match.start
            dst_range_part = range(
                src_range_part.start + delta,
                src_range_part.stop + delta,
            )
        dst_ranges.append(dst_range_part)

    result = []
    for dst_range in dst_ranges:
        result.extend(resolve_mat_range(dst_range, dst_material))

    return result


def part_1():
    smallest_loc = float("inf")
    for s in SEEDS:
        res = min(loc.start for loc in resolve_mat_range(range(s, s + 1), "seed"))
        if res < smallest_loc:
            smallest_loc = res
    print(smallest_loc)


def part_2():
    smallest_loc = float("inf")
    for seed_start, count in itertools.batched(SEEDS, 2):
        seed_range = range(seed_start, seed_start + count)
        print(f"checking {seed_range}")
        res = min(loc.start for loc in resolve_mat_range(seed_range, "seed"))
        if res < smallest_loc:
            smallest_loc = res
    print(smallest_loc)


part_1()
part_2()
