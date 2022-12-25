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
                x = len(grid[0]) - 2
        new_blizzards.append((x, y, direction))
        blizz_set.add((x, y))
    return new_blizzards, blizz_set




def main(input_path):
    grid, blizzards = parse_input(input_path)

    x_start, y_start = 1, 0
    x_end, y_end = len(grid[0]) - 2, len(grid) - 1

    steps = {
        '1': (x_end, y_end),
        '2': (x_start, y_start),
        '3': (x_end, y_end),
    }
    positions = {
        (x_start, y_start, 0, '1')
    }

    has_arrived = False
    while not has_arrived:
        blizzards, bliz_set = move_blizzards(grid, blizzards)
        new_pos = set()
        for pos in positions:
            x_last, y_last, minute, step = pos
            minute += 1

            ## Add the decision not to move
            if (x_last, y_last) not in bliz_set:
                new_pos.add((x_last, y_last, minute, step))

            for direction_fun in directions.values():
                new_position = direction_fun((x_last, y_last))
                # Game over
                if new_position == steps[step]:
                    if step == '3':
                        return minute
                    else:
                        next_step = str(int(step) + 1)
                        new_pos.add((new_position[0], new_position[1], minute, next_step))

                if is_valid(new_position, grid, bliz_set):
                    new_pos.add((new_position[0], new_position[1], minute, step))
        positions = new_pos

if __name__ == '__main__':
    minute = main("input.txt")
    print("\nResult is: ", minute)