# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 18


from functools import reduce


# GET DATA
with open("DATA.txt", 'r') as data_file:
    DATA = data_file.read().split('\n')


# UTILITY FUNCTIONS
def data2list(data):
    return [{'d': (s := d.split(' '))[0], 'l': int(s[1]), 'c': s[2][2:-1]}  for d in data]

def print_trench(trench):
    '''Print trench representation '''

    trench_char = [["#" if tile else ' ' for tile in line] for line in trench]

    # print top edge
    print("\r\u256d" + "\u257c" * len(trench[0]) + "\u256e")

    # print valley
    for line in trench_char:
        print("\r\u257d" + reduce(lambda x, y: x+y, line) + "\u257f")

    # print bottm edge
    print("\r\u2570" + "\u257e" * len(trench[0]) + "\u256f", flush=True, end='')

def trench2grid(trench):
    '''
    Converts trench to boolian grid representating valley with trench.
    
    Args:
    - trench: list of tuples (x, y) representing trench
    
    Returns:
    - trench_boolian: boolian grid representing valley with trench
    '''

    # find minimum values in both dimentions
    x_min = min(x for x, _ in trench)
    y_min = min(y for _, y in trench)

    # shift trench
    trench = [(x - x_min, y - y_min) for x, y in trench]

    # find maximum values
    x_max = max(x for x, _ in trench)
    y_max = max(y for _, y in trench)

    # create a boolian grid
    trench_boolian = [[False for _ in range(x_max + 1)] for _ in range(y_max + 1)]

    # populate boolian trench
    for x, y in trench:
        trench_boolian[y][x] = True

    return trench_boolian

def dug_trench(instruction, display=False):
    # set variables
    trench = []
    x, y = 0, 0

    # go through instructions
    for i in instruction:
        d, l = i['d'], i['l']

        # dig trench
        for _ in range(l):
            if d == 'R': x += 1
            if d == 'L': x -= 1
            if d == 'U': y -= 1
            if d == 'D': y += 1

            trench.append((x, y))

    # convert trench to grid
    grid = trench2grid(trench)

    # display trench
    if display:
        print("Trench:")
        print_trench(grid)
        print()
    
    return grid

def check_saddle(x, y, trench):
    '''Returns True if edge is saddle shaped (changes interior flag), else False'''
    # check current corner
    if trench[y+1][x]: current = True
    else: current = False

    # find beggining of edge
    while trench[y][x]:
        # check for edge
        if x == -1: break
        x -= 1

    x += 1
    
    # check other corner
    if trench[y+1][x]: other = True
    else: other = False
 
    # compare corners
    return not current == other

def dug_interior(trench, display=False):
    # initialize interior
    interior = [[False for _ in range(len(trench[0]))] for _ in range(len(trench))]

    # ommit first and last row 
    for y in range(1, len(trench) - 1):

        # set variables
        inside = False
        previous = False
        preprevius = False

        for x in range(len(trench[0])):
            
            # check for edge
            if previous and not trench[y][x]:
                    # vertical edge
                    if not preprevius:
                        inside = not inside
                    # horizontal edge
                    else:
                        # check if saddle shaped
                        if check_saddle(x-1, y, trench):
                            inside = not inside
                    
            # update previous
            preprevius = previous
            previous = trench[y][x]

            # update interior
            if inside: interior[y][x] = True

    interior = [[trench[y][x] or interior[y][x] for x in range(len(trench[0]))] for y in range(len(trench))]

    # display interior
    if display: 
        print("Interior:")
        print_trench(interior)
        print()

    # return interior area
    return sum(sum(row) for row in interior)

def data2list_hex(instructions):
    direction = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }
        
    # convert instructions
    instructions = [{'d': direction[instruction['c'][-1]], \
                     'l': int(instruction['c'][:-1], 16)} \
                    for instruction in instructions]
    
    return instructions

def get_point(instruction, previous=(0, 0)):
    '''Returns coordinates of the next point from insttruction dictionary (x_1, y_1)'''
    # set variables
    x, y = previous
    d, l = instruction['d'], instruction['l']

    # move to next point
    if   d == 'R': x += l
    elif d == 'L': x -= l
    elif d == 'U': y -= l
    elif d == 'D': y += l

    return (x, y)

def list_points(instructions):
    '''Returns list of corners of a poligon from instructions [(x_1, y_1),.. ]'''
    # initialize rectangles list
    points = [(0, 0)]

    # ppopulate rectangles
    for instruction in instructions:
        points.append(get_point(instruction, points[-1]))

    return points

def gausss_method(points):
    '''
    Returns area of a polygon from a list of corners
    https://en.wikipedia.org/wiki/Shoelace_formula
    Formula:
    Area = 0.5 * |(x1y2 + x2y3 + x3y4 + ... + xny1) - (y1x2 + y2x3 + y3x4 + ... + ynx1)|
    '''
    r = len(points) - 1

    sum1 = sum([points[i][0] * points[i+1][1] for i in range(r)]) + points[0][1] * points[r][0]
    sum2 = sum([points[i+1][0] * points[i][1] for i in range(r)]) + points[r][1] * points[0][0]

    return abs(sum1 - sum2) // 2

def trench_length(instructions):
    return sum([l['l'] for l in instructions]) // 2 + 1


def star1():
    print("Part 1:", dug_interior(dug_trench(data2list(DATA))))

def star2():
    # get instructions
    instructions = data2list_hex(data2list(DATA))

    # get interior and perimeter
    interior = gausss_method(list_points(instructions))
    perimeter = trench_length(instructions)

    # print results
    print("Part 2:", interior + perimeter)


star1()
star2()