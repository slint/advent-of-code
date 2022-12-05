import itertools

def are_overlapping(a, b, full=True):
    if full:
        return all(a[0] <= l <= a[1] for l in b)
    else:
        return any(a[0] <= l <= a[1] for l in b)


def run(input_data: str):

    full_overlap_count = 0
    partial_overlap_count = 0
    for pair in input_data.splitlines():
        first, second = [tuple(map(int, p.split("-"))) for p in pair.split(",")]

        for pair_perm in itertools.permutations((first, second)):
            if are_overlapping(*pair_perm):
                full_overlap_count += 1
                break  # so we don't double count pairs that contain each other

        for pair_perm in itertools.permutations((first, second)):
            if are_overlapping(*pair_perm, False):
                partial_overlap_count += 1
                break  # so we don't double count pairs that contain each other

    print(f"Part one: {full_overlap_count}")
    print(f"Part two: {partial_overlap_count}")
