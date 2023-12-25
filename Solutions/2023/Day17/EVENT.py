# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 17

import numpy as np
from heapq import heappop as hpop
from heapq import heappush as hpush


# GET DATA
with open("DATA.txt", 'r') as data_file:
    # numpy arry of ints
    DATA = np.array([[int(char) for char in line] for line in data_file.read().split('\n')])
    # size of array
    WIDTH, HEIGHT = len(DATA[0]), len(DATA)


# CONSTANTS
# direction mapping
DIRECTION_MAP = {
    #     x, y
    'r': (1, 0),
    'l': (-1, 0),
    'u': (0, -1),
    'd': (0, 1)
    }
# direction change mappings
LEFT_TURN = {'r': 'd', 'd': 'l', 'l': 'u', 'u': 'r'}
RIGHT_TURN = {'r': 'u', 'u': 'l', 'l': 'd', 'd': 'r'}


# UTILITY FUNCTIONS
def if_edge(coords):
    return 0 <= coords[0] < HEIGHT and 0 <= coords[1] < WIDTH

def search_path(max_straight, min_straight=1):
    '''Returns heat loss along most optimal path possible'''

    # initialize variables
    visited = set()
    path = [(0, (0, 0), 'd'), (0, (0, 0), 'r')] # [(heat, coords, direction),.. ]
    
    while True:
        # get element with least heat loss
        heat, coords, direction = hpop(path)

        # display progress
        print(f"\rCalculating... {heat}", end='')

        # reached end block
        if coords == (WIDTH-1, HEIGHT-1): return heat

        # path looped
        if (coords, direction) in visited: continue
        visited.add((coords, direction))

        # loop over possible directions
        for dir_k  in LEFT_TURN[direction], RIGHT_TURN[direction]:
            dir_v = DIRECTION_MAP[dir_k]

            # move in one direction till max value of straight movement reached
            for line in range(min_straight, max_straight+1):
                if if_edge((next_coords := (coords[0] + dir_v[0] * line, \
                                            coords[1] + dir_v[1] * line))):
                    
                    # sum up the cost of line (heat loss)
                    current_heat_loss = \
                        sum(DATA[coords[1] + dir_v[1] * steps][coords[0] + dir_v[0] * steps] \
                        for steps in range(1, line+1))
                    
                    # upadtae path heap
                    hpush(path, (heat + current_heat_loss, next_coords, dir_k))

    
def star1():
    print("\rPart 1:", search_path(3), " "*20)

def star2():
    print("\rPart 2:", search_path(10, 4), " "*20)


star1()
star2()


















