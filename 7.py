from itertools import combinations, product
from pprint import pprint


class ConcatInt(int):
    def __or__(self, other):
        if isinstance(other, int):
            # Конкатенация чисел
            return ConcatInt(int(f"{self}{other}"))
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, int):
            # Сложение чисел, результат — ConcatInt
            return ConcatInt(super().__add__(other))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int):
            # Умножение чисел, результат — ConcatInt
            return ConcatInt(super().__mul__(other))
        return NotImplemented


def r_data(d_s):
    return {int(a): tuple(b.split()) for a, b in [x.split(': ') for x in d_s.split('\n')][:-1]}


with open('input7.txt') as f:
    d_s = f.read()
data = r_data(d_s)
# pprint(data)

d = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
# data = r_data(d)
pprint(data)


def equation(res: int, data: tuple[int]):
    operations = '+*|'
    variants = [[operations[o] for o in comb] for comb in product(range(len(operations)), repeat=len(data) - 1)]
    # print(res)
    # print(data)
    # print(variants)
    candidates = list(map(eval,
                          ["(" * len(v) + "ConcatInt("+data[0]+")" + "".join(["".join(v[i] + "ConcatInt("+data[i + 1]) + "))" for i in range(len(v))])
                           for v in variants]))
    # print(candidates)
    return res if (res in candidates) else 0

# print(sum([equation(a, b) for a, b in data.items()]))

def equation1(res: int, data: tuple[int]):
    operations = (0,1,2)
    variants = [[operations[o] for o in comb] for comb in product(range(len(operations)), repeat=len(data) - 1)]
    d = tuple(map(int, data))
    candidates = []

    for v in variants:
        evaluation = d[0]
        for i in range(len(v)):
            if v[i] == 0:
                evaluation += d[i+1]
            elif v[i] == 1:
                evaluation *= d[i + 1]
            else:
                evaluation = int(f"{evaluation}{d[i + 1]}")
        candidates.append(evaluation)
    return res if (res in candidates) else 0

print(sum([equation1(a, b) for a, b in data.items()]))