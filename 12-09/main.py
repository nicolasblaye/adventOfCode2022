def move_head(direction, xH, yH):
    # MOVE H
    if direction == 'R':
        xH += 1

    if direction == 'L':
        xH -= 1

    if direction == 'U':
        yH -= 1

    if direction == 'D':
        yH += 1

    return xH, yH


def move_tail(xH, yH, xT, yT):
    # Move T according to previous note H

    # Motion to follow a node
    # If the previous node is 2 diagonals ahead
    if abs(xH - xT) >= 2 and abs(yH - yT) >= 2:
        # T is down right from H
        xT += (xH - xT) / 2
        yT += (yH - yT) / 2

    # Motion to follow the head
    # Only move T if there are more than two spaces for any dimension
    elif abs(xH - xT) >= 2 or abs(yH - yT) >= 2:
        # T is left from H
        if xH - xT == 2:
            xT = xH - 1
            yT = yH

        # T is up from H
        if yH - yT == 2:
            yT = yH - 1
            xT = xH

        # T is right from H
        if xH - xT == -2:
            xT = xH + 1
            yT = yH

        # T is down from H
        if yH - yT == -2:
            yT = yH + 1
            xT = xH

    return xT, yT


def main():
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        xH, yH, xT, yT = 0, 0, 0, 0
        set = {(0, 0)}
        for line in lines:
            line = line.strip()
            splits = line.split()
            direction = splits[0]
            moves = int(splits[1])

            for i in range(moves):
                xH, yH = move_head(direction, xH, yH)
                xT, yT = move_tail(xH, yH, xT, yT)
                set.add((xT, yT))
    return len(set)


def main2():
    snake_length = 10

    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        node_coordinates = [(0, 0)] * snake_length
        unique_point_tail = {(0, 0)}
        for line in lines:
            line = line.strip()
            splits = line.split()
            direction = splits[0]
            moves = int(splits[1])

            for _ in range(moves):
                node_coordinates[0] = move_head(direction, node_coordinates[0][0], node_coordinates[0][1])

                for i in range(1, len(node_coordinates)):
                    node_coordinates[i] = move_tail(node_coordinates[i-1][0], node_coordinates[i-1][1], node_coordinates[i][0], node_coordinates[i][1])

                unique_point_tail.add(node_coordinates[-1])
    return len(unique_point_tail)


if __name__ == '__main__':
    print(main2())
