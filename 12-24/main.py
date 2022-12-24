from copy import deepcopy

directions = {
    '^': lambda x: (x[0], x[1] - 1),
    'v': lambda x: (x[0], x[1] + 1),
    '>': lambda x: (x[0] + 1, x[1]),
    '<': lambda x: (x[0] - 1, x[1])
}

def parse_input(input_path):
    with open(input_path) as f:
        lines = f.readlines()
    grid = [['.'] * len(lines[0].strip()) for _ in range(len(lines))]
    blizzards = []

    for y in range(len(lines)):
        line = lines[y].strip()
        for x in range(len(line)):
            char = lines[y][x]
            if char == '#':
                grid[y][x] = char
            elif char in directions:
                blizzards.append((x, y, char))

    return grid, blizzards

# A new position is valid if it's in bound
# and if the blizzard is not on the same position
# and if the position is not a wall
def is_valid(new_position, grid, bliz_set):
    x, y = new_position
    is_oob = x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid)
    if is_oob or new_position in bliz_set or grid[y][x] == '#':
        return False
    return True


def move_blizzards(grid, blizzards):
    new_blizzards = []
    blizz_set = set()
    for blizzard in blizzards:
        x, y, direction = blizzard
        x, y = directions[direction]((x, y))
        if grid[y][x] == '#':
            if direction == '^':
                y = len(grid) - 2

            if direction == 'v':
                y = 1

            if direction == '>':
                x = 1

            if direction == '<':
                x = len(grid[0]) - 1
        new_blizzards.append((x, y, direction))
        blizz_set.add((x, y))
    return new_blizzards, blizz_set




def main(input_path):
    grid, blizzards = parse_input(input_path)

    init_blizzards = blizzards.copy()

    x_start, y_start = 1, 0
    x_end, y_end = len(grid[0]) - 2, len(grid) - 1

    paths = [
        [(x_start, y_start, 0)]
    ]

    has_arrived = False
    while not has_arrived:
        #print("TURN " + str(i))
        #copy_grid = deepcopy(grid)
        #for x_b, y_b, dir_b in blizzards:
        #    copy_grid[y_b][x_b] = dir_b
        #for line in copy_grid:
        #    print("".join(line))
        #print("###############")
        print(len(blizzards))
        blizzards, bliz_set = move_blizzards(grid, blizzards)
        print(len(blizzards))
        new_paths = []
        new_pos = set()
        for path in paths:
            x_last, y_last, minute = path[-1]
            minute += 1

            ## Add the decision not to move
            if (x_last, y_last) not in bliz_set and (x_last, y_last) not in new_pos:
                new_path = path + [(x_last, y_last, minute)]
                new_paths.append(new_path)
                new_pos.add((x_last, y_last))

            for direction_fun in directions.values():
                new_position = direction_fun((x_last, y_last))
                # Game over
                if new_position == (x_end, y_end):
                    return path + [(x_end, y_end, minute)], grid, init_blizzards

                if is_valid(new_position, grid, bliz_set) and new_position not in new_pos:
                    new_path = path + [(new_position[0], new_position[1], minute)]
                    new_paths.append(new_path)
                    new_pos.add(new_position)
        paths = new_paths

if __name__ == '__main__':
    path, grid, init_blizz = main("input.txt")
    print("\nResult is: ", path[-1][-1])