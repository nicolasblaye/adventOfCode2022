def main():
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        for line in f.readlines():
            # X = Rock 1pts
            # Y = Paper 2pts
            # Z = Scissors 3pts
            line = line.strip()
            # A = Rock
            if line == "A X":
                current += 4
            elif line == "A Y":
                current += 8
            elif line == "A Z":
                current += 3
            # B = Paper
            elif line == "B X":
                current += 1
            elif line == "B Y":
                current += 5
            elif line == "B Z":
                current += 9
            # C = Scissors
            elif line == "C X":
                current += 7
            elif line == "C Y":
                current += 2
            elif line == "C Z":
                current += 6
    print(current)


def main2():
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        for line in f.readlines():
            # Rock 1pts
            # Paper 2pts
            # Scissors 3pts
            # X = Lose
            # Y = Draw
            # Z = Win
            line = line.strip()
            # A = Rock
            if line == "A X":
                current += 3
            elif line == "A Y":
                current += 4
            elif line == "A Z":
                current += 8
            # B = Paper
            elif line == "B X":
                current += 1
            elif line == "B Y":
                current += 5
            elif line == "B Z":
                current += 9
            # C = Scissors
            elif line == "C X":
                current += 2
            elif line == "C Y":
                current += 6
            elif line == "C Z":
                current += 7
    print(current)


if __name__ == '__main__':
    main2()
