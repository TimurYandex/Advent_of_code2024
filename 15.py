def show():
    print(*["".join(f) for f in field], sep="\n")


data_s = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

# data_s = '''#######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######
#
# <vv<<^^<<^^
# '''

data_s = open("input15.txt").read()


field = [list(s) for s in data_s.split('\n\n')[0].split()]
movement = data_s.split('\n\n')[1].replace('\n', '')
print(field)
print(movement)
show()
tall = len(field)
wide = len(field[0])
walls = set()
boxes = set()
for i in range(tall):
    for j in range(wide):
        if field[i][j] == '@':
            robot = (i, j)
        if field[i][j] == 'O':
            boxes.add((i, j))
        if field[i][j] == '#':
            walls.add((i, j))

moves = {'<': (0, -1),
         '>': (0, 1),
         '^': (-1, 0),
         'v': (1, 0)}


def apply(place, move):

    return tuple(moves[move][i] + place[i] for i in range(2))


def make_move(move):
    changes = []
    check = apply(robot, move)
    while check not in walls and check in boxes:
        check = apply(check, move)
    if not check in walls:
        changes.append(robot)
        check = apply(robot, move)
        while check in boxes:
            changes.append(check)
            check = apply(check, move)
    return changes


def update(field):
    for j in range(tall):
        for i in range(wide):
            field[j][i] = '.'
    for wall in walls:
        field[wall[0]][wall[1]] = '#'
    for box in boxes:
        field[box[0]][box[1]] = 'O'
    field[robot[0]][robot[1]] = '@'


for move in movement:
    new_robot = robot
    cells = set(make_move(move))
    new_boxes = set()
    for cell in cells:
        new = apply(cell, move)
        if cell == robot:
            new_robot = new
        if cell in boxes:
            new_boxes.add(new)
    boxes = boxes - cells
    boxes = boxes | new_boxes
    robot = new_robot
    update(field)
show()

print(robot)
print(boxes)
print(sum([100 * a + b for a, b in boxes]))

data_s = data_s.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')

# data_s = '''##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##############
#
# ^^
# '''

field = [list(s) for s in data_s.split('\n\n')[0].split()]
movement = data_s.split('\n\n')[1].replace('\n', '')
print(field)
print(movement)
show()
tall = len(field)
wide = len(field[0])
boxes_left = set()
boxes_right = set()
walls = set()
for i in range(tall):
    for j in range(wide):
        if field[i][j] == '@':
            robot = (i, j)
        if field[i][j] == '[':
            boxes_left.add((i, j))
            boxes_right.add((i, j + 1))
        if field[i][j] == '#':
            walls.add((i, j))
boxes = boxes_left | boxes_right


def update_wide(field):
    for j in range(tall):
        for i in range(wide):
            field[j][i] = '.'
    for wall in walls:
        field[wall[0]][wall[1]] = '#'
    for box in boxes:
        field[box[0]][box[1]] = '[' if box in boxes_left else ']'
    field[robot[0]][robot[1]] = '@'


update_wide(field)
show()


def get_children(point, move):
    res = set()
    to_be = apply(point, move)
    if to_be in boxes:
        left = to_be if to_be in boxes_left else (to_be[0], to_be[1] - 1)
        right = to_be if to_be in boxes_right else (to_be[0], to_be[1] + 1)
        res |= {left, right}
    return res


def get_tree(point, move):
    res = {point}
    children = get_children(point, move)
    res |= children
    if children:
        for child in children:
            if move == '<' and child in boxes_left or move == '>' and child in boxes_right or move == '^'  or move == 'v':
                for elem in get_tree(child, move):
                    res.add(elem)
    return res

def check_tree(tree, move):
    if any([apply(node, move) in walls for node in tree]):
        return False
    return True

def move_tree(tree,move):
    global boxes_left
    global boxes_right
    global boxes
    global robot
    new_left_tree = set()
    new_right_tree = set()
    for node in tree:
        if node in boxes_left:
            new_left_tree.add(apply(node, move))
        elif node in boxes_right:
            new_right_tree.add(apply(node, move))
        else:
            robot = apply(node, move)
    boxes_left -= tree
    boxes_right -= tree
    boxes_left |= new_left_tree
    boxes_right |= new_right_tree
    boxes = boxes_left | boxes_right


for move in movement:

    t = get_tree(robot, move)
    if check_tree(t, move):
        move_tree(t, move)
        update_wide(field)
    # show()

print(sum([100 * a + b for a, b in boxes_left]))


