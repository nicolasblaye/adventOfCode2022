import math


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


class Monkey:
    inspect = 0

    def __init__(self, monkey_id, items, operation, test, throw_true, throw_false, is_worry_less):
        self.id = monkey_id
        self.items = items
        self.operation = operation
        self.test = test
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.is_worry_less = is_worry_less

    def __str__(self):
        return f"Monkey {self.id}\nitems: {self.items}\noperation: {self.operation}\ntest: {self.test}" \
               f"\ntrue: {self.throw_true}\nfalse: {self.throw_false}\ninspections: {self.inspect}"

    def apply_operation(self, item, lcm_num):
        members = self.operation.strip().split(" ")
        operation_sign = members[1]
        x1, x2 = 0, 0
        if 'old' == members[0].strip():
            x1 = item
        else:
            x1 = int(members[0].strip())

        if 'old' == members[2].strip():
            x2 = item
        else:
            x2 = int(members[2].strip())
        if operation_sign == '+':
            return (x1 + x2) % lcm_num
        elif operation_sign == '-':
            return (x1 - x2) % lcm_num
        elif operation_sign == '*':
            return (x1 * x2) % lcm_num
        return 0

    @staticmethod
    def throw_to(monkey, item):
        monkey.items.append(item)

    def inspect_items(self, monkeys, lcm_num):
        for item in self.items:
            self.inspect += 1
            new_item = self.apply_operation(item, lcm_num)
            if self.is_worry_less:
                new_item = int(new_item / 3)
            test = new_item % self.test == 0
            if test:
                self.throw_to(monkeys[self.throw_true], int(new_item))
            else:
                self.throw_to(monkeys[self.throw_false], int(new_item))

        self.items = []


def main():
    monkeys = []
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in range(0, len(lines), 7):
            monkey_stat = lines[line:line+7]
            monkey_id = int(monkey_stat[0].strip().split(" ")[-1].split(":")[0])
            monkey_items = list(map(int, monkey_stat[1].strip().split(":")[-1].split(', ')))
            monkey_operation = monkey_stat[2].strip().split("=")[-1]
            monkey_test_divisible = int(monkey_stat[3].strip().split("by ")[-1])
            monkey_throw_true = int(monkey_stat[4].strip().split(" ")[-1])
            monkey_throw_false = int(monkey_stat[5].strip().split(" ")[-1])

            monkey = Monkey(monkey_id, monkey_items, monkey_operation, monkey_test_divisible, monkey_throw_true,
                            monkey_throw_false, True)
            monkeys.append(monkey)

    lcm_num = 1
    for monkey in monkeys:
        lcm_num = lcm(lcm_num, monkey.test)
    print(lcm_num)
    for i in range(20):
        for monkey in monkeys:
            monkey.inspect_items(monkeys, lcm_num)
    return monkeys


def main2():
    monkeys = []
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in range(0, len(lines), 7):
            monkey_stat = lines[line:line + 7]
            monkey_id = int(monkey_stat[0].strip().split(" ")[-1].split(":")[0])
            monkey_items = list(map(int, monkey_stat[1].strip().split(":")[-1].split(', ')))
            monkey_operation = monkey_stat[2].strip().split("=")[-1]
            monkey_test_divisible = int(monkey_stat[3].strip().split("by ")[-1])
            monkey_throw_true = int(monkey_stat[4].strip().split(" ")[-1])
            monkey_throw_false = int(monkey_stat[5].strip().split(" ")[-1])

            monkey = Monkey(monkey_id, monkey_items, monkey_operation, monkey_test_divisible, monkey_throw_true,
                            monkey_throw_false, False)
            monkeys.append(monkey)

    lcm_num = 1
    for monkey in monkeys:
        lcm_num = lcm(lcm_num, monkey.test)
    print(lcm_num)

    for i in range(10000):
        for monkey in monkeys:
            monkey.inspect_items(monkeys, lcm_num)
    return monkeys


if __name__ == '__main__':
    inspections = []
    monkeys = main2()
    for monkey in monkeys:
        print(f"Monkey {monkey.id}: {monkey.inspect} inspections")
        inspections.append(monkey.inspect)
    inspections = sorted(inspections)
    print("Monkey Business is: ", inspections[-1] * inspections[-2])
