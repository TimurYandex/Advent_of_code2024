from functools import reduce
from itertools import combinations, product
from pprint import pprint
import numpy as np


def r_data(d_s):
    d = d_s.split()
    return d


data_s = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
data = r_data(data_s)
with open('input01.txt') as f:
    data_s = f.read()

data = r_data(data_s)

pprint(data)
digits = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
data = list(map(lambda x: x.replace('eightwo', 'eighttwo'), data))
data = list(map(lambda x: x.replace('nineight', 'nineeight'), data))
data = list(map(lambda x: x.replace('sevenine', 'sevennine'), data))
data = list(map(lambda x: x.replace('fiveight', 'fiveeight'), data))
data = list(map(lambda x: x.replace('eighthree', 'eightthree'), data))
data = list(map(lambda x: x.replace('threeight', 'threeeight'), data))
data = list(map(lambda x: x.replace('oneight', 'oneeight'), data))
data = list(map(lambda x: x.replace('twone', 'twoone'), data))
for d in digits:
    data = list(map(lambda x: x.replace(d, digits[d]), data))

data1 = data.copy()
for d in "123456789":
    data1 = list(map(lambda x: x.replace(d, "0"), data1))
print(data1)
print([(x, y) for x, y in zip(data1, data)])
print(sum([int(x + y) for x, y in
           map(lambda s: (s[1][s[0].find("0")], s[1][s[0].rfind("0")]), [(x, y) for x, y in zip(data1, data)])]))
