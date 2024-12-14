from functools import reduce
from itertools import combinations, product
from pprint import pprint
import numpy as np


def r_data(d_s):
    d = [[x for x in s] for s in d_s.split()]
    return d


data_s = '''AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
'''
data = r_data(data_s)
with open('input12.txt') as f:
    data_s = f.read()

data = r_data(data_s)

pprint(data)
assert len(data) == len(data[0])
size = len(data)


def close_neighbours(point):
    r = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i * j == 0:
                r.append((i + point[0], j + point[1]))
    return r


def neighbours(point):
    r = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == j == 0):
                r.append((i + point[0], j + point[1]))
    return r


def area(r):
    return len(r)


def perimeter(r):
    count = 0
    for point in r:
        for n in close_neighbours(point):
            if n not in r:
                count += 1
    return count


def sides(r):
    count = 0
    for i in range(size):
        count += scan_h_line(r, [(i, j) for j in range(size)])
    for j in range(size):
        count += scan_v_line(r, [(i, j) for i in range(size)])
    return count


def scan_h_line(r, line):
    fence_up = ["0"] * size
    fence_down = ["0"] * size
    for i in range(size):
        ii, jj = line[i]
        fence_up[i] = "1" if (ii - 1, jj) not in r and line[i] in r else " "
        fence_down[i] = "1" if (ii + 1, jj) not in r and line[i] in r else " "
    return len("".join(fence_up).split()) + len("".join(fence_down).split())

def scan_v_line(r, line):
    fence_up = ["0"] * size
    fence_down = ["0"] * size
    for i in range(size):
        ii, jj = line[i]
        fence_up[i] = "1" if (ii, jj - 1) not in r and line[i] in r else " "
        fence_down[i] = "1" if (ii, jj + 1) not in r and line[i] in r else " "
    return len("".join(fence_up).split()) + len("".join(fence_down).split())


def get_data(p):
    return data[p[0]][p[1]]


datadict = {(i, j): get_data((i, j)) for i in range(size) for j in range(size)}
dataset = {d for d in datadict}


def get_next_region(dset):
    front = {dset.pop()}
    reg = set()
    while front:
        f = front.pop()
        reg.add(f)
        for p in close_neighbours(f):
            if p in dset and p not in reg and datadict[p] == datadict[f]:
                front.add(p)
    dset -= reg
    return reg


def get_regs(dataset):
    regions = []
    while dataset:
        print()
        regions.append(get_next_region(dataset))
        for i in range(size):
            for j in range(size):
                p = (i, j)
                print(get_data(p) if p in regions[-1] else '.', end="")
            print()
    return regions


regions = get_regs(dataset)
pprint(regions, width=150)
print(sum(len(r) for r in regions))
print(*[(get_data(list(r)[0]), area(r), perimeter(r), r) for r in regions], sep="\n")
print(sum([area(r) * perimeter(r) for r in regions]))
print(sum([area(r) * sides(r) for r in regions]))