import operator

from functools import reduce
from itertools import product
from pprint import pprint


def show():
    print(*["".join(f) for f in field], sep="\n")


data_s = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''

data_s = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''
# data_s = '''#####
# #..E#
# #S.##
# #####
# '''
data_s = open("input16.txt").read()


field = [list(s) for s in data_s.split()]
show()
tall, wide = len(field), len(field[0])
directions = {'>': (0, 1),
              '<': (0, -1),
              '^': (-1, 0),
              'v': (1, 0)
              }
possible = {'>': 'v^',
            '<': 'v^',
            '^': '<>',
            'v': '<>'
            }
opposite = {'>': '<',
            '<': '>',
            '^': 'v',
            'v': '^'
            }
same = {'>': '>',
            '<': '<',
            '^': '^',
            'v': 'v'
            }


def neib(*args):
    if len(args) == 2:
        return neib2(*args)
    else:
        return neib1(*args)

def neib2(point, direction):
    vx, vy = directions[direction]
    x, y = point
    return (x + vx, y + vy)

def neib1(node):
    point = (node[0], node[1])
    d = node[2]
    return neib(point, d)


def neibs(point):
    return [neib(point, d) for d in directions]


def path_cost(path):
    cost = 0
    direction = path[0]
    for step in path[1:]:
        if direction != step:
            cost += 1000
        else:
            cost += 1
        direction = step
    return cost


print(path_cost('>^^^^>>>^^^>>>>>>>>>vvvvvvv>>>^^^^^^^^^^^^^^'))
print(path_cost('>'))
print(path_cost('>^'))

walls = set()
graph = {}
costs = {}

for i, j in product(range(tall), range(wide)):
    if field[i][j] == '#':
        walls.add((i, j))
for i, j in product(range(tall), range(wide)):
    if field[i][j] == 'S':
        start = (i, j, ">")
    elif field[i][j] == 'E':
        finishes = [(i, j, ">"), (i, j, "<"), (i, j, "^"), (i, j, "v")]

    if (i, j) not in walls:
        for d in directions:
            n = neib((i, j), d)
            costs[(i, j, d)] = 10 ** 20
            graph[(i, j, d)] = {}
            if (n[0], n[1]) not in walls:
                graph[(i, j, d)][(n[0], n[1], d)] = 1
            for dd in directions:
                if dd in possible[d]:
                    graph[(i, j, d)][(i, j, dd)] = 1000


costs[start] = 0
parents = {}
for k in costs:
    parents[k] = set()
for n in neibs((start[0],start[1])):
    if n in costs:
        parents[n].add(start)
pprint(costs)
print()
pprint(graph)
print()
pprint(parents)

processed = set()
setcosts = set(costs.keys())

def find_lowest_cost_node(costs):
    unseen = setcosts - processed
    if unseen:
        return min((node for node in unseen), key=lambda x:costs[x])
    else:
        return None

# Find the lowest-cost node that you haven't processed yet.
node = find_lowest_cost_node(costs)
# If you've processed all the nodes, this while loop is done.
while node is not None:
    print(len(processed))
    cost = costs[node]
    # Go through all the neighbors of this node.
    neighbors = graph[node]
    for n in neighbors:
        new_cost = cost + neighbors[n]
        # If it's cheaper to get to this neighbor by going through this node...
        if costs[n] >= new_cost:
            # ... update the cost for this node.
            costs[n] = new_cost
            # This node becomes the new parent for this neighbor.
            parents[n].add(node)
    # Mark the node as processed.
    processed.add(node)
    # Find the next node to process, and loop.
    node = find_lowest_cost_node(costs)

print("Cost from the start to each node:")
pprint(costs)

def show_path(p):
    papaset = {p}
    for papa in parents[p]:
        papaset.add(papa)
        nextlevel = parents[papa]
        for n in nextlevel:
            papaset |= show_path(n)
    return papaset


smallest = min([costs[fin] for fin in finishes])
pathes = set()
for fin in finishes:
    if smallest == costs[fin]:
        pathes |= show_path(fin)
        print(pathes)
        print(costs[fin])
print("наименьший ", smallest)
print("длина всех мест вдоль какого-то пути", len(pathes))
for i in range(tall):
    for j in range(wide):
        if any([(i,j,d) in pathes for d in directions]):
            field[i][j] = "O"
show()
print(sum([s.count("O") for i in range(tall) for s in field[i]]))
