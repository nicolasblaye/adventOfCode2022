# return the index as a positive number
def compute_index(current_index, number, len_input):
    index = correct_overflow(current_index + number, len_input)
    if index >= 0:
        return index
    elif index < 0:
        return len_input + index


# if the index overflows, correct it
def correct_overflow(index, len_input):
    if index >= 0 and index >= len_input:
        return index % len_input
    if index < 0 and abs(index) >= len_input:
        new_index = - abs(index) % len_input -1
        return new_index
    else:
        return index


def compute_solution(input, indexes):
    len_input = len(input)
    list_in_order = [0] * len_input
    for i in range(len_input):
        list_in_order[i] = input[indexes[i][0]]

    index_of_0 = list_in_order.index(0)
    number_1000 = list_in_order[(index_of_0 + 1000) % len_input]
    number_2000 = list_in_order[(index_of_0 + 2000) % len_input]
    number_3000 = list_in_order[(index_of_0 + 3000) % len_input]
    return number_1000 + number_2000 + number_3000


def mix(input, indexes):
    len_input = len(input)
    for i in range(len_input):
        for j in range(len_input):
            order, number = indexes[j]
            temp = indexes[j]
            if order == i:
                new_index = (j + number) % (len_input - 1)
                del indexes[j]
                indexes.insert(new_index, temp)
                break
    return indexes


def main(input_path):
    with open(input_path) as f:
        lines = f.readlines()
    input = []
    indexes = []

    i = 0
    for line in lines:
        number = int(line.strip())
        indexes.append((i, number))
        i += 1
        input.append(number)

    indexes = mix(input, indexes)

    return compute_solution(input, indexes)


def main2(input_path):
    with open(input_path) as f:
        lines = f.readlines()
    input = []
    indexes = []

    i = 0
    for line in lines:
        number = int(line.strip()) * 811589153
        indexes.append((i, number))
        i += 1
        input.append(number)

    for i in range(10):
        indexes = mix(input, indexes)

    return compute_solution(input, indexes)


if __name__ == '__main__':
    result = main2("input.txt")
    print(result)
