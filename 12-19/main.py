from copy import deepcopy

from model import Blueprint, OreRobot, ClayRobot, ObsidianRobot, GeodeRobot, Solution, Geode, Ore, Clay, Obsidian
import re

pattern = re.compile("Blueprint (\d+): Each ore robot costs (\d+) ore."
                     " Each clay robot costs (\d+) ore."
                     " Each obsidian robot costs (\d+) ore and (\d+) clay."
                     " Each geode robot costs (\d+) ore and (\d+) obsidian."
                     )

def parse_input(path):
    blueprints = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        matches = pattern.match(line)
        ore_robot = OreRobot(matches.group(2), 0, 0)
        clay_robot = ClayRobot(matches.group(3), 0, 0)
        obsidian_robot = ObsidianRobot(matches.group(4), matches.group(5), 0)
        geode_robot = GeodeRobot(matches.group(6), 0, matches.group(7))
        blueprint = Blueprint(matches.group(1), ore_robot, clay_robot, obsidian_robot, geode_robot)
        blueprints.append(blueprint)
    return blueprints


def compute_n_turns(turns_left, solution):
    if turns_left == 1:
        return solution.copy()
    child_solutions = []

    new_solution = solution.copy()
    time_for_next_robot = new_solution.time_for_next_robot()
    # if we can build geode, do it
    if time_for_next_robot[new_solution.blueprint.geode_robot] == 0:
        robot, time = new_solution.blueprint.geode_robot, 0
        if time + 1 <= turns_left:
            new_new_solution = new_solution.copy()
            new_new_solution.play_turn(time + 1)
            new_new_solution.create(robot, turns_left - time - 1)
            child_solutions.append(compute_n_turns(turns_left-time-1, new_new_solution))
        else:
            child_solutions.append(new_solution)
    else:
        for robot, time in time_for_next_robot.items():
            if time + 1 <= turns_left:
                new_new_solution = new_solution.copy()
                new_new_solution.play_turn(time + 1)
                new_new_solution.create(robot, turns_left - time - 1)
                child_solutions.append(compute_n_turns(turns_left-time-1, new_new_solution))
            else:
                child_solutions.append(new_solution)
    if child_solutions:
        return max(child_solutions, key=lambda x: int(x.get_ore(Geode())))
    else:
        return solution


def main(input_path):
    blueprints = parse_input(input_path)

    max_geode = []
    for blueprint in blueprints:
        solution = Solution(blueprint, ores = {Ore() : 0, Clay() : 0, Obsidian() : 0, Geode() : 0}, robots = {}, turn_played = 0, created_at = [])
        solution.play_turn(1)
        best_solution = compute_n_turns(23, solution)
        if Geode() in best_solution.ores:
            max_geode.append(best_solution.ores[Geode()] * int(blueprint.b_id))
            #print(best_solution)
            print(f"max for blueprint {blueprint.b_id} is {best_solution.ores[Geode()]}")
    return max_geode


def main2(input_path):
    blueprints = parse_input(input_path)
    blueprints = blueprints[:3]

    max_geode = []
    for blueprint in blueprints:
        solution = Solution(blueprint, 0, 0, 0, 0, 1, 0, 0)
        best_solution = compute_n_turns(32, solution)
        max_geode.append(best_solution.get_ore(Geode()))
        #print(best_solution)
        print(f"max for blueprint {blueprint.b_id} is {best_solution.get_ore(Geode())}")
    return max_geode


if __name__ == '__main__':
    result = main2("input.txt")
    geodes = 1
    for i in result:
        geodes *= i
    print(geodes)
