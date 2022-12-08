# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def main():
    with(open("input.txt", encoding ='utf-8')) as f:
        max = 0
        current = 0
        for line in f.readlines():
            if (line.strip()):
                current += int(line)
            else:
                if (current > max):
                    max = current
                current = 0
    print(max)


def main2():
    with(open("input.txt", encoding ='utf-8')) as f:
        list_elf = []
        current = 0
        for line in f.readlines():
            if (line.strip()):
                #print(current, int(line))
                current += int(line)
            else:
                list_elf.append(current)
                current = 0
    list_elf.sort()
    list_elf.reverse()
    print(list_elf)
    print(list_elf[0] + list_elf[1] + list_elf[2])


if __name__ == '__main__':
    main2()
