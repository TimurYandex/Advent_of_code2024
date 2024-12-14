from pprint import pprint

with open('input5.txt') as f:

    order, data = f.read().split('\n\n')
data = [x.split(',') for x in data.strip().split()]
order = [tuple(x.split('|')) for x in order.strip().split()]
order.sort()
print(data)
print(order)
nums = set([a[0] for a in order]) | set([a[1] for a in order])
print(len(nums),sorted(list(nums)))
print(len(order))
print(len(data))
print(max([len(x) for x in data]))
brak = []
for seq in data:
    pairs = [(seq[i], seq[j]) for i in range(len(seq)) for j in range(len(seq)) if i<j]
    for p in pairs:
        if (p[1],p[0]) in order:
            brak.append(seq)
            break
good = [s for s in data if s not in brak]
count = 0
print(*[(i,s) for i,s in enumerate(data)], sep='\n')
print(*[(i,s) for i,s in enumerate(good)], sep='\n')
for g in good:
    count += int(g[len(g)//2])
print(count)

for seq in brak:
    for i in range(len(seq)):
        for j in range(len(seq)):
            if i < j:
                if (seq[j], seq[i]) in order:
                    seq[j], seq[i] = seq[i], seq[j]
count = 0
for g in brak:
    count += int(g[len(g) // 2])
print(count)




