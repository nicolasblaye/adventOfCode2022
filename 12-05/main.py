import queue
import re


def main():
    fifo_queues = dict()
    moves = []
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('move'):
                move = line.strip().split(" ")
                moves.append((move[1], move[3], move[5]))
            elif "[" in line:
                letters = re.split(";", line)
                i = 1
                for letter in letters:
                    if letter.strip():
                        real_letter = letter.strip()[1]
                        if i not in fifo_queues:
                            fifo_queues[i] = []
                        fifo_queues[i].append(real_letter)
                    i += 1
    print(fifo_queues)
    for move in moves:
        number, from_, to = move
        from_queue = fifo_queues[int(from_)]
        to_queue = fifo_queues[int(to)]
        for i in range(int(number)):
            elem = from_queue.pop(0)
            to_queue.insert(0, elem)

    print(fifo_queues)
    for i in range(len(fifo_queues.keys())):
        key = i+1
        print(fifo_queues[key].pop(0))

def main2():
    fifo_queues = dict()
    moves = []
    current = 0
    with(open("input.txt", encoding='utf-8')) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('move'):
                move = line.strip().split(" ")
                moves.append((move[1], move[3], move[5]))
            elif "[" in line:
                letters = re.split(";", line)
                i = 1
                for letter in letters:
                    if letter.strip():
                        real_letter = letter.strip()[1]
                        if i not in fifo_queues:
                            fifo_queues[i] = []
                        fifo_queues[i].append(real_letter)
                    i += 1
    print(fifo_queues)
    for move in moves:
        number, from_, to = move
        from_queue = fifo_queues[int(from_)]
        to_queue = fifo_queues[int(to)]
        to_append = []
        for i in range(int(number)):
            elem = from_queue.pop(0)
            to_append.append(elem)
        for i in range(len(to_append)):
            to_queue.insert(0, to_append[-(1 + i)])

    print(fifo_queues)
    for i in range(len(fifo_queues.keys())):
        key = i + 1
        print(fifo_queues[key].pop(0))


if __name__ == '__main__':
    main2()
