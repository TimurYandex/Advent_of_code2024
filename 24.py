from itertools import combinations, product
from pprint import pprint

data_s = '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''

data_s = open("input24.txt").read()


def f_and(a, b):
    return a and b


def f_or(a, b):
    return a or b


def f_xor(a, b):
    return a ^ b


def make_func(s):
    x, op, y, arrow, r = s.split()
    if op == "AND":
        return x, y, r, f_and
    if op == "OR":
        return x, y, r, f_or
    if op == "XOR":
        return x, y, r, f_xor


def get_data(d):
    a, b = d.strip().split('\n\n')
    starts = dict(zip(map(lambda x: x[:-1], a.strip().split()[::2]), map(int, a.strip().split()[1::2])))
    funcs = list(map(make_func, b.strip().split('\n')))
    return starts, funcs


data = get_data(data_s)
values = data[0]
functions = data[1]
wires = {f[2]: (f[0], f[1], f[3]) for f in functions}
wires_original = wires.copy()


# connections = {(f[0], f[1], f[2]): f[3] for f in functions}

def update_dependencies(wrs):
    args = {a[0] for a in wrs.values()} | {a[1] for a in wrs.values()}
    deps = {arg: [] for arg in args}
    for w in wrs:
        deps[wrs[w][0]].append(w)
        deps[wrs[w][1]].append(w)
    return deps


depends = update_dependencies(wires)
depends_original = depends.copy()
unknown = list(wires.keys())

print("wires", wires)
print("values", values)
print("functions", functions)
# print("connections", connections)
print("unknown", unknown)
print("depends", depends)
# print(sorted([node for node in unknown if node.startswith("z")]))


finalrow = sorted([node for node in unknown if node.startswith("z")])


class Loop(Exception):
    ...


def make_levels(starting):
    level = 0
    levels = [starting]
    while any([n in wires.keys() for n in levels[-1]]):
        level += 1
        nextlevel = set()
        for n in levels[-1]:
            if n in wires.keys():
                a, b, _ = wires[n]
                nextlevel.add(a)
                nextlevel.add(b)
        levels.append(list(nextlevel))
        if len(levels) > 150:
            raise Loop
    levels.reverse()
    return levels


def run_net():
    for level in range(1, len(levels)):
        for u in levels[level]:
            if u in wires:
                a, b, f = wires[u]
                values[u] = f(values[a], values[b])

    lastlevel = sorted(levels[-1], reverse=True)

    # print("".join([val for val in lastlevel]))
    bi_str = "".join([str(values[val]) for val in lastlevel])

    # print("", num("x"))
    # print("", num("y"))
    # print(bi_str)
    # print(int(bi_str, 2))
    return "0" + num("x"), "0" + num("y"), bi_str, int(bi_str, 2)


def num(letter):
    lastlevel = [values[node] for node in sorted(values, reverse=True) if node.startswith(letter)]
    bi_str = "".join([str(val) for val in lastlevel])
    return bi_str


def make_x_key(i):
    return "x" + f"{i:02}"


def make_y_key(i):
    return "y" + f"{i:02}"


def test_n_bit(x, y):
    for xx in ["x" + f"{i:02}" for i in range(45)]:
        values[xx] = 0
    for yy in ["y" + f"{i:02}" for i in range(45)]:
        values[yy] = 0
    if x < 50:
        xn = "x" + f"{x:02}"
        values[xn] = 1
    if y < 50:
        yn = "y" + f"{y:02}"
        values[yn] = 1


def find_errors():
    err = set()
    for i in range(45):
        test_n_bit(i, i)
        x, y, z, zz = run_net()
        if y[1:] != z[:-1]:
            err.add(i)
    for i in range(45):
        test_n_bit(i, 99)
        x, y, z, zz = run_net()
        if x != z:
            err.add(i)
    for i in range(45):
        test_n_bit(99, i)
        x, y, z, zz = run_net()
        if y != z:
            err.add(i)
        res = list(err)
        res.sort()
    return res


def swap(a, b):
    wires[a], wires[b] = wires[b], wires[a]


# swap_forever('nfj', 'ncd')
# swap_forever('mrm', 'rjm')
# swap_forever('z37', 'vkg')
# swap_forever('msn', 'z20')
#

# levels = make_levels(finalrow)


def swap_wires(a, b, n):
    global wires, depends, arguments
    saved_wires = wires.copy()
    swap(a, b)
    update_dependencies(wires)
    errors = find_errors()
    update_dependencies(saved_wires)
    if len(errors) < n:
        return errors
    else:
        return None


