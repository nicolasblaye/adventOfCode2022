def parse_input(input_path):
    with open(input_path) as f:
        lines = f.readlines()

    max_x = len(lines[0])-1
    max_y = len(lines)-2
    indexes_by_line = [(0, 0)] * max_y
    indexes_by_column = [(1000, 0)] * max_x

    grid = [[' '] * max_x for _ in range(max_y)]
    for j in range(len(lines)-2):
        line = lines[j]
        if len(line) - 1 > max_x:
            for x_line in grid:
                x_line.extend([' '] * (len(line) - max_x - 1))
                indexes_by_column.extend([(1000, 0)] * (len(line) - max_x - 1))
            max_x = len(line) - 1
        index_min_x = 1000
        index_max_x = 0
        for i in range(len(line)-1):
            char = line[i]
            if char != ' ':
                index_min_x = min(index_min_x, i)
                index_max_x = max(index_max_x, i)
                index_min_y = min(j, indexes_by_column[i][0])
                index_max_y = max(j, indexes_by_column[i][1])
                indexes_by_column[i] = (index_min_y, index_max_y)
            grid[j][i] = char
        indexes_by_line[j]  = (index_min_x, index_max_x)

    move_line = lines[-1]
    acc = []
    moves = []
    for char in move_line:
        is_number = char.isnumeric()
        if not is_number:
            moves.append(int("".join(acc)))
            moves.append(char)
            acc = []
        else:
            acc.append(char)
    if acc:
        moves.append(int("".join(acc)))

    return grid, indexes_by_line, indexes_by_column, moves


def parse_input_tailored(input_path):
    with open(input_path) as f:
        lines = f.readlines()

    face_A = [['.'] * 50 for _ in range(50)]
    face_B = [['.'] * 50 for _ in range(50)]
    face_C = [['.'] * 50 for _ in range(50)]
    face_D = [['.'] * 50 for _ in range(50)]
    face_E = [['.'] * 50 for _ in range(50)]
    face_F = [['.'] * 50 for _ in range(50)]

    for j in range(50):
        for i in range(50):
            face_A[j][i] = lines[j][i+50]
            face_B[j][i] = lines[j][i+100]
            face_C[j][i] = lines[j+50][i+50]
            face_D[j][i] = lines[j+100][i]
            face_E[j][i] = lines[j+100][i+50]
            face_F[j][i] = lines[j+150][i]

    cube = {
        'A' : face_A,
        'B' : face_B,
        'C' : face_C,
        'D' : face_D,
        'E' : face_E,
        'F' : face_F
    }

    move_line = lines[-1]
    acc = []
    moves = []
    for char in move_line:
        is_number = char.isnumeric()
        if not is_number:
            moves.append(int("".join(acc)))
            moves.append(char)
            acc = []
        else:
            acc.append(char)
    if acc:
        moves.append(int("".join(acc)))

    return cube, moves


def rotate(facing, move):
    if facing == 'R':
        if move == 'R':
            return 'D'
        else:
            return 'U'
    if facing == 'D':
        if move == 'R':
            return 'L'
        else:
            return 'R'
    if facing == 'L':
        if move == 'R':
            return 'U'
        else:
            return 'D'
    if facing == 'U':
        if move == 'R':
            return 'R'
        else:
            return 'L'

def compute_next_position(row, column, facing, indexes_by_line, index_by_column):
    if facing == 'R':
        next_row, next_column = row, column + 1
        if next_column > indexes_by_line[next_row][1]:
            next_column = indexes_by_line[next_row][0]
        return next_row, next_column

    if facing == 'L':
        next_row, next_column = row, column - 1
        if next_column < indexes_by_line[next_row][0]:
            next_column = indexes_by_line[next_row][1]
        return next_row, next_column

    # need y index
    if facing == 'D':
        next_row, next_column = row + 1, column
        if next_row > index_by_column[next_column][1]:
            next_row = index_by_column[next_column][0]
        return next_row, next_column

    if facing == 'U':
        next_row, next_column = row - 1, column
        if next_row < index_by_column[next_column][0]:
            next_row = index_by_column[next_column][1]
        return next_row, next_column


def compute_next_position(row, column, facing, indexes_by_line, index_by_column):
    if facing == 'R':
        next_row, next_column = row, column + 1
        if next_column > indexes_by_line[next_row][1]:
            next_column = indexes_by_line[next_row][0]
        return next_row, next_column

    if facing == 'L':
        next_row, next_column = row, column - 1
        if next_column < indexes_by_line[next_row][0]:
            next_column = indexes_by_line[next_row][1]
        return next_row, next_column

    # need y index
    if facing == 'D':
        next_row, next_column = row + 1, column
        if next_row > index_by_column[next_column][1]:
            next_row = index_by_column[next_column][0]
        return next_row, next_column

    if facing == 'U':
        next_row, next_column = row - 1, column
        if next_row < index_by_column[next_column][0]:
            next_row = index_by_column[next_column][1]
        return next_row, next_column

def compute_move(move, facing, start_row, start_column, grid, indexes_by_line, index_by_column):
    cur_row, cur_column = start_row, start_column
    for i in range(move):
        row, column = compute_next_position(cur_row, cur_column, facing, indexes_by_line, index_by_column)
        if grid[row][column] == '.':
            cur_row, cur_column = row, column
        else:
            break
    return cur_row, cur_column

def compute_moves(grid, indexes_by_line, index_by_column, moves):
    facing = 'R'
    row = 0
    column = indexes_by_line[row][0]
    for move in moves:
        if type(move) == int:
            row, column = compute_move(move, facing, row, column, grid, indexes_by_line, index_by_column)
        else:
            facing = rotate(facing, move)
    return row, column, facing


