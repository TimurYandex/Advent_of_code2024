from itertools import product
from pprint import pprint

data = [list(map(int, s.split(","))) for s in open("input18.txt").read().split()]

s = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''
# data = [list(map(int, ss.split(","))) for ss in s.split()]

def prepare(j):
    space = [[0] * 71 for _ in range(71)]
    for d in data[:j]:
        y, x = d
        space[x][y] = 1
    return space



def show(s):
    for row in s:
        print("".join([("#" if row[i] == 1 else "O") if row[i] else "." for i in range(len(row))]))



def bfs(s):
    seen = {(0, 0): 0}
    front = [((0, 0), 0)]
    front_set = {(0, 0)}
    size = len(s)

    def unseen_children(point):
        nonlocal s
        y, x = point
        children = []
        for a, b in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            child = (y + a, x + b)
            if 0 <= x + b <= size - 1 and 0 <= y + a <= size - 1 and s[x + b][y + a] == 0:
                if child not in seen:
                    children.append((child, seen[point] + 1))
        return children

    count = 0
    while front:
        count += 1
        point, score = front.pop(0)
        seen[point] = score
        y, x = point
        # s[x][y] = seen[(y, x)]
        if point == (size - 1, size - 1):
            break
        for ch in unseen_children(point):
            if ch[0] not in front_set:
                front.append(ch)
                front_set.add(ch[0])

        # if count % 10 == 0:
        #     print()
        #     show(s)
        #     print(front)

    return seen[(size - 1, size - 1)]

try:
    for i in range(5000):
        j = i
        space = prepare(j)
        print(bfs(space))
except KeyError:
    print(data[j - 1])

