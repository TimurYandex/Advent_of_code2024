from itertools import combinations, product
from pprint import pprint

import numpy as np


def r_data(d_s):
    return [list(x) for x in d_s.split()]



with open('input8.txt') as f:
    data_s = f.read()

d_s = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''

d_s = data_s

data = r_data(d_s)
pprint(data)
set_d_s = set("".join(d_s.split()))
nums = sorted(list(range(len(set_d_s))))
di = dict(zip(sorted(list(set_d_s)), nums))
print(len(set_d_s))
pprint(di)
data_num = [[di[x] for x in line] for line in data]
width = len(data_num[0])
height = len(data_num)
pprint(data_num)
data_np = np.array(data_num)
print(data_np)
antinode = len(set_d_s)
dic = {node:[(i,j) for i in range(height) for j in range(width) if data_np[i,j] == node] for node in nums[1:]}
pprint(dic)
all_locations = {(i,j) for i in range(height) for j in range(width)}
# print(sorted(list(all_locations)))
locations = set()
for node in dic:
    # print(dic[node])
    pairs = [p for p in product(dic[node], repeat=2) if p[0] < p[1]]
    # print(pairs)
    for p in pairs:
        locations |= {(2 * p[0][0] - p[1][0], 2 * p[0][1] -  p[1][1]), (2 * p[1][0] - p[0][0], 2 * p[1][1] -  p[0][1])}
# print(sorted(list(locations)))
final = all_locations & locations
# print(sorted(list(final)))
print(len(final))

locations = set()
for node in dic:
    # print(dic[node])
    pairs = [p for p in product(dic[node], repeat=2) if p[0] < p[1]]
    # print(pairs)
    for p in pairs:
        delta = (p[0][0] - p[1][0], p[0][1] - p[1][1])
        locations |= {(p[0][0] + delta[0] * k, p[0][1] + delta[1] * k) for k in range(-width-height, width+height+1)}
# print(sorted(list(locations)))
final = all_locations & locations
# print(sorted(list(final)))
print(len(final))