def main(input_path):
    facing_score = {'R' : 0, 'D': 1, 'L': 2, 'U': 3}
    grid, indexes_by_line, index_by_column, moves = parse_input(input_path)
    row, column, facing = compute_moves(grid, indexes_by_line, index_by_column, moves)
    return 1000 * (row + 1) + 4 * (column + 1) + facing_score[facing]

def compute_next_position_cub(row, column, facing, cube_face, mapping):
    if facing == 'R':
        next_row, next_column = row, column + 1
        if next_column > 49:
            print(f"Changing cube face from {cube_face + 'R'} {row} {column}")
            cube_face, facing, new_coord_fun = mapping[cube_face + 'R']
            next_column, next_row = new_coord_fun((column, row))
            print(f"To {cube_face + facing} {next_row} {next_column}")
        return next_row, next_column, facing, cube_face

    if facing == 'L':
        next_row, next_column = row, column - 1
        if next_column < 0:
            print(f"Changing cube face from {cube_face + facing} {row} {column}")
            cube_face, facing, new_coord_fun = mapping[cube_face + 'L']
            next_column, next_row = new_coord_fun([row, column])
            print(f"To {cube_face + facing} {next_row} {next_column}")
        return next_row, next_column, facing, cube_face

    if facing == 'D':
        next_row, next_column = row + 1, column
        if next_row > 49:
            print(f"Changing cube face from {cube_face + facing} {row} {column}")
            cube_face, facing, new_coord_fun = mapping[cube_face + 'D']
            next_column, next_row = new_coord_fun((column, row))
            print(f"To {cube_face + facing} {next_row} {next_column}")
        return next_row, next_column, facing, cube_face

    if facing == 'U':
        next_row, next_column = row - 1, column
        if next_row < 0:
            print(f"Changing cube face from {cube_face + facing} {row} {column}")
            cube_face, facing, new_coord_fun = mapping[cube_face + 'U']
            next_column, next_row = new_coord_fun((column, row))
            print(f"To {cube_face + facing} {next_row} {next_column}")
        return next_row, next_column, facing, cube_face


def compute_move_cube(move, row, column, facing, cube_face, cube, mapping):
    cur_row, cur_column = row, column
    for i in range(move):
        row, column, facing, cube_face = compute_next_position_cub(cur_row, cur_column, facing, cube_face, mapping)
        if cube[cube_face][row][column] == '.':
            cur_row, cur_column, facing, cube_face = row, column, facing, cube_face
        else:
            break
    return cur_row, cur_column, facing, cube_face


def compute_moves_cube(cube, mapping, moves):
    facing = 'R'
    row = 0
    column = 0
    cube_face = 'A'
    for move in moves:
        print(move)
        print(row, column, facing, cube_face)
        if type(move) == int:
            row, column, facing, cube_face = compute_move_cube(move, row, column, facing, cube_face, cube, mapping)
        else:
            facing = rotate(facing, move)
        print(row, column, facing, cube_face)
        print("###### MOVE DONE #############")
    return row, column, facing, cube_face


## Main is tailored to the input
def main2():
    cube, moves = parse_input_tailored("input.txt")

    # With a face and a direction, gives the next face, direction
    # and a function to compute next coordinates given the current ones
    mapping = {
        'AU' : ('F', 'R', lambda x: (0, x[0])),
        'AR' : ('B', 'R', lambda x: (0, x[1])),
        'AD' : ('C', 'D', lambda x: (x[0], 0)),
        'AL' : ('D', 'R', lambda x: (0, 49 - x[1])),

        'BU': ('F', 'U', lambda x: (x[0], 49)),
        'BR': ('E', 'L', lambda x: (49, 49 - x[1])),
        'BD': ('C', 'D', lambda x: (x[0], 0)),
        'BL': ('D', 'R', lambda x: (0, 49 - x[0])),

        'CU': ('A', 'U', lambda x: (x[0], 49)),
        'CR': ('B', 'U', lambda x: (x[1], 49)),
        'CD': ('E', 'D', lambda x: (x[0], 0)),
        'CL': ('D', 'D', lambda x: (x[1], 0)),

        'DU': ('C', 'R', lambda x: (0, x[0])),
        'DR': ('E', 'R', lambda x: (0, x[1])),
        'DD': ('F', 'D', lambda x: (x[0], 0)),
        'DL': ('A', 'R', lambda x: (0, 49 - x[1])),

        'EU': ('C', 'U', lambda x: (x[0], 49)),
        'ER': ('B', 'L', lambda x: (49, 49-x[1])),
        'ED': ('F', 'L', lambda x: (49, x[0])),
        'EL': ('D', 'L', lambda x: (49, x[1])),

        'FU': ('D', 'U', lambda x: (x[0], 49)),
        'FR': ('E', 'U', lambda x: (x[1], 49)),
        'FD': ('B', 'D', lambda x: (x[0], 0)),
        'FL': ('A', 'D', lambda x: (x[1], 0))
    }

    row, column, facing, cube_face = compute_moves_cube(cube, mapping, moves)
    facing_score = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    print(row, column, facing, cube_face)
    if cube_face == 'C':
        return 1000 * (row + 51) + 4 * (column + 51) + facing_score[facing]
    elif cube_face == 'A':
        return 1000 * (row + 1) + 4 * (column + 51) + facing_score[facing]
    elif cube_face == 'D':
        return 1000 * (row + 101) + 4 * (column + 1) + facing_score[facing]
    return row, column, facing, cube_face


if __name__ == '__main__':
    print(main2())