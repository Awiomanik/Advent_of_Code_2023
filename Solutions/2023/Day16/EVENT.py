# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 16

import numpy as np
from functools import reduce

# GET DATA
with open("DATA.txt", 'r') as data_file:
    data = np.array([[char for char in line] for line in data_file.read().split('\n')])


# CONSTANTS
direction_tuple = {
    #     x, y
    'r': (1, 0),
    'l': (-1, 0),
    'u': (0, -1),
    'd': (0, 1)
    }


# UTILITY FUNCTIONS
def calculate_energy(entering_beam):
    '''Returns number of energized tiles after entering beam gets into repetetive cycle'''
    # set variables
    energized = set()
    current_light_beams = [entering_beam]

    while True:
        new_beams = []
        
        # move all current beams
        for beam in current_light_beams:
            new_beams.extend(move_beam(beam))

        # check if any new beams are actually new
        new_unique_beams = [beam for beam in new_beams if beam not in energized]

        # new beams generated
        if new_unique_beams:
            # update energized with new unique beams
            energized.update(new_unique_beams)
            # set current beams to new unique beams for next iteration
            current_light_beams = new_unique_beams
        
        # no new beams (repetetive cycle reached)
        else: break

    # return unique energized tiles
    return len({e[0] for e in energized})

def move_beam(beam):
    '''
    Retnrns list of tuples of coordinates and direction (beams)
    after performing one move into direction
    [(coordinates (int, int), direction (int, int)),.. ]
    '''
    # update cooordinates
    coords, direction = beam
    new_coords = (coords[0] + direction[0], coords[1] + direction[1])

    # Check for edge of contraption
    if new_coords[0] < 0 or new_coords[0] >= len(data[0]) \
    or new_coords[1] < 0 or new_coords[1] >= len(data):
        #print('EDGE')
        return []

    # get type of tile
    space = data[new_coords[1]][new_coords[0]]
    
    # Handle splitter
    # Moving vertically
    if space == '|' and direction[0] != 0:  
            #print('SPLITTER |', new_coords)
            return [(new_coords, direction_tuple['u']), (new_coords, direction_tuple['d'])]
    # Moving horizontally
    if space == '-' and direction[1] != 0:  
            #print('SPLITTER -', new_coords)
            return [(new_coords, direction_tuple['l']), (new_coords, direction_tuple['r'])]

    # Handle mirror
    if space == '\\':
        #print("MIRROR \\", new_coords)
        # Moving horizontally
        if direction[0] != 0:  
            return [(new_coords, direction_tuple['d' if direction[0] == 1 else 'u'])]
        # Moving vertically
        else: 
            return [(new_coords, direction_tuple['r' if direction[1] == 1 else 'l'])]
    elif space == '/':
        #print("MIRROR", new_coords)
        # Moving horizontally
        if direction[0] != 0:  
            return [(new_coords, direction_tuple['u' if direction[0] == 1 else 'd'])]
        # Moving vertically
        else:  
            return [(new_coords, direction_tuple['l' if direction[1] == 1 else 'r'])]

    # Empty space
    #print('EMPTY SPACE', new_coords)
    return [(new_coords, direction)]


def star1():
    print("Part 1:", calculate_energy(((-1, 0), direction_tuple['r'])))

def star2():
    hottest_alignment = 0

    # left edge
    for y in range(len(data)):
        #print('left edge', (-1, y))
        hottest_alignment = max(hottest_alignment, \
                            calculate_energy(((-1, y), direction_tuple['r'])))

    # right edge
    for y in range(len(data)):
        #print('right edge', len(data[0]), y)
        hottest_alignment = max(hottest_alignment, \
                            calculate_energy(((len(data[0]), y), direction_tuple['l'])))
        
    # top edge
    for x in range(len(data[0])):
        #print('top edge', (x, -1))
        hottest_alignment = max(hottest_alignment, \
                            calculate_energy(((x, -1), direction_tuple['d'])))
        
    # bottom edge
    for x in range(len(data)):
        #print('bottom edge', (x, len(data)+1))
        hottest_alignment = max(hottest_alignment, \
                            calculate_energy(((x, len(data)), direction_tuple['u'])))

    print("Part 2:", hottest_alignment)


star1()
star2()