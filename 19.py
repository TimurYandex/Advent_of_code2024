from time import time

import numpy as np
from numba import njit

data_s = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''
data_s = open("input19.txt").read()
parts, strings = data_s.split("\n\n")[0].split(', '), data_s.split("\n\n")[1].strip().split('\n')
print(parts, strings)


def check_str(s: str, parts: [str]) -> bool:
    dyn = [False] * (len(s) + 1)
    dyn[0] = True
    for i in range(len(s) + 1):
        dyn[i] |= any([dyn[i - len(part)] for part in parts if s[:i].endswith(part)])
    return dyn[len(s)]


print(len(strings))


# print(sum([1 for s in strings if check_str(s, parts)]))


def check_str_int(s: str, parts: [str]) -> int:
    dyn = [0] * (len(s) + 1)
    dyn[0] = 1
    for i in range(len(s) + 1):
        dyn[i] += sum([dyn[i - len(part)] for part in parts if s[:i].endswith(part)])

    return dyn[len(s)]


t = time()
print(sum([check_str_int(s, parts) for s in strings]))
print(time()-t)


def check_str_both(s: str, parts: [str]) -> int:
    dyn = [0] * (len(s) + 1)
    dyn[0] = 1
    dyn1 = [False] * (len(s) + 1)
    dyn1[0] = True
    for i in range(len(s) + 1):
        dyn[i] += sum([dyn[i - len(part)] for part in parts if s[:i].endswith(part)])
        dyn1[i] |= any([dyn[i - len(part)] for part in parts if s[:i].endswith(part)])

    return dyn[len(s)], dyn1[len(s)]

# print(*tuple(map(sum, zip(*[check_str_both(s, parts) for s in strings]))))

def check_str_int_numpy(s: str, parts: [str]) -> int:
    dyn = np.zeros((len(s) + 1), dtype=np.int64)
    dyn[0] = 1
    k = max(len(p) for p in parts)
    ss = [s[i-k:i] for i in range(len(s)+1)]
    for i in range(len(s) + 1):
        dyn[i] = sum([dyn[i - len(part)] for part in parts if ss[i].endswith(part)])

    return dyn[len(s)]


t = time()
print(sum([check_str_int_numpy(s, parts) for s in strings]))
print(time()-t)
