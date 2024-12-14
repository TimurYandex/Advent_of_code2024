from functools import reduce
from itertools import combinations, product
from pprint import pprint

import numpy as np


def r_data(d_s):
    d = [[int(x) for x in s] for s in d_s.split()]

    return d


data_s = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''
# data_s = '''19432
# 78121
# 67130
# 56109
# 43211
# '''

data = r_data(data_s)
with open('input10.txt') as f:
    data_s = f.read()


data = r_data(data_s)


pprint(data)
size = len(data)
assert len(data) == len(data[0])

def f1():
    heads = {}
    tops = []
    for i in range(size):
        for j in range(size):
            if data[i][j] == 0:
                heads[(i, j)] = {(i, j)}
            elif data[i][j] == 9:
                tops.append([i, j])
    # print(heads)
    # print(tops)
    for j in range(1,10):
        for head in heads:
            for trail in list(heads[head]):
                if j != 1 + data[trail[0]][trail[1]]:
                    heads[head] -= {trail}
                else:
                    new_trails = {n for n in [(max(0, trail[0] - 1), trail[1]),
                                              (min(size-1, trail[0] + 1), trail[1]),
                                              (trail[0], min(size-1, trail[1] + 1)),
                                              (trail[0], max(0, trail[1] - 1))
                                              ] if data[n[0]][n[1]] == 1 + data[trail[0]][trail[1]]}
                    if new_trails:
                        heads[head] |= new_trails
                heads[head] -= {trail}
    return sum([len(heads[head]) for head in heads])
    # print(f"step {j} = {heads}")
# pprint(heads)
# for head in heads:
    # print(f"head {head} = {len(heads[head])}")
# print([len(heads[head]) for head in heads])
print(f1())

def f2():
    heads = {}
    for i in range(size):
        for j in range(size):
            if data[i][j] == 0:
                heads[(i, j)] = {(i, j)}
    for j in range(1,10):
        for head in heads:
            for trail in list(heads[head]):
                a, b = trail[-2], trail[-1]
                if j != 1 + data[a][b]:
                    heads[head] -= {trail}
                else:
                    new_trails = {trail + n for n in [(max(0, a - 1), b),
                                              (min(size-1, a + 1), b),
                                              (a, min(size-1, b + 1)),
                                              (a, max(0, b - 1))
                                              ] if data[n[0]][n[1]] == 1 + data[a][b]}
                    if new_trails:
                        heads[head] |= new_trails
                heads[head] -= {trail}
    return sum([len(heads[head]) for head in heads])
print(f2())
