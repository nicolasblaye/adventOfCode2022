import re
import time


class Valve:
    opened = False

    def __init__(self, name, flow_rate, children):
        self.name = name
        self.flow_rate = flow_rate
        self.children = children

    def is_useful(self):
        return self.flow_rate > 0

    def __str__(self):
        return f"{self.name} : {self.flow_rate} : {self.children}"


def distance_from_start_to_all_valve_rec(children, valves, distance, visited, current_distance):
    next_children = []
    for child in children:
        if child not in visited:
            visited.add(child)
            distance[child] = current_distance
            valve = valves[child]
            next_children.extend(valve.children)
    if next_children:
        return distance_from_start_to_all_valve_rec(next_children, valves, distance, visited, current_distance + 1)
    else:
        return distance


def distance_from_start_to_all_valve(start_valve, valves):
    current_distance = 0
    distance = {start_valve.name: 0}
    visited = set()
    visited.add(start_valve.name)
    return distance_from_start_to_all_valve_rec(start_valve.children, valves, distance, visited, current_distance + 1)


def compute_distance(useful_valves, valves):
    distances = {}
    for valve in useful_valves:
        distance = distance_from_start_to_all_valve(valve, valves)
        distances[valve.name] = distance
    return distances


def parse_input_line(line):
    p = re.compile(r'Valve (\w+) has flow rate=(\d+); tunne(l|ls) lea(ds|d) to valv(es|e) (.*)')
    matches = p.match(line)
    valve = matches.group(1)
    flow_rate = int(matches.group(2))
    children = matches.group(6).strip().split(", ")
    return Valve(valve, flow_rate, children)


def compute_potential_flow_rate(distance, valves, minutes_left):
    potential_flow_rate_by_valve = {}
    for valve_name, d in distance.items():
        valve = valves[valve_name]
        flow_rate = valve.flow_rate * (minutes_left - d - 1)
        potential_flow_rate_by_valve[valve_name] = flow_rate
    return potential_flow_rate_by_valve


def release_pressure_rec(valve, valves, minutes_left, opened, visited):
    if minutes_left < 2 or valve.name in visited:
        return 0
    # print(minutes_left)
    # print(valve)
    new_visited = visited.copy()
    new_visited.add(valve.name)
    flow_rates = []
    ### We do not open it
    for child in valve.children:
        valve_child = valves[child]
        flow_rate = release_pressure_rec(valve_child, valves, minutes_left - 1, opened.copy(), new_visited)
        flow_rates.append(flow_rate)

    if valve.flow_rate > 0 and valve.name not in opened:
        new_opened = opened.copy()
        new_opened.add(valve.name)
        flow_rate = (minutes_left - 1) * valve.flow_rate
        for child in valve.children:
            valve_child = valves[child]
            child_flow_rate = release_pressure_rec(valve_child, valves, minutes_left - 2, new_opened, set()) + flow_rate
            flow_rates.append(child_flow_rate)

    return max(flow_rates)


def release_pressure_useful_rec(valve, valves, minutes_left, opened, distances, useful_valves):
    if minutes_left < 2:
        return 0
    flow_rates = []

    new_opened = opened.copy()
    if valve.flow_rate > 0:
        new_opened.add(valve.name)
        minutes_left -= 1
        flow_rate = minutes_left * valve.flow_rate
    else:
        flow_rate = 0

    for useful_valve in useful_valves:
        if useful_valve not in new_opened:
            distance = distances[valve.name][useful_valve]
            child_flow_rate = release_pressure_useful_rec(valves[useful_valve], valves, minutes_left - distance,
                                                          new_opened, distances, useful_valves)
            flow_rates.append(child_flow_rate)

    if flow_rates:
        return max(flow_rates) + flow_rate
    else:
        return 0


def release_pressure_useful_dual_rec(valve_h, valve_e, valves, minutes_left_h, minutes_left_e, opened, distances,
                                     useful_valves):
    if minutes_left_h < 2 and minutes_left_e < 2:
        return 0
    flow_rates = []

    flow_rate = 0

    ## human player
    if valve_h.flow_rate > 0 and valve_h.name not in opened:
        opened.add(valve_h.name)
        minutes_left_h -= 1
        flow_rate = minutes_left_h * valve_h.flow_rate

    ## elephant player
    elif valve_e.flow_rate > 0 and valve_e.name not in opened:
        opened.add(valve_e.name)
        minutes_left_e -= 1
        flow_rate = minutes_left_e * valve_e.flow_rate

    for useful_valve in useful_valves:
        if useful_valve not in opened:
            # move human first
            if minutes_left_h >= minutes_left_e:
                # human
                distance_h = distances[valve_h.name][useful_valve]
                child_flow_rate = release_pressure_useful_dual_rec(valves[useful_valve], valve_e, valves,
                                                                   minutes_left_h - distance_h, minutes_left_e, opened.copy(),
                                                                   distances, useful_valves)
                flow_rates.append(child_flow_rate)
            else:
                # elephant
                distance_e = distances[valve_e.name][useful_valve]
                child_flow_rate = release_pressure_useful_dual_rec(valve_h, valves[useful_valve], valves,
                                                                   minutes_left_h, minutes_left_e - distance_e, opened.copy(),
                                                                   distances, useful_valves)
                flow_rates.append(child_flow_rate)

    if flow_rates:
        return max(flow_rates) + flow_rate
    else:
        return 0


