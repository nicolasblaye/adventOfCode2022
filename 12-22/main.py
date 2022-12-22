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


def compute_next_position_in_cube(row, column, facing, indexes_by_line, index_by_column):
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

if __name__ == '__main__':
    result = main("input.txt")
    print(result)
