# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 15

import numpy as np
from functools import reduce
import time

# PARAMETERS
data_path = "DATA.txt"

# GET DATA
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    data = np.array([[x if x != '.' else ' 'for x in line]for line in data])


# UTILITY FUNCTIONS Part 1
def print_platform(platform, tempo, return_coursor=True):
    '''Print platform state '''
    # print top edge
    print("\r\u256d" + "\u257c" * len(platform[0]) + "\u256e")
    # print platform
    for line in platform[::-1]:
        print("\r\u257d" + reduce(lambda x, y: x+y, line) + "\u257f")
    # print bottm edge
    print("\r\u2570" + "\u257e" * len(platform[0]) + "\u256f", flush=True, end='')

    # tempo of animation
    time.sleep(tempo)

    # return coursor to the top
    if return_coursor:
        for _ in range(len(platform) + 1):
            print("\033[A", flush=True, end='')
        print('\r', end='')

    print(flush=True, end='')

def roll(platform, y, x, animation_tempo, display=False):
    '''Rolls given by x and y rock to the edge or obsticle'''
    # search row for obsticle or edge
    for path in range(y-1, -2, -1):
        if platform[path][x] != ' ' or path == -1:
            # display animation
            if display: print_platform(platform, animation_tempo)
            # adjust values
            platform[y][x] = ' '
            platform[path+1][x] = 'O'
            break

def tiltTheLever(platform, animation_tempo=0.1, return_coursor=False, display=False):
    '''Rolls all rocks to the north edge or obsticle'''
    # find rocks to roll
    for y, line in enumerate(platform):
        for x, place in enumerate(line):
            if place == 'O':
                # roll rock
                roll(platform, y, x, animation_tempo, display=display)
    # display animation
    if display:
        print_platform(platform, animation_tempo, return_coursor=return_coursor)

    return platform

def calculateLoad(tilted_platform):
    '''Calculates total load on the north support beams'''
    load = 0
    hight = len(tilted_platform)

    # find all rocks
    for y, line in enumerate(tilted_platform):
        for element in line:
            if element == 'O':
                # increment load
                load += hight - y

    return load


def star1():
    resoult = calculateLoad(tiltTheLever(data.copy()))
    print("\nPart 1:", resoult, ' ' * len(data[0]))



# UTILITY FUNCTIONS Part 2
def spin_cycle_animated(platform, cycles=3):
    '''Visualization of spin cycle'''

    print("Test cycles:\n\n")
    for i in range(cycles):
        for _ in range(4):
            # roll rocks
            platform = tiltTheLever(platform, return_coursor=True, display=True, animation_tempo=0.1)
            # rotate whole array
            platform = np.rot90(platform, k=3)

            print("\033[Acycle =", i+1)
    print_platform(platform, 0)
    print("\n" * (len(platform)+1))

def test_cycle():
    # get test data
    with open("TESTDATA.txt", 'r') as data_file:
        test = data_file.read().split('\n')
        test = np.array([[x if x != '.' else ' 'for x in line]for line in test])

    # test spin cycle
    spin_cycle_animated(test.copy())

# devided functions so there will be one if less to check
# tilting functions
def tiltTheLeverNorth(platform):
    # find rocks
    y_indices, x_indices = np.where(platform == 'O')

    # roll rocks
    for y, x in zip(y_indices, x_indices):
        rollNorth(platform, y, x)
    
    return platform

def tiltTheLeverSouth(platform):
    # find rocks
    y_indices, x_indices = np.where(platform == 'O')

    # roll rocks
    for y, x in sorted(zip(y_indices, x_indices), key=lambda pair: -pair[0]):
        rollSouth(platform, y, x)

    return platform

def tiltTheLeverWest(platform):
    # find rocks
    y_indices, x_indices = np.where(platform == 'O')

    # roll rocks
    for y, x in sorted(zip(y_indices, x_indices), key=lambda pair: pair[1]):
        rollWest(platform, y, x)

    return platform

def tiltTheLeverEast(platform):
    # find rocks
    y_indices, x_indices = np.where(platform == 'O')

    # roll rocks
    for y, x in sorted(zip(y_indices, x_indices), key=lambda pair: -pair[1]):
        rollEast(platform, y, x)

    return platform

# rolling functions
def rollNorth(platform, y, x):
    # find the first non-empty space or the top
    for target_y in range(y - 1, -1, -1):

        # update positions and break if an obstacle is found
        if platform[target_y][x] != ' ':
            platform[y][x] = ' '
            platform[target_y + 1][x] = 'O'
            break

    # if no obstacle is found, move the rock to the top
    else:
        platform[y][x] = ' '
        platform[0][x] = 'O'

def rollSouth(platform, y, x):
    # find the first non-empty space or the bottom
    for target_y in range(y + 1, platform.shape[0]):

        # update positions and break if an obstacle is found
        if platform[target_y][x] != ' ':
            platform[y][x] = ' '
            platform[target_y - 1][x] = 'O'
            break

    # if no obstacle is found, move the rock to the bottom
    else:
        platform[y][x] = ' '
        platform[platform.shape[0] - 1][x] = 'O'

def rollWest(platform, y, x):
    # Find the first non-empty space or the left edge
    for target_x in range(x - 1, -1, -1):

        # Update positions and break if an obstacle is found
        if platform[y][target_x] != ' ':
            platform[y][x] = ' '
            platform[y][target_x + 1] = 'O'
            break

    # If no obstacle is found, move the rock to the left edge
    else:
        platform[y][x] = ' '
        platform[y][0] = 'O'

def rollEast(platform, y, x):
    # find the first non-empty space or the right edge
    for target_x in range(x + 1, platform.shape[1]):

        # update positions and break if an obstacle is found
        if platform[y][target_x] != ' ':
            platform[y][x] = ' '
            platform[y][target_x - 1] = 'O'
            break

    # if no obstacle is found, move the rock to the right edge
    else:
        platform[y][x] = ' '
        platform[y][platform.shape[1] - 1] = 'O'

# above functions combined into cycles
def spin_cycle(platform, cycles):
    '''Returns total load on north supporting beams after cycles cycles'''
    # memoization
    memory = []

    # loop through cycles
    for i in range(1, cycles+1):
        # update platform for one cycle
        tiltTheLeverNorth(platform)
        tiltTheLeverWest(platform)
        tiltTheLeverSouth(platform)
        tiltTheLeverEast(platform)

        # memoization
        for mem in memory:
            if np.array_equal(mem[0], platform):

                length = i - mem[1]
                remaining_cycles = cycles - i
                cycles2run = remaining_cycles % length

                print(f"\nIn memory at cycle {i}, previously seen at cycle {mem[1]}")
                print(f"Skipping repetitive cycles, running {cycles2run} cycles left")

                return spin_cycle(platform, cycles2run)

        memory.append((platform.copy(), i))

    return platform


def star2():
    print("\nPart 2:", calculateLoad(spin_cycle(data.copy(), 10 ** 9)))


star1()
test_cycle()
star2()

