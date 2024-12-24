from functools import cache
from itertools import permutations
from pprint import pprint

from numpy.f2py.crackfortran import vars2fortran

data_s = '''029A
980A
179A
456A
379A'''

data_s = open("input21.txt").read()
data = data_s.split()


def fprint(s):
    print()
    print(s + f" = \n{eval(s)}")


fprint("data")

pad0_s = '''789
456
123
 0A'''
pad1_s = ''' ^A
<v>'''
pad2_s = ''' ^A
<v>'''
pad3_s = ''' ^A
<v>'''


def make_pad_array(s):
    return [[w if w != ' ' else None for w in line] for line in s.split("\n")]


def make_pad_inverse(pad):
    inverse = {}
    for i in range(len(pad)):
        for j in range(len(pad[0])):
            inverse[pad[i][j]] = (i, j)
    return inverse


a_pad = make_pad_array(pad0_s)
inv_pad = make_pad_inverse(a_pad)
fprint("a_pad")
fprint("inv_pad")

pult = make_pad_array(pad1_s)
inv_pult = make_pad_inverse(pult)
fprint("pult")
fprint("inv_pult")

maxlevel = 1


def get_numpress(current, pressing, level):
    if level == maxlevel:
        return 0


arrows = {}
arrows[('<', 'v')] = {'>A'}
arrows[('<', '>')] = {'>>A'}
arrows[('<', '^')] = {'>^A'}
arrows[('<', 'A')] = {'>>^A', '>^>A'}
arrows[('v', '<')] = {'<A'}
arrows[('v', '>')] = {'>A'}
arrows[('v', '^')] = {'^A'}
arrows[('v', 'A')] = {'>^A', '^>A'}
arrows[('^', '<')] = {'v<A'}
arrows[('^', '>')] = {'v>A', '>vA'}
arrows[('^', 'v')] = {'vA'}
arrows[('^', 'A')] = {'>A'}
arrows[('>', '<')] = {'<<A'}
arrows[('>', '^')] = {'<^A', '^<A'}
arrows[('>', 'v')] = {'<A'}
arrows[('>', 'A')] = {'^A'}
arrows[('A', '<')] = {'v<<A', '<v<A'}
arrows[('A', '^')] = {'<A'}
arrows[('A', 'v')] = {'<vA', 'v<A'}
arrows[('A', '>')] = {'vA'}


def shortest(a, b):
    coord_a = inv_pad[a]
    coord_b = inv_pad[b]
    dx = coord_b[1] - coord_a[1]
    dy = coord_b[0] - coord_a[0]
    res = ""
    if dx > 0:
        res += ">" * dx
        if dy > 0:
            res += "v" * dy
        else:
            res += "^" * (-dy)
    elif dy > 0:
        res += "v" * dy
        res += "<" * (-dx)
    else:
        res += "^" * (-dy)
        res += "<" * (-dx)

    # <<^^
    result = set()
    for p in permutations(res):
        take_it = True
        w = list(coord_a)
        for z in p:
            if z == '^':
                w[0] -= 1
            elif z == 'v':
                w[0] += 1
            elif z == '<':
                w[1] -= 1
            elif z == '>':
                w[1] += 1
            else:
                raise Exception("Жопа")
            if a_pad[w[0]][w[1]] == None:
                take_it = False
        if take_it:
            result.add("".join(p) + "A")
    return result


numpad = {(a, b): shortest(a, b) for a in list(map(str, range(10))) + ["A"] for b in list(map(str, range(10))) + ["A"]}


fprint("numpad")
pprint(numpad)


def simple_routes(a, b):
    if a == b:
        return "A"
    if a in "<>^v" or b in "<>^v":
        return arrows[(a, b)]
    return numpad[(a, b)]


def pairs(s):
    ss = "A" + s
    return zip(ss[:-1], ss[1:])


s = '379A'

s1 = 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'
s2 = 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'


def num_steps_s(s, maxlevel, level=0):
    result = ""
    for p in pairs(s):
        if level == maxlevel:
            variants = simple_routes(*p)
            # print(f"variants = {variants}, {list(map(len,variants))} level = {level}, option level == maxlevel is {level == maxlevel}")
            result += min(variants, key=len)
        else:
            variants = [num_steps_s(sub, maxlevel, level + 1)
                        for sub in simple_routes(*p)]
            # print(f"variants = {variants}, {list(map(len,variants))} level = {level}, option level == maxlevel is {level == maxlevel}")
            result += min(variants, key=len)

    return result


@cache
def num_steps(s, maxlevel, level=0):
    if level == maxlevel:
        result = len(s)
    else:
        result = 0
        prev = "A"
        for cur in s:
            variants = [num_steps(sub, maxlevel, level + 1)
                            for sub in simple_routes(prev,cur)]
            result += min(variants)
            prev = cur
    return result


s = '179A'
summa = 0
for s in data:
    nums = num_steps(s, 26)
    summa += int(s[:-1]) * nums
    print(s)
    print(nums)
print(summa)
