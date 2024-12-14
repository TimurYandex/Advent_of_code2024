from functools import reduce
from itertools import combinations, product
from pprint import pprint

import numpy as np


def r_data(d_s):
    file_size = list(map(int, list(d_s.strip()) + ['0']))
    return dict([(i, f) for i, f in enumerate(zip(file_size[::2], file_size[1::2]))])


with open('input9.txt') as f:
    data_s = f.read()

d_s = '''2333133121414131402
'''

d_s = data_s

data = r_data(d_s)
length = len(data)


def dict_repr(d):
    return d.copy()


def list_repr(data):
    return np.array(reduce(lambda x, y: x + y, [[i] * data[i][0] + [None] * data[i][1] for i in data]))


def string_repr(data):
    return "".join([str(i) * data[i][0] + '.' * data[i][1] for i in data])


disk = list_repr(data)
data_backwards = []
for i, d in enumerate(disk[::-1]):
    if d is not None:
        data_backwards.append(d)
free_spaces = []
for i, d in enumerate(disk):
    if d is None:
        free_spaces.append(i)
backw = np.array(data_backwards)
free_spaces_size = len(disk[disk == None])
data_size = len(disk) - free_spaces_size
# for i in range(free_spaces_size):
#     try:
#         disk[free_spaces[i]] = backw[i]
#     except:
#         break
# final = disk[:data_size]
# print(sum([i * x for i, x in enumerate(final)]))
# print(string_repr(data))
# print(list_repr(data))
# print(dict_repr(data))
free_list = []
files_list = []
dd = dict_repr(data)
last_free = 0
for d in dd:
    files_list.append((d, dd[d][0], last_free))
    free_list.append([dd[d][0] + last_free, dd[d][1]])
    last_free += (dd[d][0] + dd[d][1])
# print(files_list)
# print(free_list)
# print(files_list[::-1])
# print(free_spaces_size)
# print(len(free_list))
# print("".join(list(map(lambda x: '.' if x is None else str(x), disk))))
for f in files_list[::-1]:
    file_start = f[2]
    for free in free_list:
        if free[1] >= f[1] and free[0] < f[2]:
            for i in range(f[1]):
                disk[free[0]+i] = f[0]
                disk[file_start + i] = None
            free[1] -= f[1]
            free[0] += f[1]
            break
# print("".join(list(map(lambda x: '.' if x is None else str(x), disk))))
# print('00992111777.44.333....5555.6666.....8888..')
final = disk
print(sum([i * (x if x is not None else 0) for i, x in enumerate(final)]))
print(list(final))