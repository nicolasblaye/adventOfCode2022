from copy import deepcopy
from math import ceil

class Mineral:
    name = ""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


    def __hash__(self):
        return self.name.__hash__()


class Ore(Mineral):
    def __init__(self):
        super().__init__("Ore")

class Clay(Mineral):
    def __init__(self):
        super().__init__("Clay")
class Obsidian(Mineral):
    def __init__(self):
        super().__init__("Obsidian")

class Geode(Mineral):
    def __init__(self):
        super().__init__("Geode")

class Robot:
    name = ""

    def __init__(self, ore: int, clay: int, obsidian: int):
        self.needed_minerals = dict()
        self.needed_minerals[Ore()] = ore
        self.needed_minerals[Clay()] = clay
        self.needed_minerals[Obsidian()] = obsidian

    def produce(self):
        return Mineral("")

    def __str__(self):
        return f"{self.name} - {self.needed_minerals}"

    def __eq__(self, other):
        return self.name.__eq__(other.name)

    def __hash__(self):
        return self.name.__hash__()


class OreRobot(Robot):
    name = "OreRobot"

    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)

    def produce(self):
        return Ore()

class ClayRobot(Robot):
    name = "ClayRobot"
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)

    def produce(self):
        return Clay()

class ObsidianRobot(Robot):
    name = "ObsidianRobot"
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)

    def produce(self):
        return Obsidian()

class GeodeRobot(Robot):
    name = "GeodeRobot"
    produced_mineral = Geode()
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)

    def produce(self):
        return Geode()


class Blueprint:
    max_ore_for_robot = 0
    max_clay_for_robot = 0

    def __init__(self, b_id, ore_robot, clay_robot, obsidian_robot, geode_robot):
        self.b_id = b_id
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.geode_robot = geode_robot
        self.robots = [self.ore_robot, self.clay_robot, self.obsidian_robot, self.geode_robot]
        self.max_ore_for_robot = max(max(clay_robot.needed_minerals[Ore()], obsidian_robot.needed_minerals[Ore()]),
                                     geode_robot.needed_minerals[Ore()])
        self.max_clay_for_robot = max(int(obsidian_robot.needed_minerals[Clay()]), int(geode_robot.needed_minerals[Clay()]))

    def __str__(self):
        return f"{self.b_id} - {self.ore_robot} - {self.clay_robot} - {self.obsidian_robot} - {self.geode_robot}"


class Solution:
    created_at = []

    def __init__(self, blueprint, ores = {Ore() : 0, Clay() : 0, Obsidian() : 0, Geode() : 0}, robots = {}, turn_played = 0, created_at = []):
        self.blueprint = blueprint
        self.types_of_robots = blueprint.robots
        self.turn_played = turn_played
        self.created_at = created_at
        if not robots:
            self.robots = robots
            self.ores = ores
            self.create(blueprint.ore_robot, 23)
            self.ores[Ore()] = 0
        else:
            self.ores = ores
            self.robots = robots
        self.mineral_mapping = {
            Ore(): self.blueprint.ore_robot,
            Clay(): self.blueprint.clay_robot,
            Obsidian(): self.blueprint.obsidian_robot,
            Geode(): self.blueprint.geode_robot,
        }

    def can_create(self, robot):
        for mineral, number in robot.needed_minerals.items():
            number = int(number)
            if number > 0 and (mineral not in self.ores or number > self.ores[mineral]):
                return False
        return True

    def time_for_next_robot(self):
        time_for_robots = {}
        for robot in self.types_of_robots:
            if robot in self.robots and robot == self.blueprint.ore_robot and int(self.robots[robot]) >= int(self.blueprint.max_ore_for_robot):
                continue
            elif robot in self.robots and robot == self.blueprint.clay_robot and int(self.robots[robot]) >= int(self.blueprint.max_clay_for_robot):
                continue
            else:
                time_for_robots[robot] = self.time_for_robot(robot)
        return time_for_robots

    def time_for_robot(self, robot):
        time = 0
        for mineral, number in robot.needed_minerals.items():
            number = int(number)
            if number > 0:
                if mineral in self.ores:
                    number = max(0, number - self.ores[mineral])
                time = max(time, self.time_for_n_mineral(mineral, number))
        return time


    def time_for_n_mineral(self, mineral, number):
        robot = self.mineral_mapping[mineral]
        if robot in self.robots and self.robots[robot] > 0:
            number_of_robots = self.robots[robot]
            return ceil(number / number_of_robots)
        else:
            return 10000

    def create(self, robot, time):
        self.created_at.append((24 - time, robot.name))
        for mineral, number in robot.needed_minerals.items():
            number = int(number)
            self.ores[mineral] = self.ores[mineral] - number
        ## if it's a geode, just compute the number of geodes
        if robot == self.blueprint.geode_robot:
            if Geode() not in self.ores:
                self.ores[Geode()] = 0
            self.ores[Geode()] += time
        else:
            if robot not in self.robots:
                self.robots[robot] = 0
            self.robots[robot] = self.robots[robot] + 1


    def play_turn(self, time):
        self.turn_played += time
        for robot, number in self.robots.items():
            mineral = robot.produce()
            if mineral in self.ores:
                self.ores[mineral] = self.ores[mineral] + (number * time)
            else:
                self.ores[mineral] = (number * time)


    def get_ore(self, mineral):
        if mineral in self.ores:
            return self.ores[mineral]
        else:
            return 0

    def get_nb_robot(self, robot):
        if robot in self.robots:
            return self.robots[robot]
        else:
            return 0


    def __str__(self):
        return f"Solution has {self.get_nb_robot(self.blueprint.ore_robot)} ore robot, {self.get_nb_robot(self.blueprint.clay_robot)} clay robot, " \
               f"{self.get_nb_robot(self.blueprint.obsidian_robot)} obsidian robot and {self.get_nb_robot(self.blueprint.geode_robot)} geode robot" \
               f". It has {self.get_ore(Ore())} ore, {self.get_ore(Clay())} clay, " \
               f"{self.get_ore(Obsidian())} obsidian and {self.get_ore(Geode())} geode." \
               f" Turn_played: {self.turn_played}. " \
               f"Created at: {self.created_at}"
