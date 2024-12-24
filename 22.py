from itertools import product, repeat
from pprint import pprint
from time import time

from numba import njit

data_s = '''
1
2
3
2024
'''
data_s = open("input22.txt").read()
data = list(map(int, data_s.strip().split()))
print(data)

modulo = 16777216


def secret(code):
    first = ((code * 64) ^ code) % modulo
    second = ((first // 32) ^ first) % modulo
    return ((second * 2048) ^ second) % modulo


print(sum([(lambda sec: [(sec := secret(sec)) for _ in range(2000)][-1])(d) for d in data]))

prices = []
changes = []
for d in data:
    sec = d
    price = list(zip(*([(d, d % 10)] + [((sec := secret(sec)), sec % 10) for _ in range(2000)])))[1]
    change = tuple(b - a for a, b in zip(price[:-1], price[1:]))
    prices.append(price)
    changes.append(change)


magics = []
for lend in range(len(data)):
    magic = {}
    for i in range(1, 1997):
        if (changes[lend][i - 1], changes[lend][i], changes[lend][i + 1], changes[lend][i + 2]) not in magic:
            magic[(changes[lend][i - 1], changes[lend][i], changes[lend][i + 1], changes[lend][i + 2])] = prices[lend][i + 3]
    magics.append(magic)


# print(prices)
# print(changes)


def get_seq(lend, seq):
    magic = magics[lend]
    try:
        return magic[seq]
    except:
        return 0


t = time()
res = []
for seq in product(range(-9,10), repeat=4):
    res.append(sum([get_seq(lend, seq) for lend in range(len(data))]))
print(max(res))
print(time()-t)
