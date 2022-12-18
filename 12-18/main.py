import copy

def parse_input(path):
    with open(path) as f:
        lines = f.readlines()
    droplets = []
    max_x, max_y, max_z = 0, 0, 0
    for line in lines:
        x, y, z = map(int, line.strip().split(","))
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        max_z = max(z, max_z)
        droplets.append((x, y, z))

    grid = [[["."] * (max_z+1) for _ in range(max_y+1)] for _ in range(max_x+1)]

    for drops in droplets:
        x, y, z = drops
        grid[x][y][z] = '#'
    return grid, droplets


def copy_grid(grid):
    return copy.deepcopy(grid)


def find_surface_area(drop, grid):
    x, y, z = drop
    surface_area = 0
    if x == 0 or grid[x-1][y][z] != '#':
        surface_area += 1
    if x == len(grid) - 1 or grid[x+1][y][z] != '#':
        surface_area += 1

    if y == 0 or grid[x][y-1][z] != '#':
        surface_area += 1
    if y == len(grid[x]) - 1 or grid[x][y+1][z] != '#':
        surface_area += 1

    if z == 0 or grid[x][y][z-1] != '#':
        surface_area += 1
    if z == len(grid[x][y]) - 1 or grid[x][y][z+1] != '#':
        surface_area += 1

    return surface_area


## Return True if the drop is trapped
def is_trapped(drop, grid):
    x, y, z = drop
    if x == 0 or x == len(grid)-1 or y == 0 or y == len(grid[x])-1 or z == 0 or z == len(grid[x][y])-1:
        return False

    # a neighboor was already analysed as not trapped
    if grid[x-1][y][z] == 'O' or grid[x+1][y][z] == 'O' or grid[x][y-1][z] == 'O' or grid[x][y+1][z] ==  'O' or\
            grid[x][y][z-1] == 'O' or grid[x][y][z+1] == 'O':
        return False

    if grid[x-1][y][z] == grid[x+1][y][z] == grid[x][y-1][z] == grid[x][y+1][z] == grid[x][y][z-1] == grid[x][y][z+1] == '#':
        return True

    grid[x][y][z] = '#'

    neighboors = [
        (x-1, y, z),
        (x+1, y, z),
        (x, y-1, z),
        (x, y+1, z),
        (x, y, z-1),
        (x, y, z+1),
    ]

    for x_n, y_n, z_n in neighboors:
        if grid[x_n][y_n][z_n] != '#':
            n_is_trapped = is_trapped((x_n, y_n, z_n), grid)
            if not n_is_trapped:
                return False
    return True



def find_trapped_air(grid):
    for x in range(1, len(grid)-1):
        for y in range(1, len(grid[x])-1):
            for z in range(1, len(grid[x][y])-1):
                if grid[x][y][z] != '#' and is_trapped((x, y, z), copy_grid(grid)):
                    grid[x][y][z] = '#'
    return grid




def main(input_path):
    grid, droplets = parse_input(input_path)
    find_trapped_air(grid)

    count = 0
    for drop in droplets:
        count += find_surface_area(drop, grid)
    return count



if __name__ == '__main__':
    print(main("input.txt"))
