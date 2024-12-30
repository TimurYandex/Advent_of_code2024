from pprint import pprint

import numpy as np

data_s = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

data_s = open("input25.txt").read()
def get_data(d):
    locks, keys = [], []
    locks_n_keys = d.strip().split('\n\n')
    for k in locks_n_keys:
        table = [list(k) for k in k.strip().split()]
        is_key = any([table[0][i] == '.' for i in range(len(table[0]))])
        trans = [[table[i][j] for i in range(len(table))] for j in range(len(table[0]))]
        forma = [t.count("#") - 1 for t in trans]
        if is_key:
            keys.append(forma)
        else:
            locks.append(forma)
    return locks, keys


data = get_data(data_s)

pprint(data)

locks, keys = np.array(data[0], dtype=np.uint32), np.array(data[1], dtype=np.uint32)
pprint(locks)
pprint(keys)
def overlap(locks, keys):
    sums = locks[:, None] + keys[None, :]
    max_sums = np.max(sums, axis=2)
    return np.sum(max_sums < 6)


print(overlap(locks, keys))

