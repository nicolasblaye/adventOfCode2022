def parse_input(input_path, nb_line_to_add):
    with open(input_path) as f:
        lines = f.readlines()

    grid = [['.'] * (len(lines[0]) + 2*nb_line_to_add) for _ in range(nb_line_to_add)]
    elfs = []
    j = nb_line_to_add
    for line in lines:
        grid.append(['.'] * (len(lines[0]) + 2*nb_line_to_add))
        i = nb_line_to_add
        for char in line.strip():
            if char == '#':
                elfs.append((i, j))
            grid[j][i] = char
            i += 1
        j += 1
    grid.extend(['.'] * (len(lines[0]) + 2 * nb_line_to_add) for _ in range(nb_line_to_add))
    return grid, elfs


def should_move(x, y, grid):
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if grid[j][i] == '#' and (x, y) != (i, j):
                return True
    return False

directions = ['N', 'S', 'W', 'E']

def first_round(grid, elfs, offset):
    next_elfs = {}
    i = 0
    should_move_count = 0
    for x, y in elfs:
        if should_move(x, y, grid):
            should_move_count += 1
            for j in range(len(directions)):
                direction = directions[(offset + j) % len(directions)]
                if direction == 'N':
                    # if N is possible (y > 0 and == .) and if NE/NW are either out of the map, or does not contain an elf
                    if y > 0 and (x-1 == -1 or grid[y-1][x-1] == '.') and grid[y-1][x] == '.' and (x+1 == len(grid[y]) or grid[y-1][x+1] == '.'):
                        new_coord = (x, y - 1)
                        if new_coord not in next_elfs:
                            next_elfs[new_coord] = (0, i)
                        count, index = next_elfs[new_coord]
                        next_elfs[new_coord] = count + 1, index
                        break

                if direction == 'S':
                    # if S is possible (y < len(grid) and == .) and if SE/SW are either out of the map, or does not contain an elf
                    if y < len(grid) and (x-1 == -1 or grid[y+1][x-1] == '.') and grid[y+1][x] == '.' and (x+1 == len(grid[y]) or grid[y+1][x+1] == '.'):
                        new_coord = (x, y + 1)
                        if new_coord not in next_elfs:
                            next_elfs[new_coord] = (0, i)
                        count, index = next_elfs[new_coord]
                        next_elfs[new_coord] = count + 1, index
                        break


                if direction == 'W':
                    # if W is possible (x > 0 and == .) and if WS/WN are either out of the map, or does not contain an elf
                    if x > 0 and (y-1 == -1 or grid[y-1][x-1] == '.') and grid[y][x-1] == '.' and (y+1 == len(grid) or grid[y+1][x-1] == '.'):
                        new_coord = (x - 1, y)
                        if new_coord not in next_elfs:
                            next_elfs[new_coord] = (0, i)
                        count, index = next_elfs[new_coord]
                        next_elfs[new_coord] = count + 1, index
                        break


                if direction == 'E':
                    # if W is possible (x < len(grid[y]) and == .) and if ES/EN are either out of the map, or does not contain an elf
                    if x < len(grid[y]) and (y-1 == -1 or grid[y-1][x+1] == '.') and grid[y][x+1] == '.' and (y+1 == len(grid) or grid[y+1][x+1] == '.'):
                        new_coord = (x + 1, y)
                        if new_coord not in next_elfs:
                            next_elfs[new_coord] = (0, i)
                        count, index = next_elfs[new_coord]
                        next_elfs[new_coord] = count + 1, index
                        break
        i += 1
    return next_elfs, should_move_count


def second_round(grid, previous_elfs, next_elfs):
    real_next_elf = previous_elfs.copy()

    for key, value in next_elfs.items():
        new_x, new_y = key
        count, index = value

        if count == 1:
            old_x, old_y = previous_elfs[index]
            grid[new_y][new_x] = '#'
            grid[old_y][old_x] = '.'
            real_next_elf[index] = (new_x, new_y)

    return grid, real_next_elf


def main(input_path, moves):
    grid, elfs = parse_input(input_path, moves)
    #for line in grid:
    #    print("".join(line))
    #print("################\n")
    for i in range(moves):
        #print("Start of Round: " + str(i+1))
        next_elfs, should_move_count = first_round(grid, elfs, i)
        if should_move_count == 0:
            print("Start of Round: " + str(i + 1))
            break
        grid, elfs = second_round(grid, elfs, next_elfs)

        #for line in grid:
            #print("".join(line))
        #print("################")

    min_x = 1000
    max_x = 0
    min_y = 1000
    max_y = 0
    for x, y in elfs:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    result = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elfs)

    return result

if __name__ == '__main__':
    print(main("input.txt", 1000))