def find_next_best_path_rec(valve, valves, minutes_left, opened, distances, useful_valves):
    if minutes_left < 2:
        return 0, []

    flow_rates = []

    new_opened = opened.copy()
    if valve.flow_rate > 0:
        new_opened.add(valve.name)
        minutes_left -= 1
        flow_rate = minutes_left * valve.flow_rate
    else:
        flow_rate = 0

    for useful_valve in useful_valves:
        if useful_valve not in new_opened:
            distance = distances[valve.name][useful_valve]
            child_flow_rate, path = find_next_best_path_rec(valves[useful_valve], valves, minutes_left - distance,
                                                          new_opened, distances, useful_valves)
            path.insert(0, valves[useful_valve])
            flow_rates.append((child_flow_rate, path))

    if flow_rates:
        max_flow, path = max(flow_rates, key=lambda x: x[0])
        return max_flow + flow_rate, path
    else:
        return 0, []


def release_pressure(valve, valves, minutes_left):
    return release_pressure_rec(valve, valves, minutes_left, set(), set())


def release_pressure_useful(valve, valves, minutes_left, distances, useful_valves):
    return release_pressure_useful_rec(valve, valves, minutes_left, set(), distances, useful_valves)


def release_pressure_useful_dual(valve, valves, minutes_left, distances, useful_valves):
    return release_pressure_useful_dual_rec(valve, valve, valves, minutes_left, minutes_left, set(), distances,
                                            useful_valves)

## same as release_pressure_useful but next valve instead
def find_next_best_path(valve, valves, minutes_left, opened, distances, useful_valves):
    return find_next_best_path_rec(valve, valves, minutes_left, opened, distances, useful_valves)


def release_pressure_by_turn(valve, valves, minutes_left, distances, useful_valves):
    minutes_left_h = minutes_left
    minutes_left_e = minutes_left

    valve_h = valve
    valve_e = valve

    opened = set()

    flow_rate = 0
    while (minutes_left_e > 2 or minutes_left_h > 2) and len(opened) != len(useful_valves):
        if minutes_left_h >= minutes_left_e:
            path = find_next_best_path(valve_h, valves, minutes_left_h, opened, distances, useful_valves)[1]
            next_valve = path[0]
            minutes_left_h = minutes_left_h - distances[valve_h.name][next_valve.name] - 1
            print(f"Opening valve {next_valve} for human at turn {26 - minutes_left_h}")
            print(list(map(lambda x: x.name, path)))
            opened.add(next_valve.name)
            valve_h = next_valve
            flow_rate += valve_h.flow_rate * minutes_left_h
        else:
            path = find_next_best_path(valve_e, valves, minutes_left_e, opened, distances, useful_valves)[1]
            next_valve = path[0]
            minutes_left_e = minutes_left_e - distances[valve_e.name][next_valve.name] - 1
            print(f"Opening valve {next_valve} for elephant at turn {26 - minutes_left_e}")
            print(list(map(lambda x: x.name, path)))
            opened.add(next_valve.name)
            valve_e = next_valve
            flow_rate += valve_e.flow_rate * minutes_left_e
    return flow_rate





def main():
    with open("input.txt") as f:
        lines = f.readlines()

    valves = dict()
    for line in lines:
        valve = parse_input_line(line)
        valves[valve.name] = valve

    return release_pressure(valves['AA'], valves, 30)


# Optimize exercise 1
def main_bis():
    with open("input.txt") as f:
        lines = f.readlines()

    valves = dict()
    valve_list = []
    useful_valves = []
    for line in lines:
        valve = parse_input_line(line)
        valves[valve.name] = valve
        valve_list.append(valve)
        if valve.is_useful():
            useful_valves.append(valve.name)

    distances = compute_distance(valve_list, valves)
    return release_pressure_useful(valves['AA'], valves, 30, distances, useful_valves)

## too slow, bad result
def main2():
    with open("input.txt") as f:
        lines = f.readlines()

    valves = dict()
    valve_list = []
    useful_valves = []
    for line in lines:
        valve = parse_input_line(line)
        valves[valve.name] = valve
        valve_list.append(valve)
        if valve.is_useful():
            useful_valves.append(valve.name)

    distances = compute_distance(valve_list, valves)
    return release_pressure_useful_dual(valves['AA'], valves, 26, distances, useful_valves)


def main2bis():
    with open("input.txt") as f:
        lines = f.readlines()

    valves = dict()
    valve_list = []
    useful_valves = []
    for line in lines:
        valve = parse_input_line(line)
        valves[valve.name] = valve
        valve_list.append(valve)
        if valve.is_useful():
            useful_valves.append(valve.name)

    distances = compute_distance(valve_list, valves)
    return release_pressure_by_turn(valves['AA'], valves, 26, distances, useful_valves)


if __name__ == '__main__':
    print(main2bis())
