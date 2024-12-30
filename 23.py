import sys

sys.setrecursionlimit(6000)
from functools import reduce
from itertools import combinations
from pprint import pprint

data_s = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''

data_s = open("input23.txt").read()

data = [d.split("-") for d in data_s.strip().splitlines()]

print("".join(sorted(list(reduce(set.union, [set(pair[0]) | set(pair[1]) for pair in data])))))
edges = set([frozenset(pair) for pair in data])
tedges = set([frozenset(pair) for pair in data if pair[0].startswith('t') or pair[1].startswith('t')])
pprint(len(edges))
pprint(len(tedges))
res = []
for f, g in combinations(tedges, 2):
    if len(f | g) == 3:
        fg = f & g
        # print(f, g, fg, (g - fg), (f - fg), frozenset(((g - fg), (f - fg))))
        if frozenset((tuple(g - fg)[0], tuple(f - fg)[0])) in edges:
            res.append(frozenset(f | g))

pprint(res)
pprint(len(set(res)))


def edges_to_inci(edges):
    vert = set()
    for e in edges:
        for v in e:
            vert.add(v)
    vertices = {v: set() for v in vert}
    for v1 in vert:
        for v2 in vert:
            edge = frozenset((v1, v2))
            if edge in edges:
                vertices[v1].add(v2)
    return vertices


graf = edges_to_inci(edges)

pprint(graf)

pprint([(k, len(graf[k])) for k in graf])
pprint(sorted([(len(graf[k]), k) for k in graf]))
pprint(max([len(graf[k]) for k in graf]))
pprint(min([len(graf[k]) for k in graf]))

t = [v for v in graf if v.startswith("t")]
print(t)


def dfs(stack, passed, clique):
    if not stack:
        return clique
    new = stack.pop()
    for ch in graf[new]:
        if ch not in passed and ch not in clique:
            stack.append(ch)
    if all([frozenset((new, cl)) in edges for cl in clique]):
        clique.add(new)
    else:
        passed.add(new)
    return dfs(stack, passed, clique)


cliques = set()
for ti in t:
    clique = set()
    cliques.add(frozenset(dfs([ti], set(), clique)))
res = [",".join(sorted(list(cl))) for cl in cliques]
print(max(res, key=len))
