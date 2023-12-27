# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 22


import numpy as np
from functools import reduce
import copy
import shutil
import time


# GET DATA
with open("DATA.txt", 'r') as data_file:
    # list of bricks: [((x, y, z), (x2, y2, z2)),.. ]
    DATA = [tuple(tuple(int(d) for d in b.split(',')) for b in brick.split('~')) for brick in data_file.read().split('\n')]
    # maximum size of a grid of bricks
    X, Y, Z = (max([max(b[0][i], b[1][i]) for b in DATA])+1 for i in range(3))
    # amount of bricks
    AMOUNT = len(DATA)


# Utility FUNCTIONS
def print_grid(grid, empty_symbol='. '):
    '''Prints visual representation of given grid array as crossesction along y axis'''
    # print cross-sections markings
    print(reduce(lambda x, y: x + y, ["    "] + [f"y = {y}{' ' * X}" for y in range(Y)]))

    # for row (printed from top)
    for row in range(Z-1, 0, -1):
        print(row, end=' ' * ((3 if Z - row < 10 else 2) if row < 100 else 1))

        # for cross-section in y dimension
        for cs in range(Y):
            # for column
            for col in range(X):

                # print space representation
                if (g := grid[col, cs, row]): print(g, end=' ')
                else: print(empty_symbol, end='')

            # add spacing between sections
            print(' ' * 5, end='')

        # separate rows
        print()

def get_bricks(data):
    '''
    Returns bricks as a list of lits of bricks coordinates
    [[(x, y, z),.. ],.. ]
    '''
    bricks = []
    for brick in data:
        brick_coord = []

        # iterate over coordnates of the brick
        for x in range(brick[0][0], brick[1][0]+1):
            for y in range(brick[0][1], brick[1][1]+1):
                for z in range(brick[0][2], brick[1][2]+1):
                    
                    # add coordinates to current brick
                    brick_coord.append((x, y, z))

        # add brick to return list
        bricks.append(brick_coord)

    return bricks

def get_grid(bricks):
    '''
    Returns 3 dimentional boolian array 
    representing snapshot of falling bricks 
    as True for brick volume and False for empty volume
    '''
    # initialize array
    grid = np.full((X, Y, Z), 0)

    # populate array
    for i, brick in enumerate(bricks):

        # iterate over brick coordinates
        for (x, y, z) in brick:

            # insert brick volume
            grid[x, y, z] = i+1 

    return grid

def drop_bricks(starting_grid, starting_bricks):
    '''
    Simulates bricks falling down
    Returns grid state after all bricks fallen down
    If count=True, returns number of fallen bricks
    '''
    # arguments will be modified
    grid, bricks = copy.deepcopy(starting_grid), copy.deepcopy(starting_bricks)

    # count falling bricks
    counter = set()

    # for brick
    # drop that brick one level
    # check if it overlaps other brick
    brick_fell = True
    while brick_fell:
        brick_fell = False
        for i, brick in enumerate(bricks):
            # check if brick touchnig the ground
            if (brick_bottom := min(b[2] for b in brick)) != 1:

                # assuming bricks are always one cube wide in at least two dimensions
                # check if brick is not vertical
                if all(cube[2] == cube2[2] for cube, cube2 in zip(brick, brick[1:])):

                    # check if all spaces directly beneth the cube are empty
                    for (x, y, z) in brick:
                        if grid[x, y, z-1]: break

                    # spaces empty
                    else:
                        # update grid and bricks for horizontal brick falling
                        for j, (x, y, z) in enumerate(brick):
                            grid[x, y, z-1] = grid[x, y, z]
                            grid[x, y, z] = 0
                            bricks[i][j] = (x, y, z-1)
                        brick_fell = True
                        counter.add(i)


                # brick is vertical
                else:
                    # check if single space beneth brick is empty
                    if not grid[brick[0][0], brick[0][1], brick_bottom - 1]:

                        # update grid for vertical brick falling
                        grid[brick[0][0], brick[0][1], brick_bottom - 1] = \
                        grid[brick[0][0], brick[0][1], (brick_top := max(b[2] for b in brick))]
                        grid[brick[0][0], brick[0][1], brick_top] = 0
                        # update bricks
                        for j, (tx, ty, tz) in enumerate(brick):
                            bricks[i][j] = (tx, ty, tz - 1)
                        brick_fell = True     
                        counter.add(i)          

    return grid, bricks, len(counter)

def loading_bar_update(start, i, total, additional_info=None):
    '''
    Updates loading bar
    Input:
    start           starting time in seconds (int)
    i               current iteration (indexing from 1!) (int)
    total           number of all calculations (int)
    additional_info additional info about current state (string)
    '''
    # initialize nmerical variables
    current_time = time.time()
    percentage = int(i/total * 100)

    # initialize strings
    percent_string = f"| {percentage}% |"
    info_string = f"| {i}/{total} | " + \
                  ((additional_info + " | ") if additional_info else '') + \
                  f"Average time = {(current_time - start)/i:.2f}s |"
        # make time show min or nanosec if necessary
        ############################################

    # initialize size
    loading_bar_size = shutil.get_terminal_size()[0] - len(percent_string) - len(info_string) - 2

    # print
    print("\r" + percent_string + \
            '\u25B0' * (int(percentage / 100 * loading_bar_size)) + \
            '\u2550' * (int((100 - percentage) / 100 * loading_bar_size)) + \
            info_string, end='')


def star1_and_2():
    starting_time = time.time()

    # get original data
    original_bricks = get_bricks(DATA)
    original_grid = get_grid(original_bricks)

    # simulate bricks falling down
    grid_setteled, bricks_setteled, _ = drop_bricks(original_grid, original_bricks)

    # loop through bricks and remove them one by one then simulate faling down again
    desintegrable_counter = 0
    fallen_counter = 0
    for i in range(1, AMOUNT+1):
        # display progress
        loading_bar_update(starting_time, i, AMOUNT)

        # copy original grid and bricks
        current_grid = copy.deepcopy(grid_setteled)
        current_bricks = copy.deepcopy(bricks_setteled)

        # get coordinates of a brick to be desintegrated
        removed_brick_coords = list(zip(*np.where(grid_setteled == i)))

        # remove elements by removed_brick_coords
        for (x, y, z) in removed_brick_coords:
            current_grid[x, y, z] = 0
        current_bricks = [brick for brick in current_bricks if brick != removed_brick_coords]

        # drop bricks again to see how many would fall
        fallen_bricks = drop_bricks(current_grid, current_bricks)[2]
        
        # update counters
        if fallen_bricks: fallen_counter += fallen_bricks
        else: desintegrable_counter += 1


    # display result
    print(f"\nPart 1: {desintegrable_counter}\nPart 2: {fallen_counter}\n(calculation time: {time.time() - starting_time:.0f}s)")

star1_and_2()
