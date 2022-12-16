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


def generate_all_possible_path_with_score(valve, valves, minutes_left, distances, useful_valves, opened):
    if minutes_left < 2:
        return [(0, [])]

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
            score_with_path = generate_all_possible_path_with_score(valves[useful_valve], valves, minutes_left - distance,
                                                                          distances, useful_valves, new_opened)
            flow_rates.extend(list(map(lambda x: (x[0], [useful_valve] + x[1]), score_with_path)))

    if flow_rates:
        score_with_path = list(map(lambda x: (x[0] + flow_rate, x[1]), flow_rates))
        return score_with_path + [(flow_rate, [valve.name])]
    else:
        return [(0, [])]

def main():
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
    score_with_path_list = generate_all_possible_path_with_score(valves['AA'], valves, 26, distances, useful_valves, set())
    print(len(score_with_path_list))
    #print(score_with_path_list)
    score_with_path_list = sorted(score_with_path_list, key=lambda x: x[0], reverse=True)
    #print(score_with_path_list)
    max_score = 0
    for i in range(len(score_with_path_list)):
        score1, path1 = score_with_path_list[i]
        for j in range(i+1, len(score_with_path_list)):
            score2, path2 = score_with_path_list[j]
            if score1 + score2 < max_score:
                break
            if set(path1).isdisjoint(path2):
                current_score = score1 + score2
                if current_score > max_score:
                    max_score = current_score
                    #print(list(map(lambda x: str(x), path1)))
                    #print(list(map(lambda x: str(x), path2)))
                    #print(max_score)
    return max_score


if __name__ == '__main__':
    start = time.time()
    print(main())
    print(round(time.time() - start, 1), "seconds")
