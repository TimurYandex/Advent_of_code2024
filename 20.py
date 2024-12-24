from itertools import product
from pprint import pprint


def show():
    print(*["".join(f) for f in field], sep="\n")


def show_wide():
    print(*[" ".join([f"{str(ff):>2}" for ff in f]) for f in field], sep="\n")


data_s = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''

data_s = open("input20.txt").read()

field = [list(s) for s in data_s.split()]
field_set = set()
show()
tall, wide = len(field), len(field[0])
walls = set()
for i, j in product(range(tall), range(wide)):
    field_set.add((i, j))
    if field[i][j] == '#':
        walls.add((i, j))
for i, j in product(range(tall), range(wide)):
    if field[i][j] == 'S':
        start = (i, j)
    elif field[i][j] == 'E':
        finish = (i, j)
print(start, finish)


def neibs(point):
    return [(point[0] + d[0], point[1] + d[1]) for d in [(1, 0), (0, 1), (-1, 0), (0, -1)] if
            (point[0] + d[0], point[1] + d[1]) in field_set]


def get_path(field):
    path = [start]
    current = start
    previous = None
    while current != finish:
        for n in neibs(current):
            if n in walls or n == previous:
                continue
            path.append(n)
            previous = current
            current = n
            break

    # path.append(finish)
    return path


path = get_path(field)
path_set = set(path)
path_inverse = {path[i]: i for i in range(len(path))}


def neibs_walls(p):
    return [n for n in neibs(p) if n in walls]


def can_get_to(p):
    maybe_cheats1 = neibs_walls(p)
    maybe_cheats2 = {}
    for cheat in maybe_cheats1:
        for n in neibs(cheat):
            if n != p and n in path_set:
                if cheat in maybe_cheats2:
                    maybe_cheats2[cheat] |= {n}
                else:
                    maybe_cheats2[cheat] = {n}
    cheats = [(cheat1, cheat2) for cheat1 in maybe_cheats1 if cheat1 in maybe_cheats2 for cheat2 in
              maybe_cheats2[cheat1]]
    return cheats


cheats_count = {}
i = 0
for p in path:
    field[p[0]][p[1]] = i
    savings = [path_inverse[t[1]] - i - 2 for t in can_get_to(p) if path_inverse[t[1]] > i + 2]
    can_get = [(t, path_inverse[t[1]]) for t in can_get_to(p) if path_inverse[t[1]] > i + 2]
    for save in savings:
        if save in cheats_count:
            cheats_count[save] += 1
        else:
            cheats_count[save] = 1
    # print(f"{i}: {p}, "
    #       f"can_get_to: {can_get}, "
    #       f"saving: {savings}")
    # show_wide()
    i += 1


# print(cheats_count)
# print(sum([cheats_count[i] for i in cheats_count if i >= 100]))

def get_cheats(p, k):
    may_be_cheats = {}
    for i in range(-k, k + 1):
        for j in range(-k, k + 1):
            if abs(i) + abs(j) <= k and not (i == j == 0):
                point = (p[0] + i, p[1] + j)
                if point in field_set and point in path_set:
                    may_be_cheats[point] = abs(i) + abs(j)
    return may_be_cheats


cheats_count = {}
i = 0
for p in path:
    cheats_on_path = get_cheats(p, 20)
    savings = [path_inverse[t] - i - cheats_on_path[t] for t in cheats_on_path if
               path_inverse[t] > i + cheats_on_path[t]]
    can_get = [(t, path_inverse[t]) for t in cheats_on_path if path_inverse[t] > i + 2]

    for save in savings:
        if save in cheats_count:
            cheats_count[save] += 1
        else:
            cheats_count[save] = 1
    # print(
    #     f"{i}: {p}, "
    #     f"can_get_to: {can_get}, "
    #     f"saving: {savings}")
    # # show_wide()
    i += 1

print(cheats_count)
print(sum([cheats_count[i] for i in cheats_count if i >= 100]))
