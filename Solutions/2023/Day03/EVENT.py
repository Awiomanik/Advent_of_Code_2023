# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 3

import numpy as np

# PARAMETERS
data_path = "DATA.txt"


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    data = np.array([list(d) for d in data])
    

# UTILITY FUNCTIONS
def list_numbers_coords(data):
    '''Iterate over data array and return list of tuples with numbers and their coordinates [(nuum, (row, col), ), ]'''
    num_coords = []
    temp_coords = []
    temp_number = ''

    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col.isdigit():
                temp_coords.append((i, j))
                temp_number += col
            else:
                if temp_coords:
                    num_coords.append((int(temp_number), temp_coords))
                    temp_coords = []
                    temp_number = ''
        if temp_coords:
            num_coords.append((int(temp_number), temp_coords))
            temp_coords = []
            temp_number = ''
    if temp_coords:
        num_coords.append((int(temp_number), temp_coords))
        temp_coords = []
        temp_number = ''
    
    return num_coords

def check_adjacent(coords, data):
    '''Checks if given coords in array has adjecent part (symbol)'''

    has_adjacent_symbol = False
    x, y = coords

    # loop through all ajecent elements
    for (i, j) in [(x+1, y+1), (x+1, y), (x+1, y-1),
                  (x, y+1), (x, y), (x, y-1),
                  (x-1, y+1), (x-1, y), (x-1, y-1)]:
        # check for parts
        try:
            if not (data[i][j].isdigit() or data[i][j] == '.'):
                has_adjacent_symbol = True
                break
        except:
            pass

    return has_adjacent_symbol

def check_numbers_for_adjacent(numbers, data):
    '''
    Loop through engine parts coordinates,
    checks if they have adjecent number with check_adjecent()
    and return sum of their numbers
    '''
    sum_of_engine_parts = 0

    for engine_part in numbers:
        for coords in engine_part[1]:
            if check_adjacent(coords, data):
                sum_of_engine_parts += engine_part[0]
                break

    return sum_of_engine_parts

def check_for_gears(data):
    '''Looops over array elements and returns list of gears (*) coordinates [(row, col), ]'''
    list_of_gears_coords = []

    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == '*':
                list_of_gears_coords.append((i, j))

    return list_of_gears_coords

def check_gear_ratio(coords, numbers):
    '''
    loop through numbers coordinates and
    checks if coords are gear (have 2 adjacent number parts).
    Returns gear ratio (0 if coords not a gear)
    '''
    adjacent_parts = []
    x, y = coords

    for num in numbers:
        for num_coords in num[1]:
            for (i, j) in [(x+1, y+1), (x+1, y), (x+1, y-1),
                  (x, y+1), (x, y), (x, y-1),
                  (x-1, y+1), (x-1, y), (x-1, y-1)]:
                try:
                    if num_coords == (i, j):
                        adjacent_parts.append(num[0])
                        # if adjacent already don't check other coordinates
                        break
                except:
                    pass
            else:
                # if not adjacent try next coord
                continue
            # if number adjacent already go to next num
            break
    
    # return o if coords is not a gear, else return it's ratio
    return adjacent_parts[0]*adjacent_parts[1] if len(adjacent_parts) == 2 else 0



def star1():
    print("Sum of part numbers is", check_numbers_for_adjacent(list_numbers_coords(data), data))

def star2():
    # it's definetly not an optimal solution 
    print("Sum of gears ratios is", sum([check_gear_ratio(g, list_numbers_coords(data)) for g in check_for_gears(data)]))


star1()
star2()