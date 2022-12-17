class Rock:
    shape = [[]]
    max_y = 0
    max_x = 0
    def __init__(self, bottom_left):
        self.bottom_left = bottom_left
        self.coordinates = []
        for i in range(len(self.shape)):
            new_line = []
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == '#':
                    new_line.append((j, i))
            self.coordinates.append(new_line)

    def __str__(self):
        return "\n".join(map("".join, self.shape))


    # Get the start position of the bottom left tile
    def start_position(self):
        return self.bottom_left[0] + 2, self.bottom_left[1]


    def is_blocked_left(self, start_position, grid):
        x_new_bottom, y_new_bottom = start_position[0] - 1, start_position[1]
        x_bottom, y_bottom = self.bottom_left
        for coordinate in self.coordinates:
            point = coordinate[0]
            new_x = point[0] - x_bottom + x_new_bottom
            new_y = point[1] - y_bottom + y_new_bottom
            is_valid = self.is_point_valid(new_x, new_y, grid)
            if not is_valid:
                return not is_valid
        return False

    def is_blocked_right(self, start_position, grid):
        x_new_bottom, y_new_bottom = start_position[0] + 1, start_position[1]
        x_bottom, y_bottom = self.bottom_left
        for coordinate in self.coordinates:
            point = coordinate[-1] ## only diff with is_blocked_right
            new_x = point[0] - x_bottom + x_new_bottom
            new_y = point[1] - y_bottom + y_new_bottom
            is_valid = self.is_point_valid(new_x, new_y, grid)
            if not is_valid:
                return not is_valid
        return False

    def is_blocked_down(self, start_position, grid):
        x_new_bottom, y_new_bottom = start_position[0], start_position[1] + 1
        x_bottom, y_bottom = self.bottom_left
        for coordinate in self.coordinates:
            for x, y in coordinate: # we could optimize it to iterate over only the lowest points for each column
                new_x = x - x_bottom + x_new_bottom
                new_y = y - y_bottom + y_new_bottom
                is_valid = self.is_point_valid(new_x, new_y, grid)
                if not is_valid:
                    return not is_valid
        return False

    @staticmethod
    def is_point_valid(x, y, grid):
        return 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] == '.'


class LineHoriz(Rock):
    shape = [["#", "#", "#", "#"]]
    max_y = 1
    max_x = 4

    def __init__(self):
        super().__init__((0, 0))

class Plus(Rock):
    shape = [
        [".", "#", "."],
        ["#", "#", "#"],
        [".", "#", "."],
    ]
    max_y = 3
    max_x = 3

    def __init__(self):
        super().__init__((1, 2))


    def start_position(self):
        return 3, 2


class LShape(Rock):
    shape = [
        [".", ".", "#"],
        [".", ".", "#"],
        ["#", "#", "#"],
    ]
    max_y = 3
    max_x = 3

    def __init__(self):
        super().__init__((0, 2))

    def start_position(self):
        return 2, 2

class LineVert(Rock):
    shape = [
        ["#"],
        ["#"],
        ["#"],
        ["#"],
    ]
    max_y = 4
    max_x = 1

    def __init__(self):
        super().__init__((0, 3))


    def start_position(self):
        return 2, 3



class Square(Rock):
    shape = [
        ["#", "#"],
        ["#", "#"],
    ]
    max_y = 2
    max_x = 2

    def __init__(self):
        super().__init__((0, 1))

    def start_position(self):
        return 2, 1