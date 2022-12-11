def main():
    with(open("input.txt", encoding='utf-8')) as f:
        cycle = 1
        x = 1
        values = []
        for line in f.readlines():
            line = line.strip()
            splits = line.split(" ")
            if splits[0] == 'noop':
                cycle += 1
                if cycle in [20, 60, 100, 140, 180, 220]:
                    values.append(x * cycle)
            else:
                cycle += 1
                if cycle in [20, 60, 100, 140, 180, 220]:
                    values.append(x * cycle)
                cycle += 1
                x += int(splits[1])
                if cycle in [20, 60, 100, 140, 180, 220]:
                    values.append(x * cycle)
        return sum(values)


def draw_pixel(cycle, x, lines):
    position = cycle - 1
    pixel = ' '
    if position % 40 in [x-1, x, x+1]:
        pixel = '#'

    current_line = lines[-1]

    if len(current_line) == 40:
        lines.append([pixel])
    else:
        current_line.append(pixel)


def main2():
    with(open("input.txt", encoding='utf-8')) as f:
        cycle = 1
        x = 1
        lines = [[]]
        for line in f.readlines():
            draw_pixel(cycle, x, lines)
            line = line.strip()
            splits = line.split(" ")
            if splits[0] == 'noop':
                cycle += 1
            else:
                cycle += 1
                draw_pixel(cycle, x, lines)
                cycle += 1
                x += int(splits[1])
        return lines


if __name__ == '__main__':
    for result in main2():
        print("".join(result))
