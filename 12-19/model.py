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

    def __init__(self, blueprint, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot):
        self.blueprint = blueprint
        self.types_of_robots = blueprint.robots
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.mineral_mapping = {
            Ore(): self.ore_robot,
            Clay(): self.clay_robot,
            Obsidian(): self.obsidian_robot
        }

    def can_create(self, robot):
        for mineral, number in robot.needed_minerals.items():
            number = int(number)
            if number > 0 and number > self.get_ore(mineral):
                return False
        return True

    def time_for_next_robot(self):
        time_for_robots = {}
        for robot in self.types_of_robots:
            if robot == self.blueprint.ore_robot and self.ore_robot >= int(self.blueprint.max_ore_for_robot):
                continue
            elif robot == self.blueprint.clay_robot and self.clay_robot >= int(self.blueprint.max_clay_for_robot):
                continue
            else:
                time_for_robots[robot] = self.time_for_robot(robot)
        return time_for_robots

    def time_for_robot(self, robot):
        time = 0
        for mineral, number in robot.needed_minerals.items():
            number = int(number)
            if number > 0:
                number = max(0, number - self.get_ore(mineral))
                time = max(time, self.time_for_n_mineral(mineral, number))
        return time


    def time_for_n_mineral(self, mineral, number):
        robot = self.mineral_mapping[mineral]
        if robot > 0:
            return ceil(number / robot)
        else:
            return 10000

    def create(self, robot, time):
        for mineral, number in robot.needed_minerals.items():
            number = int(number)
            self.set_ore(mineral, self.get_ore(mineral) - number)
        ## if it's a geode, just compute the number of geodes
        if robot == self.blueprint.geode_robot:
            self.set_ore(Geode(), self.get_ore(Geode()) + time)
        else:
            self.create_robot(robot)


    def play_turn(self, time):
        for mineral, number in self.mineral_mapping.items():
            self.set_ore(mineral, self.get_ore(mineral) + number * time)


    def create_robot(self, robot):
        if self.blueprint.ore_robot == robot:
            self.ore_robot += 1
        if self.blueprint.clay_robot == robot:
            self.clay_robot += 1
        if self.blueprint.obsidian_robot == robot:
            self.obsidian_robot += 1
        if self.blueprint.geode_robot == robot:
            self.geode += 1

    def get_ore(self, mineral):
        if mineral == Ore():
            return self.ore
        if mineral == Clay():
            return self.clay
        if mineral == Obsidian():
            return self.obsidian
        if mineral == Geode():
            return self.geode

    def set_ore(self, mineral, number):
        if mineral == Ore():
            self.ore = number
        if mineral == Clay():
            self.clay = number
        if mineral == Obsidian():
            self.obsidian = number
        if mineral == Geode():
            self.geode = number

    def get_nb_robot(self, robot):
        if self.blueprint.ore_robot == robot:
            return self.ore_robot
        if self.blueprint.clay_robot == robot:
            return self.clay_robot
        if self.blueprint.obsidian_robot == robot:
            return self.obsidian_robot
        if self.blueprint.geode_robot == robot:
            return self.geode


    def copy(self):
        return Solution(self.blueprint, self.ore, self.clay, self.obsidian, self.geode, self.ore_robot, self.clay_robot, self.obsidian_robot)


    def __str__(self):
        return f"Solution has {self.get_nb_robot(self.blueprint.ore_robot)} ore robot, {self.get_nb_robot(self.blueprint.clay_robot)} clay robot, " \
               f"{self.get_nb_robot(self.blueprint.obsidian_robot)} obsidian robot and {self.get_nb_robot(self.blueprint.geode_robot)} geode robot" \
               f". It has {self.get_ore(Ore())} ore, {self.get_ore(Clay())} clay, " \
               f"{self.get_ore(Obsidian())} obsidian and {self.get_ore(Geode())} geode."