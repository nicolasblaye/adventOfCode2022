from model import Blueprint, OreRobot, ClayRobot, ObsidianRobot, GeodeRobot
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


def main(input_path):
    blueprints = parse_input(input_path)

    for blueprint in blueprints:
        print(blueprint)


if __name__ == '__main__':
    print(main("test_input.txt"))
