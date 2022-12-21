import re


def operation(a, b, sign, should_round = True):
    if sign == '/':
        if should_round:
            return int(a / b)
        else:
            return a/b
    elif sign == '*':
        return a * b
    elif sign == '-':
        return a - b
    elif sign == '+':
        return a + b

def parse_input(input_path):
    monkeys = {}

    with open(input_path) as f:
        lines = f.readlines()

    for line in lines:
        monkey, job = line.strip().split(":")
        parse_job = re.split(" ", job.strip())
        if len(parse_job) == 3:
            a, op, b = parse_job
            if a.isnumeric():
                a = int(a)
            if b.isnumeric():
                b = int(b)
            job =  a, op, b
        else:
            job = int(job)
        monkeys[monkey] = job
    return monkeys

def compute(monkey, op, monkeys):
    if type(op) != int:
        a, sign, b = op
        if type(a) == str:
            a = compute(a, monkeys[a], monkeys)
        if type(b) == str:
            b = compute(b, monkeys[b], monkeys)
        res = operation(a, b, sign)
        monkeys[monkey] = res
        return operation(a, b, sign)
    elif op in monkeys:
        return compute(op, monkeys[op], monkeys)
    else:
        return op


def compute_with_humn(monkey, op, monkeys):
    if type(op) != int:
        a, sign, b = op
        if type(a) == str and a != 'humn':
            a = compute_with_humn(a, monkeys[a], monkeys)
        if type(b) == str and b != 'humn':
            b = compute_with_humn(b, monkeys[b], monkeys)
        if (type(a) == str and 'humn' in a) or (type(b) == str and 'humn' in b):
            res = (a, sign, b)
        elif type(a)==type(b)==int:
            res = operation(a, b, sign)
        else:
            res = (a, sign, b)
        monkeys[monkey] = res
        return res
    elif op in monkeys:
        return compute_with_humn(op, monkeys[op], monkeys)
    else:
        return op


def compute_rec_op(temp_first_value, second_value):
    if type(temp_first_value) != tuple:
        if temp_first_value == 'humn':
            return second_value
        return temp_first_value
    else:
        a,sign,b = temp_first_value
        if type(a) == int == type(b):
            return operation(a, b, sign)
        elif type(a) == int:
            return operation(a, compute_rec_op(b, second_value), sign)
        else:
            return operation(compute_rec_op(a, second_value), b, sign)

def main(input_path):
    monkeys = parse_input(input_path)

    root_op = monkeys["root"]
    i = int(compute("root", root_op, monkeys))
    print(monkeys)
    return i

inverted_sign = {
    '-' : '+',
    '+' : '-',
    '/' : '*',
    '*' : '/',
}

def main2(input_path):
    monkeys = parse_input(input_path)

    root_op = monkeys["root"]
    first_value = compute_with_humn(root_op[0], monkeys[root_op[0]], monkeys)
    second_value = compute_with_humn(root_op[2], monkeys[root_op[2]], monkeys)
    print(first_value)
    print(second_value)
    temp_first_value = first_value
    temp_second_value = second_value
    while True:
        if type(first_value) != tuple:
            break
        a, sign, b = first_value
        if type(a) == int:
            if sign == '-':
                second_value = operation(second_value, a, '-')
                second_value = operation(second_value, -1, '*')
            else:
                second_value = operation(second_value, a, inverted_sign[sign], False)
            first_value = b
        elif type(b) == int:
            second_value = operation(second_value, b, inverted_sign[sign], False)
            first_value = a
    print(int(compute_rec_op(temp_first_value, second_value)) == int(temp_second_value))
    return second_value

if __name__ == '__main__':
    result = main2("input.txt")
    print(round(result))
