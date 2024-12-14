from pprint import pprint

with open('input6.txt') as f:
    data_s = f.read().split()

d_s = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''.split()

d_s = data_s.copy()

import numpy as np

d_np = np.array([[2 if char == '#' else 0 for char in line] for line in d_s])
d_n = d_np.copy()
g_x = [i for i, s in enumerate(d_s) if s.count('^') == 1][0]
g_y = d_s[g_x].find('^')


def up(d, x, y):
    while x > 0 and d[x - 1, y] != 2:
        x -= 1
        d[x, y] = 1
    if x == 0:
        return False
    return x, y


def down(d, x, y):
    while x < len(d) - 1 and d[x + 1, y] != 2:
        x += 1
        d[x, y] = 1
    if x == len(d) - 1:
        return False
    return x, y


def right(d, x, y):
    while y < len(d) - 1 and d[x, y + 1] != 2:
        y += 1
        d[x, y] = 1
    if y == len(d) - 1:
        return False
    return x, y


def left(d, x, y):
    while y > 0 and d[x, y - 1] != 2:
        y -= 1
        d[x, y] = 1
    if y == 0:
        return False
    return x, y


def loop(d: np.array, x, y):
    pos = (x, y)
    d[x, y] = 1
    positions = {}
    while pos and (pos not in positions or positions[pos] < 3):
        if pos:
            positions[pos] = positions.get(pos, 0) + 1
            pos = up(d, *pos)
        if pos:
            positions[pos] = positions.get(pos, 0) + 1
            pos = right(d, *pos)
        if pos:
            positions[pos] = positions.get(pos, 0) + 1
            pos = down(d, *pos)
        if pos:
            positions[pos] = positions.get(pos, 0) + 1
            pos = left(d, *pos)
    # print(positions)
    return pos


print(loop(d_n, g_x, g_y))
print(np.sum(d_n == 1))
pprint(d_np)
pprint(d_n)

s = len(d_n)
count = 0
for i in range(s):
    for j in range(s):
        print(i,j)
        if (i,j) != (g_x, g_y):
            if d_np[i,j] != 2:
                d_n = d_np.copy()
                d_n[i,j] = 2
                if loop(d_n, g_x, g_y):
                    count += 1
                    print(count)
print(count)