def computeDirSize(directories, dir, sizes):
    list_of_elem = directories[dir]
    dir_size = 0
    for elem in list_of_elem:
        if type(elem) is tuple:
            file, size = elem
            dir_size += size
        else:
            dir_to_find = dir + elem
            if dir_to_find not in sizes and elem != dir:
                if dir_to_find in directories:
                    computeDirSize(directories, dir_to_find, sizes)
                    dir_size += sizes[dir_to_find]
    sizes[dir] = dir_size

def main():
    directories = dict()
    directories["/"] = []
    current_dir = []
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('$'):
                if 'cd' in line:
                    move = line.split(" ")[-1]
                    if move == "/":
                        current_dir = ["/"]
                    elif move == "..":
                        current_dir.pop(-1)
                    else:
                        current_dir.append(move)
                        if "".join(current_dir) not in directories:
                            directories["".join(current_dir)] = []
            else:
                if line.startswith("dir"):
                    directory = line.split(" ")[-1]
                    if directory not in directories["".join(current_dir)]:
                        directories["".join(current_dir)].append(directory)
                else:
                    size = int(line.split(" ")[0])
                    file = line.split(" ")[1]
                    if file not in directories["".join(current_dir)]:
                        directories["".join(current_dir)].append((file, size))

        sizes = dict()
        computeDirSize(directories, "/", sizes)
        print(sizes)
        total_size = 0
        disk_size = 70000000
        needed_free_space = 30000000
        available = disk_size - sizes["/"]
        current = sizes["/"]
        for value in sizes.values():
            if value + available >= needed_free_space and value < current:
                current = value
        return current


def main2():
    print("toto")


if __name__ == '__main__':
    print(main())
