with open('input3.txt') as f:
    data = f.read()


def f1(data):
    data1 = data.split('mul(')
    data2 = [d[:d.find(')')] for d in data1 if d.find(')') > 3]
    data3 = [d.split(',') for d in data2 if ',' in d and len(d.split(',')) == 2]
    data4 = [int(a) * int(b) for a, b in data3 if all(x.isdigit() for x in a) and all(x.isdigit() for x in b)]
    return sum(data4)


print(f1(data))


def f2(data):
    data1 = data.split('do()')
    data2 = [d.split("don't")[0] for d in data1]
    return data2


print(sum([f1(d) for d in f2(data)]))

import pandas as pd

def f1(data):
    # Найдем все 'mul(num,num)' в строке
    df = pd.DataFrame(data.splitlines(), columns=['line'])
    df = df['line'].str.extractall(r'mul\((\d+),(\d+)\)')

    df = df.astype(int)
    df['result'] = df[0] * df[1]
    return df['result'].sum()

def f2(data):
    # Разделим данные по 'do()' и обработаем каждый сегмент
    data_list = data.split('do()')
    df = pd.DataFrame(data_list, columns=['segment'])
    df['segment'] = df['segment'].str.split("don't").str[0]
    return df['segment'].tolist()

# Прочитаем содержимое файла
with open('input3.txt') as f:
    data = f.read()

# Обработаем данные
data_list = f2(data)
total_sum = sum(f1(d) for d in data_list)
print(total_sum)

