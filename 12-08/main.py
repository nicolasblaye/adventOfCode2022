def is_visible(tree, x, y, trees):
    left_visible = True
    right_visible = True
    top_visible = True
    bottom_visible = True
    for i in range(len(trees)):
        # check same line
        if i == y:
            # check before tree
            for j in range(0, x):
                if trees[i][j] >= tree:
                    left_visible = False
            # check after tree
            for j in range(x + 1, len(trees[i])):
                if trees[i][j] >= tree:
                    right_visible =  False
        # check same column
        else:
            if trees[i][x] >= tree and i < y:
                top_visible = False
            elif trees[i][x] >= tree and i > y:
                bottom_visible = False

    return left_visible or right_visible or top_visible or bottom_visible


def scenic_score(tree, x, y, trees):
    left_score = 0
    right_score = 0
    top_score = 0
    bottom_score = 0

    # compute top
    for i in range(y-1, -1, -1):
        top_score += 1
        if trees[i][x] >= tree:
            break

    # compute bottom
    for i in range(y + 1, len(trees)):
        bottom_score += 1
        if trees[i][x] >= tree:
            break

    # compute left
    for i in range(x-1, -1, -1):
        left_score += 1
        if trees[y][i] >= tree:
            break

    for i in range(x+1, len(trees[y])):
        right_score += 1
        if trees[y][i] >= tree:
            break

    return left_score * right_score * top_score * bottom_score


def main():
    with(open("input.txt", encoding='utf-8')) as f:
        trees = []
        lines = f.readlines()
        for line in lines:
            tree_line = []
            line = line.strip()
            for i in line:
                tree_line.append(int(i))
            trees.append(tree_line)

        count = 0
        y = 0
        for tree_line in trees:
            x = 0
            for tree in tree_line:
                if is_visible(tree, x, y, trees):
                    count += 1
                x += 1
            y += 1
        return count



def main2():
    with(open("input.txt", encoding='utf-8')) as f:
        trees = []
        lines = f.readlines()
        for line in lines:
            tree_line = []
            line = line.strip()
            for i in line:
                tree_line.append(int(i))
            trees.append(tree_line)

        current_max = 0
        y = 0
        for tree_line in trees:
            x = 0
            for tree in tree_line:
                score = scenic_score(tree, x, y, trees)
                if score > current_max:
                    current_max = score
                x += 1
            y += 1
        return current_max


if __name__ == '__main__':
    print(main2())
