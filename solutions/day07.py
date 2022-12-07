FS = {
    "/": {"parent": "", "files": {}, "dirs": {}, "size": None},
}

SIZE_THRESHOLD = 100_000
AVAILABLE_SPACE = 70_000_000
FREE_SPACE = 30_000_000
TARGET_SPACE = AVAILABLE_SPACE - FREE_SPACE


def _dir_size(dirname, level=0):
    if FS[dirname]["size"] is not None:
        return FS[dirname]["size"]
    files_size = sum(FS[dirname]["files"].values())
    subdirs = FS[dirname]["dirs"].keys()
    dirs_size = 0
    tabs = level * "  "
    for subdir in subdirs:
        dirs_size += _dir_size(subdir, level=level + 1)
    FS[dirname]["size"] = files_size + dirs_size
    return FS[dirname]["size"]


def run(input_data: str):

    cur_dir = None
    for line in input_data.splitlines():
        parts = line.split()
        if parts[0] == "$":
            # Start of new cmd
            if parts[1] == "ls":
                pass
            if parts[1] == "cd":
                if parts[2] == "..":
                    cur_dir = FS[cur_dir]["parent"]
                elif parts[2] == "/":
                    cur_dir = "/"
                else:
                    cur_dir += parts[2] + "/"

        else:  # we're reading "ls" output then
            if parts[0] == "dir":
                # register new directory
                dirname = cur_dir + parts[1] + "/"
                FS.setdefault(
                    dirname, {"parent": cur_dir, "files": {}, "dirs": {}, "size": None}
                )
                FS[cur_dir]["dirs"].setdefault(dirname, 0)
            else:
                size, filename = parts
                FS[cur_dir]["files"].setdefault(filename, int(size))

    # Calculate total sizes
    total_size = 0
    for d in FS:
        if _dir_size(d) < SIZE_THRESHOLD:
            total_size += _dir_size(d)

    min_size = FS["/"]["size"] - TARGET_SPACE
    best_dir = "/"
    for d in FS:
        if min_size <= FS[d]["size"] <= FS[best_dir]["size"]:
            best_dir = d
    print(f"Part one: {total_size}")
    print(f"Part two: {FS[best_dir]['size']} ({best_dir})")
