def main():
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in lines:
            pairs = line.strip().split(",")
            first_pair = pairs[0].split("-")
            second_pair = pairs[1].split("-")
            if int(first_pair[0]) >= int(second_pair[0]) and int(first_pair[-1]) <= int(second_pair[-1]):
                current += 1
            elif int(second_pair[0]) >= int(first_pair[0]) and int(second_pair[-1]) <= int(first_pair[-1]):
                current += 1
    print(current)


def main2():
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in lines:
            pairs = line.strip().split(",")
            first_pair = pairs[0].split("-")
            second_pair = pairs[1].split("-")
            if int(second_pair[0]) <= int(first_pair[0]) <= int(second_pair[-1]):
                current += 1
            elif int(first_pair[0]) <= int(second_pair[0]) <= int(first_pair[-1]):
                current += 1
    print(current)


if __name__ == '__main__':
    main2()
