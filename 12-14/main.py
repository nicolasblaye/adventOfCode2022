def sand_can_rest(x, y, grid):
    if x == 0 or y == len(grid)-1 or grid[y][x] == 'o':
        return False

    # down, down left and down right are filled
    if grid[y+1][x-1] != '.' and grid[y+1][x+1] != '.' and grid[y+1][x] != '.':
        return True

    return False


def sand_is_blocked_left(x, y, grid):
    return x != 0 and (grid[y+1][x-1] != '.')


def sand_is_blocked_right(x, y, grid):
    return x != len(grid[y])-1 and (grid[y+1][x+1] != '.')


def sand_is_blocked_down(x, y, grid):
    return y != len(grid)-1 and (grid[y+1][x] != '.')


def sand_rest_coordinates(x, y, grid, sand_path):
    if x == 0 or y == len(grid) - 1:
        return None

    if sand_can_rest(x, y, grid):
        return x, y
    # try down
    elif not sand_is_blocked_down(x, y, grid):
        sand_path.append((x, y+1))
        if sand_can_rest(x, y+1, grid):
            return x, y+1
        else:
            return sand_rest_coordinates(x, y + 1, grid, sand_path)
    # try down left
    elif not sand_is_blocked_left(x, y, grid):
        sand_path.append((x-1, y+1))
        if sand_can_rest(x-1, y+1, grid):
            return x-1, y+1
        else:
            return sand_rest_coordinates(x - 1, y + 1, grid, sand_path)
    # try down right
    elif not sand_is_blocked_right(x, y, grid):
        sand_path.append((x+1, y+1))
        if sand_can_rest(x+1, y+1, grid):
            return x+1, y+1
        else:
            return sand_rest_coordinates(x + 1, y + 1, grid, sand_path)
    else:
        # return one step above the first one
        if len(sand_path) > 0:
            x, y = sand_path.pop(-1)
            return sand_rest_coordinates(x, y, grid, sand_path)
        else:
            return None


def main():
    with open("input.txt") as f:
        lines = f.readlines()
        # sand starts at 500
        min_x, min_y, max_x, max_y = 1000000, 1000000, 500, 0
        rocks_coordinates = []
        for line in lines:
            splits = line.strip().split(" -> ")
            for i in range(0, len(splits)-1):
                start_x, start_y = map(int, splits[i].strip().split(","))
                end_x, end_y = map(int, splits[i+1].strip().split(','))

                if max_x < start_x:
                    max_x = start_x
                if min_x > end_x:
                    min_x = end_x

                if max_x < end_x:
                    max_x = end_x
                if min_x > start_x:
                    min_x = start_x

                if max_y < end_y:
                    max_y = end_y
                if min_y > start_y:
                    min_y = start_y

                if max_y < start_y:
                    max_y = start_y
                if min_y > end_y:
                    min_y = end_y
                # left line
                if start_x - end_x > 0:
                    for j in range(0, abs(start_x - end_x) + 1):
                        rocks_coordinates.append((start_x - j, start_y))

                # right line
                if start_x - end_x < 0:
                    for j in range(0, abs(start_x - end_x) + 1):
                        rocks_coordinates.append((start_x + j, start_y))

                # up line
                if start_y - end_y < 0:
                    for j in range(0, abs(start_y - end_y) + 1):
                        rocks_coordinates.append((start_x, start_y + j))

                # down line
                if start_y - end_y > 0:
                    for j in range(0, start_y - end_y + 1):
                        rocks_coordinates.append((start_x, start_y - j))

        grid = [['.'] * (max_x+1) for _ in range(max_y+1)]
        for rock in rocks_coordinates:
            x, y = rock
            grid[y][x] = '#'

        sand = 0
        sand_can_rest_bool = True
        sand_path = []
        while sand_can_rest_bool:
            if (len(sand_path)) > 1:
                x_start, y_start = sand_path[-2]
            else:
                x_start, y_start = (500, 0)
            possible_sand_coordinates = sand_rest_coordinates(x_start, y_start, grid, sand_path)
            if possible_sand_coordinates is None:
                sand_can_rest_bool = False
            else:
                x, y = possible_sand_coordinates
                grid[y][x] = 'o'
                sand += 1

        return sand


def main2():
    with open("input.txt") as f:
        lines = f.readlines()
        # sand starts at 500
        min_x, min_y, max_x, max_y = 1000000, 1000000, 500, 0
        rocks_coordinates = []
        for line in lines:
            splits = line.strip().split(" -> ")
            for i in range(0, len(splits)-1):
                start_x, start_y = map(int, splits[i].strip().split(","))
                end_x, end_y = map(int, splits[i+1].strip().split(','))

                if max_x < start_x:
                    max_x = start_x
                if min_x > end_x:
                    min_x = end_x

                if max_x < end_x:
                    max_x = end_x
                if min_x > start_x:
                    min_x = start_x

                if max_y < end_y:
                    max_y = end_y
                if min_y > start_y:
                    min_y = start_y

                if max_y < start_y:
                    max_y = start_y
                if min_y > end_y:
                    min_y = end_y
                # left line
                if start_x - end_x > 0:
                    for j in range(0, abs(start_x - end_x) + 1):
                        rocks_coordinates.append((start_x - j, start_y))

                # right line
                if start_x - end_x < 0:
                    for j in range(0, abs(start_x - end_x) + 1):
                        rocks_coordinates.append((start_x + j, start_y))

                # up line
                if start_y - end_y < 0:
                    for j in range(0, abs(start_y - end_y) + 1):
                        rocks_coordinates.append((start_x, start_y + j))

                # down line
                if start_y - end_y > 0:
                    for j in range(0, start_y - end_y + 1):
                        rocks_coordinates.append((start_x, start_y - j))

        enlargement = 2
        grid = [['.'] * (enlargement*max_x+1) for _ in range(max_y+1)]
        for rock in rocks_coordinates:
            x, y = rock
            grid[y][x] = '#'

        grid.append(['.'] * (enlargement*max_x+1))
        grid.append(['#'] * (enlargement*max_x+1))

        sand = 0
        sand_can_rest_bool = True
        sand_path = [(500, 0)]
        while sand_can_rest_bool:
            if (len(sand_path)) > 1:
                x_start, y_start = sand_path[-2]
            else:
                x_start, y_start = (500, 0)
            possible_sand_coordinates = sand_rest_coordinates(x_start, y_start, grid, sand_path)
            if possible_sand_coordinates is None:
                sand_can_rest_bool = False
            else:
                x, y = possible_sand_coordinates
                grid[y][x] = 'o'
                sand += 1
        for line in grid:
            print(line[489:])
        return sand


if __name__ == '__main__':
    print(main2())
