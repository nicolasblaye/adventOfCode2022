class Mineral:
    name = ""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


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
    produced_mineral = Mineral("")
    def __init__(self, ore: int, clay: int, obsidian: int):
        self.needed_mineral = dict()
        self.needed_mineral[Ore] = ore
        self.needed_mineral[Clay] = clay
        self.needed_mineral[Obsidian] = obsidian

    def produce(self):
        return self.produced_mineral

    def __str__(self):
        return f"{self.produced_mineral} - {self.needed_mineral}"


class OreRobot(Robot):
    produced_mineral = Ore
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)

class ClayRobot(Robot):
    produced_mineral = Clay
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)

class ObsidianRobot(Robot):
    produced_mineral = Obsidian
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)
class GeodeRobot(Robot):
    produced_mineral = Geode
    def __init__(self, ore: int, clay: int, obsidian: int):
        super().__init__(ore, clay, obsidian)


class Blueprint:
    def __init__(self, b_id, ore_robot, clay_robot, obsidian_robot, geode_robot):
        self.b_id = b_id
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.geode_robot = geode_robot


    def __str__(self):
        return f"{self.b_id} - {self.ore_robot} - {self.clay_robot} - {self.obsidian_robot} - {self.geode_robot}"

