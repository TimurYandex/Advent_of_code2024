from pprint import pprint

with open('input4.txt') as f:

    data = [[w for w in s] for s in map(str.strip, f.readlines())]
count = 0

print(len(data))
print(len(data[0]))

d = [[w for w in s] for s in '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''.split()]
print(d)

def count_list(r):
    lines = ['XMAS', 'SAMX']
    return sum([sum(["".join(x).count(line) for line in lines]) for x in r])


def count_half(d):
    width = len(d[0])
    height = len(d)
    NS = count_list(d)
    SW_list1 = [[d[j][i+j] for j in range(height - i)] for i in range(width-3)]
    SW_list2 = [[d[i + j][j] for j in range(width - i)] for i in range(1, height - 3)]
    SW_lists = SW_list1 + SW_list2
    SW = count_list(SW_lists)
    return NS + SW

def count_all(d):
    res1 = count_half(d)
    d1 = [[d[len(d)-j-1][i] for j in range(len(d))] for i in range(len(d))]
    res2 = count_half(d1)
    return res1 + res2



print(count_all(data))

def second(d):
    count = 0
    patterns = ['MMSSA', 'SSMMA', 'MSMSA', 'SMSMA']
    for i in range(len(d)-2):
        for j in range(len(d) - 2):
            m = "".join([d[i][j], d[i][j+2], d[i+2][j], d[i+2][j+2], d[i+1][j+1]])
            if m in patterns:
                count += 1
    return count

print(second(data))
