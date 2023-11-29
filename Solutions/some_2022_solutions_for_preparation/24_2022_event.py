# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: (test from 2022)


from time import sleep
import numpy as np
import os
import gc


# PARAMETERS
data_path = "test3_data.txt"

expedition_char = "\u2603"
blizzard_char = "\u2600"


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')


def get_valley(data):
    '''
    Takes:    ASCII represetation of valley
    Returns:  dict of types of fields as boolian arrays
    '''
    # Define dimentions of valley
    height, width = len(data) - 2, len(data[0]) - 2
    # Define valley
    valley = {
        ".": np.zeros((height, width), dtype=bool),
        "^": np.zeros((height, width), dtype=bool),
        "v": np.zeros((height, width), dtype=bool),
        ">": np.zeros((height, width), dtype=bool),
        "<": np.zeros((height, width), dtype=bool)
    }
    # Populate valley
    for x, d in enumerate(data[1:-1]):
        for y, c in enumerate(d[1:-1]):
            valley[c][x, y] = True
    
    return valley

def blizzard_fields_proceeding(boolian_valley):
    valleys = []
    for _ in range(len(boolian_valley["^"]) * len(boolian_valley["^"][0])):
        # Append frame
        valleys.append(boolian_valley["^"] | boolian_valley["v"] | boolian_valley[">"] | boolian_valley["<"])
        # Shift arrays
        boolian_valley["^"] = np.row_stack((boolian_valley["^"][1:,:], boolian_valley["^"][:1,:]))
        boolian_valley[">"] = np.column_stack((boolian_valley[">"][:,-1:], boolian_valley[">"][:,:-1]))
        boolian_valley["v"] = np.row_stack((boolian_valley["v"][-1:,:], boolian_valley["v"][:-1,:]))
        boolian_valley["<"] = np.column_stack((boolian_valley["<"][:,1:], boolian_valley["<"][:,:1]))

    return valleys

def print_valley(boolian_valley, expedition_coords, current_time, tempo=0.2):
    '''Clears screen, prints valley with expedition'''
    width = len(boolian_valley[0,:])
    expedition_coords = list(expedition_coords)

    os.system("cls")

    print("# " + (expedition_char \
          if expedition_coords == [0, -1] \
            else " ") + "# "*(width))
    for i, row in enumerate(boolian_valley):
        body = " ".join([((" " if not c \
                        else blizzard_char) \
                        if expedition_coords != [i, j] \
                        else expedition_char) \
                        for j, c in enumerate(row)])
        print("# " + body + "#")
    print("# "*width + " #")
    print("Expedition at:", expedition_coords)
    print("Current time: ", current_time)
    
    sleep(tempo)

def valid_neighbours(coords, valley, width, height):
    '''Checks which neighboring nodes are valid (including current)
    Takes:   (int, int), [[...]...], int, int
    Returns: [(...)...]'''

    neighboring_nodes = []

    # Absolute start coords
    #print(coords)
    if coords == (-1, 0):
        neighboring_nodes.append((-1, 0))
        if not valley[0][0]:
            return [(0, 0), (-1, 0)]
    # Absolute end coords
    if coords == (height, width-1):
        neighboring_nodes.append((height, width-1))
        if not valley[height-1][width-1]:
            return [(height-1, width-1), (height, width-1)]
        
    # Expedition can always hide in start and end position
    if coords == (0, 0):
        neighboring_nodes.append((-1, 0))
    if coords == (height-1, width-1):
        neighboring_nodes.append((height, width-1))

    # End coords
    elif coords == (height-1, width-1):
        return [(height, width-1)]
    
    # Other cases
    for (r, c) in [(coords[0]+1, coords[1]), # down
                   (coords[0], coords[1]+1), # right
                   (coords[0]-1, coords[1]), # up
                   (coords[0], coords[1]-1), # left
                   (coords[0], coords[1])]:  # wait
        #print("all nodes:   ", r, c, valley)

        #print("hei, wid:    ", height, width)
        # check if in boundaries of valley
        if r < 0 or c < 0 or c >= width or r >= height:
            continue

        # check if not a blizzard
        #print("nodes inside:", r, c, valley)
        if not valley[r][c]:
            neighboring_nodes.append((r, c))

    return neighboring_nodes

