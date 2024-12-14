with open('input2.txt') as f:
    data = list(map(lambda x: [int(y) for y in x.split()],f.read().splitlines()))
diffs1 = [set([(b-a) for a,b in zip(d[1:],d[:-1])]) for d in data]
diffs = len([x for x in diffs1 if x | {1,2,3} == {1,2,3} or x | {-1,-2,-3} == {-1,-2,-3}])
print(diffs)

def safe(x):
    for i in range(len(x)):
        y = x[:i] + x[i+1:]
        s = set([(b - a) for a, b in zip(y[1:], y[:-1])])
        if s | {1,2,3} == {1,2,3} or s | {-1,-2,-3} == {-1,-2,-3}:
            return True
    return False

print(len([d for d in data if safe(d)]))

