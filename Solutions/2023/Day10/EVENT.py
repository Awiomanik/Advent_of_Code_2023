# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 10


# CONSTANTS
# Directions: N, S, W, E
directions = {
    '|': ('N', 'S'),
    '-': ('W', 'E'),
    'L': ('N', 'E'),
    'J': ('N', 'W'),
    '7': ('S', 'W'),
    'F': ('S', 'E')
}


# GET DATA
with open("DATA.txt", 'r') as data_file:
    DATA = data_file.read().split('\n')


# UTILITY FUNCTIONS
def find_S(data):
    '''
    Finds the starting point of the loop

    Args:
    - data: list of listss of chars representation of pipes

    Returns:
    - i, j: coordinates of the starting point
    '''
    for i, d in enumerate(data):
        for j, b in enumerate(d):
            if b == 'S':
                return i, j

def find2nodes_from_S(data, start):
    '''
    Finds the nodes connected to the starting point
    
    Args:
    - data: list of listss of chars representation of pipes
    - start: coordinates of the starting point
    
    Returns:
    - nodes: coordinates of the nodes connected to the starting point
    '''

    nodes = []

    # Check South
    if data[start[0]+1][start[1]] == '|' or \
       data[start[0]+1][start[1]] == 'L' or \
       data[start[0]+1][start[1]] == 'J':
        nodes.append((start[0]+1, start[1]))

    # Check North
    if data[start[0]-1][start[1]] == '|' or \
       data[start[0]-1][start[1]] == 'F' or \
       data[start[0]-1][start[1]] == '7':
        nodes.append((start[0]-1, start[1]))

    # Check East
    if data[start[0]][start[1]+1] == '-' or \
       data[start[0]][start[1]+1] == 'J' or \
       data[start[0]][start[1]+1] == '7':
        nodes.append((start[0], start[1]+1))

    # Check West
    if data[start[0]][start[1]-1] == '-' or \
       data[start[0]][start[1]-1] == 'L' or \
       data[start[0]][start[1]-1] == 'F':
        nodes.append((start[0], start[1]-1))
                   
    return tuple(nodes)

def check_direction(data, previous_pipe, pipe):
    '''
    Determines the next direction to move
    
    Args:
    - data: list of listss of chars representation of pipes
    - previous_pipe: coordinates of the previous pipe
    - pipe: coordinates of the current pipe
    
    Returns:
    - next_pipe: coordinates of the next pipe
    '''

    # connections of current pipe
    pipe_type = data[pipe[0]][pipe[1]]

    # determine the direction to move based on the current pipe type
    possible_directions = directions[pipe_type]

    # determine the direction from current to previous
    if previous_pipe[0] < pipe[0]:  # moved South
        move_direction = 'N'
    elif previous_pipe[0] > pipe[0]:  # moved North
        move_direction = 'S'
    elif previous_pipe[1] > pipe[1]:  # moved East
        move_direction = 'E'
    elif previous_pipe[1] < pipe[1]:  # moved West
        move_direction = 'W'

    # determine the next direction based on the current pipe
    next_direction = possible_directions[0] if possible_directions[0] != move_direction else possible_directions[1]

    # Calculate the next pipe's coordinates based on the next direction
    if next_direction == 'N': return (pipe[0] - 1, pipe[1])
    elif next_direction == 'S': return (pipe[0] + 1, pipe[1])
    elif next_direction == 'E': return (pipe[0], pipe[1] + 1)
    elif next_direction == 'W': return (pipe[0], pipe[1] - 1)

def walk(data, previous_nodes, starting_nodes, visited=None, distance=1):
    '''
    Walks through the loop and counts the distance to the furthest node
    
    Args:
    - data: list of listss of chars representation of pipes
    - previous_nodes: coordinates of the previous nodes
    - starting_nodes: coordinates of the current nodes
    - visited: list of visited nodes
    - distance: distance from the starting point
    
    Returns:
    - starting_nodes: coordinates of the current nodes
    - next_nodes: coordinates of the next nodes
    - visited: list of visited nodes
    - distance: distance from the starting point
    '''

    # set starting visited
    if visited is None:
        visited = set()

    # recursion stop condition
    # if the current node is already visited or the two nodes are the same
    if starting_nodes[0] in visited:
        return distance, visited
    if starting_nodes[0] == starting_nodes[1]:
        return distance, visited.add(starting_nodes[0])
    
    # mark current position as visited
    visited.add(starting_nodes[0])
    visited.add(starting_nodes[1])

    # update distance
    distance += 1

    # determin next nodes
    next_nodes = check_direction(data, previous_nodes[0], starting_nodes[0]), \
                 check_direction(data, previous_nodes[1], starting_nodes[1])

    return starting_nodes, next_nodes, visited, distance

