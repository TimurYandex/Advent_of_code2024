from functools import partial
from operator import matmul


class Mlist():
    def __init__(self, s):
        if isinstance(s, str):
            self._s = [s]
        elif isinstance(s, Mlist):
            self._s = s._s
        else:
            self._s = s

    def bind(self, func):
        new = []
        for e in self._s:
            new.extend(func(e)._s)
        return Mlist(new)

    def __repr__(self):
        return f"Mlist({self._s})"


with open("input14.txt") as f:
    data_s = Mlist(f.read())

# data_s = Mlist('''p=0,4 v=0,1
# p=6,3 v=0,1
# p=10,3 v=0,1
# p=2,0 v=0,1
# p=0,0 v=0,1
# p=3,0 v=-0,1
# ''')

data_split = (data_s.bind(lambda x: Mlist(x.split("\n")))
              .bind(lambda x: Mlist(x.split("\n")))
              .bind(lambda x: Mlist(x.split(" ")))
              .bind(lambda x: Mlist(x.split("=")))
              .bind(lambda x: Mlist(x.split(","))))

p = list(zip(data_split._s[1::6], data_split._s[2::6]))
v = list(zip(data_split._s[4::6], data_split._s[5::6]))
data = [{'p': p0, 'v': v0} for p0, v0 in zip(p, v)]

wide = 101
tall = 103
# wide = 11
# tall = 7
time = 100


def show(d):
    print()
    print()
    print()
    positions = [dd['p'] for dd in d]
    positions_dict = {}
    for pos in positions:
        if pos in positions_dict:
            positions_dict[pos] += 1
        else:
            positions_dict[pos] = 1
    for j in range(tall):
        for i in range(wide):
            if (str(i), str(j)) in positions_dict:
                print(positions_dict[(str(i), str(j))], end="")
            else:
                print('.', end="")
        print()


def where(robot, time, data):
    x, y = map(int, data[robot]['p'])
    vx, vy = map(int, data[robot]['v'])
    new_x = (x + vx * time) % wide
    new_y = (y + vy * time) % tall
    return new_x, new_y


mid_x = wide // 2
mid_y = tall // 2
count = [0] * 4


def step(d,i):
    new_d = []
    for r in range(len(d)):
        x, y = where(r, i, d)
        new_d.append({'p': (str(x), str(y)), 'v': d[r]['v']})
    return new_d


for r in range(len(data)):
    x, y = where(r, time, data)
    if x > mid_x and y > mid_y:
        count[0] += 1
    elif x > mid_x and y < mid_y:
        count[1] += 1
    elif x < mid_x and y > mid_y:
        count[2] += 1
    elif x < mid_x and y < mid_y:
        count[3] += 1
from functools import reduce
from operator import mul
mul_count = reduce(mul, count)
print(mul_count)


for i in range(10000):
    count = [0] * 4
    for r in range(len(data)):
        x, y = where(r, i, data)
        if x > mid_x and y > mid_y:
            count[0] += 1
        elif x > mid_x and y < mid_y:
            count[1] += 1
        elif x < mid_x and y > mid_y:
            count[2] += 1
        elif x < mid_x and y < mid_y:
            count[3] += 1

    if reduce(mul, count) < 0.5*mul_count:
        d = data.copy()
        show(step(d, i))
        print(count)
        print(i)


