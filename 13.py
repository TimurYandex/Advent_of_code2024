from functools import reduce
from itertools import combinations, product
from pprint import pprint
import numpy as np


def r_data(d_s):
    d1 = list(map(lambda x: tuple(map(int, x.split('A: X')[1].split(', Y'))), d_s.split('\n')[::4]))
    d2 = list(map(lambda x: tuple(map(int, x.split('B: X')[1].split(', Y'))), d_s.split('\n')[1::4]))
    d3 = list(map(lambda x: tuple(map(int, x.split('X=')[1].split(', Y='))), d_s.split('\n')[2::4]))
    d11 = [x[0] for x in d1]
    d12 = [x[1] for x in d1]
    d21 = [x[0] for x in d2]
    d22 = [x[1] for x in d2]
    d = list(zip(zip(d11, d21), zip(d12, d22), d3))
    return d


data_s = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''
data = r_data(data_s)
with open('input13.txt') as f:
    data_s = f.read()

data = r_data(data_s)

pprint(data)
from math import gcd

for task in data:
    X_gcd = gcd(task[0][0], task[1][0])
    Y_gcd = gcd(task[0][1], task[1][1])
    print(task, X_gcd, Y_gcd)


def det(m):
    return m[0][0] * m[1][1] - m[1][0] * m[0][1]


def solution(m, r):
    d = det(m)
    dx = det(((r[0], m[0][1]), (r[1], m[1][1])))
    dy = det(((m[0][0], r[0]), (m[1][0], r[1])))
    if d != 0:
        if dx % d == dy % d == 0:
            return dx // d, dy // d
    return None

count = 0
for task in data:
    r = (10000000000000 + task[2][0], 10000000000000 + task[2][1])
    res = solution((task[0], task[1]), r)
    if res:
        x, y = res
        print(sum([a * b for a, b in zip(task[0], (x, y))]))
        print(sum([a * b for a, b in zip(task[1], (x, y))]))
        print(r)
        count += 3*x+y
    else:
        print("решение не целое")
print(f"count = {count}")
print(any([det((task[0], task[1])) == 0 for task in data]))
