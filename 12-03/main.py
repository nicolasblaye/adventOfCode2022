letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in lines:
            mid_index = int(len(line.strip()) / 2)
            first_half = line[:mid_index]
            second_half = line[mid_index::]
            for letter in first_half:
                if letter in second_half:
                    print(letter)
                    current += letters.index(letter) + 1
                    break
    print(current)


def main2():
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            first = lines[i]
            second = lines[i+1]
            third = lines[i+2]
            for letter in first:
                if letter in second and letter in third:
                    current += letters.index(letter) + 1
                    break

    print(current)


if __name__ == '__main__':
    main2()
