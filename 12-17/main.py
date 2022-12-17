from  rock import LineHoriz, LShape, LineVert, Square, Plus

def parse_input(path):
    with open(path) as f:
        line = f.readline().strip()
    pattern = []
    for char in line:
        pattern.append(char)
    return pattern


# start_position is the position of the bottom left
def rock_fall(rock, patterns, grid, index_pattern):
    start_position = rock.start_position()
    blocked = False
    max_y = len(grid)
    while not blocked:
        pattern = patterns[index_pattern % len(patterns)]
        if pattern == '>' and not rock.is_blocked_right(start_position, grid):
            start_position = start_position[0] + 1, start_position[1]
        elif pattern == '<' and not rock.is_blocked_left(start_position, grid):
            start_position = start_position[0] - 1, start_position[1]
        if rock.is_blocked_down(start_position, grid):
            blocked = True
            for j in range(len(rock.coordinates)):
                for i in range(len(rock.coordinates[j])):
                    x, y = rock.coordinates[j][i]
                    x_grid = x - rock.bottom_left[0] + start_position[0]
                    y_grid = y - rock.bottom_left[1] + start_position[1]
                    if y_grid < max_y:
                        max_y = y_grid
                    grid[y_grid][x_grid] = '#'
        else:
            start_position = start_position[0], start_position[1] + 1
        index_pattern += 1
    return max_y, index_pattern


def compute_cycle(input_path):
    patterns = parse_input(input_path)

    rocks = [LineHoriz(), Plus(), LShape(), LineVert(), Square()]

    grid = [(["."] * 7) for _ in range(4)]

    # max_y is the highest part of a rock, grid is the highest at len(grid)-1
    # starts at len(grid) since it's the ground
    current_max_y = len(grid)
    index_pattern = 0
    index_rock = 0
    store_pairs = {}
    nb_rocks = 0
    while True:
        rock = rocks[index_rock]
        number_of_line_to_add = rock.max_y + 3 - current_max_y

        if number_of_line_to_add < 0:
            for _ in range(0, abs(number_of_line_to_add)):
                grid.pop(0)
        else:
            for _ in range(number_of_line_to_add):
                grid.insert(0, (["."] * 7))

        current_max_y += number_of_line_to_add

        max_y, index_pattern = rock_fall(rock, patterns, grid, index_pattern)
        current_max_y = min(max_y, current_max_y)
        pair = ((index_pattern - 1) % len(patterns), index_rock)
        height = len(grid) - current_max_y
        if pair not in store_pairs:
            store_pairs[pair] = [(height, nb_rocks)]
        else:
            store_pairs[pair].append((height, nb_rocks))
            last_rock_diff = store_pairs[pair][-1][1] - store_pairs[pair][-2][1]
            last_height_diff = store_pairs[pair][-1][0] - store_pairs[pair][-2][0]
            is_same = True
            for j in range(len(store_pairs[pair]) - 1):
                diff = store_pairs[pair][j + 1][1] - store_pairs[pair][j][1]
                diff_height = store_pairs[pair][j + 1][0] - store_pairs[pair][j][0]
                if last_rock_diff != diff or diff_height != last_height_diff:
                    is_same = False
                    break
            if is_same and len(store_pairs[pair]) > 2:
                return last_rock_diff, last_height_diff

        index_pattern = index_pattern % len(patterns)

        index_rock = (index_rock + 1) % len(rocks)
        nb_rocks += 1


def main(input_path, number_of_rocks):
    cycle, height_by_cycle = compute_cycle(input_path)
    patterns = parse_input(input_path)

    current_height = int(number_of_rocks / cycle) * height_by_cycle
    remaining_cycles = number_of_rocks % cycle

    rocks = [LineHoriz(), Plus(), LShape(), LineVert(), Square()]

    grid =  [(["."] * 7) for _ in range(4)]

    # max_y is the highest part of a rock, grid is the highest at len(grid)-1
    # starts at len(grid) since it's the ground
    current_max_y = len(grid)
    index_pattern = 0
    index_rock = 0
    for i in range(remaining_cycles):
        if index_pattern == 0 and index_rock == 0 and current_max_y < len(grid):
            print(grid[current_max_y])
        rock = rocks[index_rock]
        number_of_line_to_add = rock.max_y + 3 - current_max_y


        if number_of_line_to_add < 0:
            for _ in range(0, abs(number_of_line_to_add)):
                grid.pop(0)
        else:
            for _ in range(number_of_line_to_add):
                grid.insert(0, (["."] * 7))


        current_max_y += number_of_line_to_add

        max_y, index_pattern = rock_fall(rock, patterns, grid, index_pattern)
        current_max_y = min(max_y, current_max_y)

        index_pattern = index_pattern % len(patterns)

        index_rock = (index_rock + 1) % len(rocks)

    return (len(grid) - current_max_y) + current_height


if __name__ == '__main__':
    print(main("input.txt", 1000000000000))
