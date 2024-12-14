

with open('input1.txt') as f:
    data = list(map(lambda x: [int(y) for y in x.split()],f.read().splitlines()))

a = sorted([x[0] for x in data])
b = sorted([-x[1] for x in data], reverse=True)
print(sum([abs(sum(x)) for x in zip(a,b)]))
b = sorted([x[1] for x in data])
d = {}
for x in a:
    d[x] = 0
for x in b:
    if x in d:
        d[x] += 1

print(sum([x * d[x] for x in a]))
