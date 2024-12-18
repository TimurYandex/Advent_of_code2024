task = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''

task = '''Register A: 30886132
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,0,3,1,4,4,4,5,5,3,0'''

regs, pro = task.split("\n\n")
pointer = 0
ra = int(regs.split("\n")[0].split(": ")[1])
rb = int(regs.split("\n")[1].split(": ")[1])
rc = int(regs.split("\n")[2].split(": ")[1])


def registers():
    return [ra, rb, rc]


def make_pro(s):
    return list(map(int, program_string.split(",")))


program_string = pro.split(": ")[1]
program = make_pro(program_string)
print(program)
print(registers())

steps = [(command, operand) for command, operand in zip(program[::2], program[1::2])]
print(steps)


def combo(operand):
    if operand == 7:
        return None
    elif operand < 4:
        return operand
    else:
        return registers()[operand - 4]


for i in range(8):
    print(i, combo(i))

output_string = ''


def output(v):
    global output_string
    if output_string == '':
        output_string = str(v)
    else:
        output_string += "," + str(v)


def simulate(a):
    while a != 0:
        print("---")
        b = (a % 8 + 1 - 2 * (a % 8 % 2) + 4 - 8 * ((a % 8 + 1 - 2 * (a % 8 % 2)) // 4 % 2)) ^ (
                    a // (2 ** (a % 8 + 1 - 2 * (a % 8 % 2)))) % 8  # 4 4
        a = a // 8  # 0 3
        print(b)


print("simulation:")


def calculate(a):
    res = []
    while a != 0:
        b = a % 8
        left = b ^ 5
        res.append((left ^ (a // (2 ** (b ^ 1)))) % 8)
        a //= 8
    return res


# for i in range(10):
#     print()
#     print(i)
#     calculate(2956*8+i)
#


for i in range(8):
    for j in range(8):
        for k in range(8):
            for m in range(8):
                for n in range(8):
                    a = (((i * 8 + j) * 8 + k) * 8 + m) * 8 + n
                    if calculate(a)[-5:] == [4, 5, 5, 3, 0]:
                        print("a,i,j,k,m,n = ", a, i, j, k, m, n, end="     ")
                        print(calculate(a))
                        print()


def find_next_octadigit(previous: [int], aim: int) -> [int]:
    res = []
    for p in previous:
        for i in range(8):
            if calculate(p * 8 + i)[0] == aim:
                res.append(p * 8 + i)
    return res


next_found = [5]
for aim in program[::-1][1:]:
    next_found = find_next_octadigit(next_found, aim)
    print(next_found, calculate(next_found[0]))
    print(min(next_found))
print(program)


def instruction(opcode, operand):
    global pointer, ra, rb, rc
    if opcode == 0:
        ra //= 2 ** combo(operand)
    elif opcode == 1:
        rb ^= operand
    elif opcode == 2:
        rb = combo(operand) % 8
    elif opcode == 3:
        if ra != 0:
            pointer = operand - 2
    elif opcode == 4:
        rb ^= rc
    elif opcode == 5:
        output(combo(operand) % 8)
    elif opcode == 6:
        rb = ra // 2 ** combo(operand)
    elif opcode == 7:
        rc = ra // 2 ** combo(operand)
    else:
        return None
    pointer += 2
    return pointer


def run(program):
    while pointer + 1 < len(program):
        print("now", pointer)
        print("registers before: ", registers(), [bin(n) for n in registers()])
        print(program[pointer], program[pointer + 1])
        instruction(program[pointer], program[pointer + 1])
        print("registers after: ", registers(), [bin(n) for n in registers()])
        print("output", output_string)
        print("next", pointer)
        print("===")


def subs(s):
    subss = set()
    for i in range(0, len(s) - 1):
        for j in range(i, len(s)):
            r = s[i:j].strip(",")
            if len(r) > 0:
                subss.add(r)
    return subss


sub = subs(program_string)


def close(s1):
    global sub
    for s in sub:
        if s1.find(s) > -1:
            return len(s)
    return False


program_string = program_string[:]

program = make_pro(program_string)
sub = subs(program_string)

b = rb
c = rc


def run_with_arg(i):
    global pointer, ra, rb, rc, output_string, program_string
    pointer = 0
    output_string = ""
    ra = i
    rb = b
    rc = c
    run(program)
    print(pointer)
    print("output", output_string)
    print(program_string)

run_with_arg(202975183645226)
