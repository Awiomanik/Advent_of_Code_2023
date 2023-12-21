# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 13

import numpy as np
from functools import reduce


# PARAMETERS
data_path = "DATA.txt"


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')


# UTILITY FUNCTIONS
def split_data():
    '''Splits data into valleys'''
    temp_list = []
    final_list = []

    for line in data:
        if line != '':
            temp_list.append(line)
        else:
            final_list.append(temp_list)
            temp_list = []

    final_list.append(temp_list)

    return final_list

def transpose_valley(valley):
    '''Transposes list of strings in place!'''

    return [reduce(lambda x, y: x+y, line) \
            for line in np.array([[x for x in line] \
                for line in valley]).transpose().tolist()]

def find_mirror_image(valley, skip=None):
    '''
    Returns row after which image is mirrored,
    using recursive check_mirror_image function
    '''
    for i in range(1, len(valley)):
        # if two consecutive rows are the same check if it's a mirror
        if valley[i] == valley[i-1]:
            if check_mirror_image(valley.copy(), i):
                # check skip parameter
                if skip == i:
                    continue
                return i
    return 0
            
def check_mirror_image(valley, mirror_position):
    '''
    Recursive check if given row splits valley into mirrror images
    Returns boolian for valley is symetric relative to given row
    '''
    # adjust row position
    mirror_position -= 1

    # recursion escape condition
    # if came to the edge of valley
    try:
        valley[mirror_position]
        valley[mirror_position+1]
        if mirror_position == -1:
            return True
    except:
        return True
    
    # check mirror recursively
    if valley[mirror_position] == valley[mirror_position+1]:
        # pop checcked rows
        valley.pop(mirror_position)
        valley.pop(mirror_position)
        return check_mirror_image(valley, mirror_position)
    else:
        return False

def smudge(valley, row, col):
    '''Returns valley with reversed element in row, col'''
    if valley[row][col] == '#':
        valley[row] = valley[row][:col] + '.' + valley[row][col+1:]
    else:
        valley[row] = valley[row][:col:] + '#' + valley[row][col+1:]

def cut_valley(valley, row=None, col=None):
    '''
    Returns valley with cuted off rows/columns 
    that are further from given row/column than 
    than edge of valley on the other side
    (In the end never used)
    '''
    # cut rows
    if row:
        h = len(valley)

        if row == h/2:
            return valley
        
        if row < h/2:
            return valley[:2*row]
        
        if row > h/2:
            return valley[h - ((h - row) * 2):]
        
    # cut columns
    if col:
        w = len(valley[0])

        if col == w/2:
            return valley
        
        if col < w/2:
            return [line[:2*col] for line in valley]
        
        if col > w/2:
            return [line[w -((w-col) * 2):] for line in valley]

def find_smudge(valley):
    '''Returns value of 100 rows or column where smudged mirror splits vlley'''
    # initialize variables
    possible_valleys = []
    final_valleys = None

    # find original valleys mirror imaage
    original_row = find_mirror_image(valley)
    original_col = find_mirror_image(transpose_valley(valley))

    # loop through elements and generate all possible valleys
    for row, line in enumerate(valley):
        for column in range(len(line)):

            # put smudge on valley
            smudge(valley, row, column)

            # find smuged valleys mirror (if there is one)
            # and populate possible valleys with it
            # vertical
            mirror_row = find_mirror_image(valley, original_row)
            if mirror_row != 0:
                possible_valleys.append(mirror_row * 100)

            # horizontal
            mirror_col = find_mirror_image(transpose_valley(valley), original_col)
            if mirror_col != 0:
                possible_valleys.append(mirror_col)

            # clea smudge from valley
            smudge(valley, row, column)

            #check if exactly one valley was generated with this smudge
            if len(possible_valleys) == 1:
                final_valleys = possible_valleys
            possible_valleys = []
    
    return final_valleys[0]


def star1():
    valleys = split_data()
    counter = 0

    for valley in valleys:
        counter += 100 * find_mirror_image(valley)
        counter += find_mirror_image(transpose_valley(valley))

    print("Part 1:", counter)

def star2():
    # set varibles
    valleys = split_data()
    valleys_len = len(valleys)
    counter = []

    print("Part 2", end='')

    # loop through valleys and find smuged mirrors
    for i, valley in enumerate(valleys):
        print(f"\rPart 2: {i/valleys_len*100:.0f}%", end='')
        counter.append(find_smudge(valley))

    
    print("\rPart 2:", sum(counter), ' '*10)


star1()
star2()