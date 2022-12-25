import math

def parse_input(input_path):
    with open(input_path) as f:
        lines = f.readlines()

    fuel_req_list = []
    for line in lines:
        fuel_req = []
        line = line.strip()
        for i in range(len(line) - 1, -1, -1):
            fuel_req.append(line[i])
        fuel_req_list.append(fuel_req)

    return fuel_req_list

signs_mapping = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}
def compute_fuel_req(fuel_req):
    number = 0
    for i in range(len(fuel_req)):
        sign = fuel_req[i]
        number += math.pow(5, i) * signs_mapping[sign]
    return int(number)

def to_snafu(numeric):
    snafu = ""
    while numeric:
        snafu += "012=-"[numeric % 5]
        numeric = (numeric + 2) // 5
    return snafu[::-1]


def main(input_path):
    fuel_req_list = parse_input(input_path)
    numeric =  sum(list(map(compute_fuel_req, fuel_req_list)))
    print(numeric)
    snafu = to_snafu(numeric)
    return snafu

if __name__ == '__main__':
    fuel_sum = main("test_input.txt")
    print("\nResult is: ", fuel_sum)