def make_possible(known_errors):
    possible = set()
    for n in known_errors:
        possible.add(make_x_key(n))
        possible.add(make_y_key(n))
    return possible


def forward(starting, hope):
    final = [set(), set(starting)]
    new = set()
    while final[-1] != final[-2] and hope:
        for wire in final[-1]:
            if wire in depends.keys():
                for dependant in depends[wire]:
                    new.add(dependant)
        final.append(new | final[-1])
        hope -= 1
    return final[-1] - starting


to_swap = set()
levels = make_levels(finalrow)
known_errors_start = find_errors()
print("known_errors", known_errors_start)
possible_start = make_possible(known_errors_start)
print("possible", possible_start)
print("len(possible)", len(possible_start))


def update_swap(known_errors, possible, hope):
    global depends, levels
    size = len(known_errors)
    k = 0
    candidates = forward(possible, hope)
    print("len(candidates)", len(candidates))
    while size > 0:
        for a in candidates:
            for b in candidates:
                k += 1
                print(a, b, k)
                new_errors = swap_wires(a, b, size)
                if new_errors:
                    print("new_errors", new_errors, a, b)
                    swap(a, b)
                    try:
                        update_depends_and_levels()
                        possible = make_possible(new_errors)
                        print("len(possible)", len(possible))
                        candidates = forward(possible, hope)
                        print("len(candidates)", len(candidates))
                        size = len(new_errors)
                        to_swap.add(a)
                        to_swap.add(b)
                        k += 1000000
                        break
                    except Loop:
                        print(f"пропускаю пару {a}, {b}")
            else:
                continue
            break
        else:
            size = 0


#
# test_n_bit(19, 19)
# print(*run_net(), sep="\n")
# test_n_bit(15, 15)
# print(*run_net(), sep="\n")

def check(s):
    global depends, levels
    a, b = s.split()
    swap(a, b)
    depends = update_dependencies(wires)

    try:
        levels = make_levels(finalrow)
    except Loop:
        print("зациклились в слоях")

    print(a, b, find_errors())
    # update_all()


def update_depends_and_levels():
    global depends, levels, wires
    depends = update_dependencies(wires)
    try:
        levels = make_levels(finalrow)
    except Loop:
        print("зациклились в слоях")
        exit(1)


def update_all():
    global depends, levels, wires
    wires = wires_original.copy()
    update_depends_and_levels()


print()
# check('z15 z16')  # четко лечит 14 15 но портит 16
# check('nfj ncd')  # четко лечит 27 без влияния на остальные
# check('z20 msn')  # четко лечит 20 без влияния на остальные
# update_all()


# update_swap(known_errors_start, possible_start, 3)
def neibs(starting, distance):
    new = starting.copy()
    for _ in range(distance):
        cur = new.copy()
        for contact in cur:
            if contact in wires:
                try:
                    new.add(wires[contact][0])
                    new.add(wires[contact][1])
                except:
                    ...
            if contact in depends:
                try:
                    new.add(depends[contact][0])
                    new.add(depends[contact][1])
                except:
                    ...
    return new - starting


new = neibs(possible_start, 2)
print("len(new):", len(new))
comb = list(combinations(new, 2))
size = len(known_errors_start)

check('z00 z00')  #
check('nfj ncd')  # четко лечит 27 без влияния на остальные
check('z37 vkg')  # четко лечит 36 37 без влияния на остальные
check('cqr z20')  # четко лечит 19 20 без влияния на остальные
# check('z15 qnw')  # четко лечит 14 15 без влияния на остальные

known_errors_start = find_errors()
print("known_errors", known_errors_start)
possible_start = make_possible(known_errors_start)
possible_start = {'y14', 'x14', 'y15', 'x15'}
print("possible", possible_start)
print("len(possible)", len(possible_start))



for p in comb:
    print(p)
    a, b = p
    swap(a, b)
    depends = update_dependencies(wires)
    try:
        levels = make_levels(finalrow)
        new_errors = find_errors()
        if 14 not in new_errors and 15 not in new_errors:
            print(a, b, find_errors())
            break
            size -= 1
        swap(a, b)
        depends = update_dependencies(wires)
    except Loop:
        print("зациклились в слоях")
        swap(a, b)

'''cqr,ncd,nfj,qnw,vkg,z15,z20,z37'''

to_swap = {'nfj', 'ncd', 'z37', 'vkg', 'cqr', 'z20', 'z15', 'qnw'}
print(to_swap)
print("answer:", ",".join(sorted(list(to_swap))))