def dijkstras_path_finding(valleys, trip_back=False, which_valley=0, \
                           animation_tempo=0.2, if_animation=False):
    '''https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    Takes:      list of states of enviroment every time step
    Opyional:   bool if trip from end to start
                int index of list of enviroments to begin
                bool if print progress
                float secounds per frame of progress
    Returns:    int shortest distance
                int index of enviroment at the end
                '''
    
    start_node = (-1, 0)
    h, w = valleys[0].shape
    end_node = h, w-1
    # reverce start and finish if trip back
    if trip_back:
        temp = start_node
        start_node = end_node
        end_node = temp

    # get length of a valley weather cycle
    cycle = len(valleys)

    # make sure which_valley in range
    which_valley = which_valley % cycle

    # { ( visited node, time step ) distance to reach them }
    visited_nodes_set = {(start_node, which_valley): 0}
    priority = []

    # [ (distance, node, time step ) ]
    priority.append((0, start_node, which_valley))

    # Loop over priority queue, pop element of smallest distance and add new possible paths
    while priority:
        # pop node with smallest distance
        priority.sort(key=lambda k: k[0])
        distance, node, valley_in_cycle = priority.pop(0)

        # check if on the end position
        if node == end_node:
            #print("\nend valley:\n\n", valleys[(valley_in_cycle)%cycle], valley_in_cycle)
            return distance, valley_in_cycle
        
        # update valley state
        next_time_step = (valley_in_cycle+1) % cycle
        current_valley = valleys[next_time_step]

        # update distance
        current_distance = distance + 1

        # loop through valid neighboring nodes and check if visited
        for current_node in valid_neighbours(node, current_valley, w, h):
            # check if next node was visited
            node_on_time = visited_nodes_set.get((current_node, next_time_step))
            if node_on_time is None or node_on_time > current_distance:
                # update queue
                visited_nodes_set[(current_node, next_time_step)] = current_distance
                priority.append((current_distance, current_node, next_time_step))
            
            # print progress
            if if_animation:
                print_valley(current_valley, current_node, next_time_step, animation_tempo)

    # Return None if goal can't be reached    
    return None


def star1():
    initial_valley = get_valley(data)
    valley_proceeding = blizzard_fields_proceeding(initial_valley)
    distance = dijkstras_path_finding(valley_proceeding)

    print("Shortest distnce is", distance)

def star2():
    initial_valley = get_valley(data)
    valley_proceeding = blizzard_fields_proceeding(initial_valley)

    distance1, current_time = dijkstras_path_finding(valley_proceeding)
    print("Trip 1 is\t\t ", distance1)
    gc.collect()
    distance2, current_time = dijkstras_path_finding(valley_proceeding, True, current_time)
    print("Trip 2 is\t\t ", distance2)
    gc.collect()
    distance3, _ = dijkstras_path_finding(valley_proceeding, False, current_time)
    print("Trip 3 is\t\t ", distance3)
    gc.collect()

    #print(valley_proceeding[distance1])
    #print(valley_proceeding[distance2])

    print("Shortest total distnce is", distance1 + distance2 + distance3)

# Testing
def test_valid_neighbors():
    # Test 1 valley
    valley1 = [
        [False, False, False],
        [False, True, False],
        [False, False, False]
    ]

    # Test 1 coordinates
    coords1 = [
        (1, 1),  # Center, surrounded by a blizzard
        (0, 0),  # Top-left corner
        (2, 2),  # Bottom-right corner
        (-1, 0), # Special start coordinate
        (3, 2),  # Special end coordinate
    ]

    # Test 2 valley
    valley2 = [
        [True, False, True],
        [False, False, False],
        [True, False, True]
    ]

    # Test 2 coordinates for Grid 2
    coords2 = [
        (1, 0),  # Edge, not a corner
        (0, 1),  # Top edge
        (1, 2),  # Right edge
        (-1, 0), # Special start coordinate
        (3, 2),  # Special end coordinate
        (3, 3)   # Bottom-right corner
    ]

    # Test 3 valley
    valley3 = [
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ]

    # Test 3 coordinates
    coords3 = [
        (1, 1),  # Center, all sides blizzard
        (0, 0),  # Top-left corner, all sides blizzard
        (2, 2),  # Bottom-right corner, all sides blizzard
        (-1, 0), # Special start coordinate
        (3, 2)   # Special end coordinate
    ]

    # Test 4 valley
    valley4 = [
        [False, True, False, True, False, True],
        [False, False, False, False, False, False],
        [True, False, True, False, True, False]
    ]

    # Test 4 coordinates
    coords4 = [
        (1, 2),  # Center, no blizzard
        (0, 5),  # Top-right corner
        (2, 0),  # Bottom-left corner
        (-1, 0), # Special start coordinate
        (3, 5)   # Special end coordinate (adjusted for grid size)
    ]

    test_set_val = [valley1, valley2, valley3, valley4]
    test_set_coo = [coords1, coords2, coords3, coords4]

    a = 0
    for v, c in zip(test_set_val, test_set_coo):
        a += 1
        print(f"TEST GRID {a}:\n")
        for i in c:
            #print(i, v)
            h, w = len(v), len(v[0])
            print("nodes out:   ", i, v, valid_neighbours(i, v, w, h))
            print("\n")

#test_valid_neighbors()
#star1()
star2()