# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 

# PARAMETERS
data_path = "DATA.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    #print("DATA:\n", data)

# UTILITY FUNCTIONS
def expand_universe(image, print_universe=(False, False)):
    '''Return image of the univers with inserted rows and columns in empty regions'''

    universe = image.copy()
    width = len(image[0])

    # loop through rows
    i = 0
    for line in image:
        # empty row
        if all([space == '.' for space in line]):
            #print("empty line", universe)
            universe.insert(i, '.'*width)
            i += 1
        i += 1

    # loop through columns
    i = 0
    for _ in range(width):
        # empty column
        if all([space[i] == '.' for space in universe]):
            universe = [line[:i] + '.' + line[i:] for line in universe]
            #print("universe altered", universe)
            i += 1
        i += 1

    # display universes
    if print_universe[0]:
        print("\nINPUT UNIVERSE:")
        for line in image:
            print(line)
    if print_universe[1]:
        print("\nEXPANDED UNIVERSE:")
        for line in universe:
            print(line)
        print()

    return universe

def get_galaxies(universe):
    '''Return dictionary of galaxies coordinates keyed by galxy ID numbers (intigers)'''
    galaxies = {}

    # populate galaxies
    galaxy_id = 0
    for i, line in enumerate(universe):
        for j, space in enumerate(line):
            if space == '#':
                galaxies[galaxy_id] = (i, j)
                galaxy_id += 1

    return galaxies

def calculate_distance(start, end):
    '''Returns Manhattan distance between start and end'''
    
    x, y = start
    w, z = end

    return abs(x-w) + abs(y-z)

def calculate_distance_from_not_expanded(start, end, empty_spaces, expansion):
    '''
    Returns Manhattan distance between start and end
    Takes into account that in a given empty_spaces unverse expanded by expansion value
    '''
    # set coordinates
    # make sure secound one is larger
    x, y = start
    w, z = end
    if y > z:
        # bitwise swap (^ bitwise XOR)
        y = y ^ z
        z = y ^ z
        y = y ^ z
    if x > w:
        #bitwise swap (^ bitwise XOR)
        x = x ^ w
        w = x ^ w
        x = x ^ w

    # initiate distance components calculations
    empty_rows, empty_columns = empty_spaces 
    vertical_distance = z - y
    horizontal_distance = w - x

    # loop through empty rows and add expansion
    for row in empty_rows:
        if row > x and row < w:
            horizontal_distance += expansion - 1
    
    # loop through empty columns and add expansion
    for column in empty_columns:
        if column > y and column < z:
            vertical_distance += expansion - 1

    
    #print("expansion:")
    #print("points", start, end)
    #print("empty", empty_rows, empty_columns)
    #print(horizontal_distance, vertical_distance)

    return horizontal_distance + vertical_distance

def get_empty_spaces(image):
    '''Returns tuple of lists of empty (populated by '.'s) rows and empty columns in image'''
    empty_rows = []
    empty_columns = []

    # loop through rows
    for i, line in enumerate(image):
        # empty row
        if all([space == '.' for space in line]):
            empty_rows += [i]
    
    # loop through columns
    for i in range(len(image[0])):
        # empty column
        if all([space[i] == '.' for space in image]):
            empty_columns += [i]

    return empty_rows, empty_columns


def star1():
    universe = expand_universe(data)
    galaxies = get_galaxies(universe)
    sum_distance = 0

    # definetly not optimal
    for i in galaxies:
        for j in galaxies:
            sum_distance += calculate_distance(galaxies[i], galaxies[j])

    print("Distance in part one is", sum_distance//2)

def star2():
    universe = data.copy()
    empty_spaces = get_empty_spaces(universe)
    galaxies = get_galaxies(universe)
    sum_distance = 0

    # definetly not optimal
    for i in galaxies:
        for j in galaxies:
            sum_distance += \
            calculate_distance_from_not_expanded(galaxies[i], galaxies[j], empty_spaces, 10**6)

    print("Distance in part two is", sum_distance//2)


star1()
star2()



























