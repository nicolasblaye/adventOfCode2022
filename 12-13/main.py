from functools import cmp_to_key


def recursive_parser(line, index):
    result_list = []
    while index < len(line):
        current_value = line[index]
        if current_value == '[':
            values_list, index = recursive_parser(line, index+1)
            result_list.append(values_list)
        elif current_value == ']':
            return result_list, index
        elif current_value != ',':
            if index + 1 < len(line) and line[index + 1] not in [',', '[', ']']:
                result_list.append(int(line[index:index+2]))
                index += 1
            else:
                result_list.append(int(line[index]))

        index += 1


def parse(line):
    result_list, _ = recursive_parser(line[1::], 0)
    return result_list


def is_pair_in_right_order(pair1, pair2):
    for i in range(len(pair1)):
        if i == len(pair2):
            return False
        value1 = pair1[i]
        value2 = pair2[i]

        is_in_right_order = None
        if type(value1) == list == type(value2):
            is_in_right_order = is_pair_in_right_order(value1, value2)
            if is_in_right_order in (True, False):
                #print("list order: ", is_in_right_order, value1, value2)
                return is_in_right_order

        elif type(value1) != type(value2):
            if type(value1) != list:
                is_in_right_order = is_pair_in_right_order([value1], value2)
            else:
                is_in_right_order = is_pair_in_right_order(value1, [value2])
            if is_in_right_order in (True, False):
                #print("list/value order: ", is_in_right_order, value1, value2)
                return is_in_right_order

        elif value1 > value2:
            #print("value order: ", False, value1, value2)
            return False
        elif value1 < value2:
            #print("value order: ", True, value1, value2)
            return True
        else:
            continue
    if len(pair2) > len(pair1):
        return True
    elif len(pair2) == len(pair1):
        return None
    else:
        return None


def compare_packets(packet1, packet2):
    result = is_pair_in_right_order(packet1, packet2)
    if result:
        return -1
    elif result is None:
        return 0
    else:
        return 1


def main():
    with open("input.txt") as f:
        lines = f.readlines()
        pair_index = 1
        results = []
        for i in range(0, len(lines), 3):
            pair1 = parse(lines[i].strip())
            pair2 = parse(lines[i+1].strip())

            result = is_pair_in_right_order(pair1, pair2)
            print(pair1, pair2)
            if result:
                results.append(pair_index)
            pair_index += 1
        return results


def main2():
    with open("input.txt") as f:
        lines = f.readlines()
        packets = []
        for i in range(0, len(lines), 3):
            pair1 = parse(lines[i].strip())
            pair2 = parse(lines[i + 1].strip())

            packets.append(pair1)
            packets.append(pair2)

        packets.append([2])
        packets.append([6])
    packets = sorted(packets, key=cmp_to_key(compare_packets))
    return packets.index([2]) + 1, packets.index([6]) + 1


if __name__ == '__main__':
    indexes = main2()
    print(indexes[0] * indexes[1])
