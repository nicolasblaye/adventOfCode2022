
def main():
    with(open("input.txt", encoding='utf-8')) as f:
        line = f.readline()
        acc = []
        letters = dict()
        for i in range(len(line)):
            char = line[i]
            if len(acc) == 14:
                removed = acc.pop(0)
                letters[removed] -= 1
            if char not in letters:
                letters[char] = 0
            letters[char] += 1
            acc.append(char)
            if len(acc) == 14:
                is_code = True
                for key, values in letters.items():
                    if values > 1:
                        is_code = False
                if is_code:
                    return i+1

def main2():
    print("toto")


if __name__ == '__main__':
    print(main())
