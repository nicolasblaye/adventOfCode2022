def main():
    with open("input.txt") as f:
        lines = f.readlines()
        grid = []
        start_point = 0,0
        end_point = 0,0
        y = 0
        for line in lines:
            vector = []
            x = 0
            for char in line.strip():
                if char == 'S':
                    start_point = x, y
                    vector.append('a')
                elif char == 'E':
                    end_point = x, y
                    vector.append('z')
                else:
                    vector.append(char)
                x += 1
            grid.append(vector)
            y += 1

        for line in grid:
            print(line)
        reached = False
        current_points = [start_point]
        max_x = len(grid[0])
        max_y = len(grid)
        visited = {start_point}
        iteration = 1
        while not reached:
            new_current_points = []
            for x, y in current_points:
                neighboors = []
                if x > 0:
                    left = x-1, y
                    neighboors.append(left)
                if x < max_x - 1:
                    right = x+1, y
                    neighboors.append(right)
                if y > 0:
                    up = x, y-1
                    neighboors.append(up)
                if y < max_y - 1:
                    down = x, y+1
                    neighboors.append(down)
                for neighboor in neighboors:
                    x_n, y_n = neighboor
                    if neighboor not in visited and ord(grid[y_n][x_n]) - ord(grid[y][x]) < 2:
                        if neighboor == end_point:
                            return iteration
                        visited.add(neighboor)
                        new_current_points.append(neighboor)
            current_points = new_current_points
            iteration += 1


def main2():
    with open("input.txt") as f:
        lines = f.readlines()
        grid = []
        start_points = []
        end_point = 0, 0
        y = 0
        for line in lines:
            vector = []
            x = 0
            for char in line.strip():
                if char == 'S' or char == 'a':
                    start_points.append((x, y))
                    vector.append('a')
                elif char == 'E':
                    end_point = x, y
                    vector.append('z')
                else:
                    vector.append(char)
                x += 1
            grid.append(vector)
            y += 1

        for line in grid:
            print(line)
        reached = False
        current_points = start_points
        max_x = len(grid[0])
        max_y = len(grid)
        visited = set(start_points)
        iteration = 1
        while not reached:
            new_current_points = []
            for x, y in current_points:
                neighboors = []
                if x > 0:
                    left = x-1, y
                    neighboors.append(left)
                if x < max_x - 1:
                    right = x+1, y
                    neighboors.append(right)
                if y > 0:
                    up = x, y-1
                    neighboors.append(up)
                if y < max_y - 1:
                    down = x, y+1
                    neighboors.append(down)
                for neighboor in neighboors:
                    x_n, y_n = neighboor
                    if neighboor not in visited and ord(grid[y_n][x_n]) - ord(grid[y][x]) < 2:
                        if neighboor == end_point:
                            return iteration
                        visited.add(neighboor)
                        new_current_points.append(neighboor)
            current_points = new_current_points
            iteration += 1


if __name__ == '__main__':
    print(main2())
