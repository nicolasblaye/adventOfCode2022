import re

def parse_input_line(line):
    p = re.compile(r'\d+|-\d+')
    x_sensor, y_sensor, x_beacon, y_beacon = map(int, p.findall(line.strip()))
    return (x_sensor, y_sensor), (x_beacon, y_beacon)


def compute_distance(a, b):
    x_a, y_a = a
    x_b, y_b = b
    return abs(x_a - x_b) + abs(y_a - y_b)


def compute_x_min_max_for_y(y_current, x_sensor, remaining_distance, min_max_x_by_line, max_x, max_y):
    if max_y >= y_current >= 0:
        x_current_min = x_sensor - remaining_distance
        x_current_max = x_sensor + remaining_distance
        if x_current_min < 0:
            x_current_min = 0
        if x_current_max > max_x:
            x_current_max = max_x

        min_max_x_by_line[y_current].append((x_current_min, x_current_max))


def main(y_line):
    with open("input.txt") as f:
        lines = f.readlines()

    sensor_and_beacon = []
    for line in lines:
        sensor_and_beacon.append(parse_input_line(line))

    line_set = set()
    beacon_line_set = set()
    for sensor_coor, beacon_coor in sensor_and_beacon:
        distance = compute_distance(sensor_coor, beacon_coor)

        x_beacon, y_beacon = beacon_coor
        x_sensor, y_sensor = sensor_coor

        ## Remove beacons from possible coordinates
        if y_beacon == y_line:
            beacon_line_set.add(beacon_coor)

        distance_to_line = abs(y_line - y_sensor)
        print(sensor_coor, beacon_coor)
        print(distance_to_line, distance)
        if distance_to_line <= distance:
            min_x = x_sensor - (distance - distance_to_line)
            max_x = x_sensor + (distance - distance_to_line)
            print(min_x, max_x, x_sensor, distance, distance_to_line)
            for i in range(min_x, max_x+1):
                line_set.add((i, y_line))

    #print(sorted(list(line_set)))
    #print(sorted(list(beacon_line_set)))

    count = 0
    for coor in line_set:
        if coor not in beacon_line_set:
            count += 1
    return count


def main2(max_x, max_y):
    with open("input.txt") as f:
        lines = f.readlines()

    sensor_and_beacon = []
    for line in lines:
        sensor_and_beacon.append(parse_input_line(line))

    min_max_x_by_line = [[] for _ in range(max_y+1)]

    for sensor_coor, beacon_coor in sensor_and_beacon:
        distance = compute_distance(sensor_coor, beacon_coor)

        x_sensor, y_sensor = sensor_coor

        for i in range(distance):
            y_current_up = y_sensor + i
            y_current_down = y_sensor - i

            remaining_distance = distance - i
            compute_x_min_max_for_y(y_current_down, x_sensor, remaining_distance, min_max_x_by_line, max_x, max_y)
            compute_x_min_max_for_y(y_current_up, x_sensor, remaining_distance, min_max_x_by_line, max_x, max_y)

    not_done = True
    y = 0
    x = 0
    while not_done:
        line = min_max_x_by_line[y]
        sorted_list = sorted(line, key=lambda q: q[0])
        #print(sorted_list)
        current_min = sorted_list[0][0]
        if current_min > 0:
            x = 0
            return x, y
        current_max = sorted_list[0][1]
        for x_min, x_max in sorted_list[1:]:
            if x_min > current_max:
                x = x_min - 1
                return x, y
            current_max = max(current_max, x_max)
        y += 1
    return x,y




if __name__ == '__main__':
    x, y = main2(4000000, 4000000)
    print(x * 4000000 + y)