def enclosed_area(data, loop, display_grid=False):
    '''
    This function calculates the area enclosed by a loop of pipes on a field.

    Parameters:
    - data: list of listss of chars representation of pipes
    - loop: list of coordinates of the loop in of pipes
    - display_grid: progress displaying flag

    Returns:
    counter: The area enclosed by the loop.
    '''

    # display grid
    if display_grid:
        # prepare grid copy
        display = [list(d) for d in data]

        # display grid copy
        print("ORIGINAL")
        for d in display:
            print(''.join(str(x) for x in d))
        print()

        # prepare copy for loop display
        dis1 = [[x for x in d] for d in display]
        for y in range(len(data)):
            for x in range(len(data[0])):
                if (y, x) in loop:
                    dis1[y][x] = '#'
                else:
                    dis1[y][x] = '.'

        # display loop
        print("LOOP")
        for d in dis1:
            print(''.join(str(x) for x in d))
        print()

    # define corner mapping
    corner_directions = {'F': 'down', 'L': 'up'}

    # go through grid line by line
    counter = 0
    for y in range(len(data)):

        # set flags
        inner = False
        last_direction = None

        # go through line
        for x in range(len(data[0])):
            cell = data[y][x]

            # loop encountred
            if (y, x) in loop:

                # horizontal wall encountered
                if cell == '|': inner = not inner
                
                # starting corner encountered
                elif cell in corner_directions: last_direction = corner_directions[cell]

                # ending corner encountered and direction mathces previous
                elif cell in ('7', 'J') \
                    and ((last_direction == 'up' and cell == '7') \
                    or (last_direction == 'down' and cell == 'J')):
                    inner = not inner

            # in the loop
            elif inner:
                counter += 1    
                # update display grid
                if display_grid: display[y][x] = '#'
            
            # out of loop
            elif display_grid:
                # update display grid
                display[y][x]  = '.'
    
    # display grid
    if display_grid:
        print("FINAL")
        for d in display:
            print(''.join(str(x) for x in d))

    return counter

def get_S_shape(s, neighbour1, neighbour2):
    '''
    Determins shape of S pipe based on pipes it is connected to.

    Args:
    - s: coords of S pipe
    - neighbour1, neighbour2: coordinates of connected pipes

    Returns:
    - Symbol for a given pipe shape and direction
    '''
    # all y-coordinates are the same, it's a vertical line
    if neighbour1[1] == neighbour2[1] == s[1]: return '|'
    
    # all x-coordinates are the same, it's a horizontal line
    elif neighbour1[0] == neighbour2[0] == s[0]: return '-'
    
    # check for corners
    else:
        # neighbour1 is horizontally aligned with s and s is vertically aligned with neighbour2
        if neighbour1[0] == s[0] and s[1] == neighbour2[1]: return 'L'
        
        # neighbour1 is vertically aligned with s and s is horizontally aligned with neighbour2
        elif neighbour1[1] == s[1] and s[0] == neighbour2[0]: return 'F'
        
        # neighbour1 is vertically aligned with s and s is horizontally aligned with neighbour2
        if neighbour1[1] == s[1] and s[0] == neighbour2[0]: return 'J'
        
        # neighbour1 is horizontally aligned with s and s is vertically aligned with neighbour2
        elif neighbour1[0] == s[0] and s[1] == neighbour2[1]: return '7'


def star1():
    # find the starting point and the nodes connected to it
    previous = find_S(DATA)
    start = find2nodes_from_S(DATA, previous)

    # walk through the loop and count the distance to the furthest node
    x = walk(DATA, (previous, previous), start)
    while True:
        x = walk(DATA, *x)
        if len(x) == 2: break

    # print the result
    print("Part 1:", x[0])

def star2():
    loop = set()

   # find the starting point and the nodes connected to it
    previous = find_S(DATA)
    start = find2nodes_from_S(DATA, previous)

    # walk through the loop and count the distance to the furthest node
    x = walk(DATA, (previous, previous), start)
    while True:
        x = walk(DATA, *x)
        if len(x) == 2: break
        else: loop = x[-2]

    # add first and last element to the loop
    loop.add(previous)
    loop.add(x[1])

    # prepare grid copy and replace S with proper pipe shape
    data = [[DATA[y][x] for x in range(len(DATA[0]))] for y in range(len(DATA))]
    data[previous[0]][previous[1]] = get_S_shape(previous, start[0], start[1])

    # print resoult
    print("Part 2:", enclosed_area(data, loop))


star1()
star2()
