from functools import reduce
from math import log10
from itertools import combinations, product
from pprint import pprint
import numpy as np


def r_data(d_s):
    d = [int(x) for x in d_s.split()]
    return d


data_s = '''125 17
'''
data = r_data(data_s)
with open('input11.txt') as f:
    data_s = f.read()
data = r_data(data_s)
pprint(data)


def rules(stone):
    if stone == 0:
        return [1]
    if int(log10(stone)) % 2 == 1:
        return [stone // (10 ** (int(log10(stone) + 1) // 2)), stone % (10 ** (int(log10(stone) + 1) // 2))]
    return [2024 * stone]





all_stones_count = {stone: 1 for stone in data}

def tree(all_stones_count):
    new_stones_count = {s:0 for s in all_stones_count}
    for s in all_stones_count:
        if all_stones_count[s] > 0:
            for stone in rules(s):
                if stone in new_stones_count:
                    new_stones_count[stone] += all_stones_count[s]
                else:
                    new_stones_count[stone] = all_stones_count[s]
    return new_stones_count


for i in range(75):
    all_stones_count = tree(all_stones_count)
pprint(all_stones_count)
pprint(sum(all_stones_count.values()))
