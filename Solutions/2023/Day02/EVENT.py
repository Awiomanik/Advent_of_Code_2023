# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 2

import math

# PARAMETERS
data_path = "DATA.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    # lose prefix
    data_games = [d.split(': ')[1] for d in data]
    # devide into lists of sets
    data_games_sets = [g.split(';') for g in data_games]

    #print(sets)

#VARIABLES
colors = {'red': 0,
          'green': 0,
          'blue': 0}

def count_colors_in_set(set):
    '''Returns dict of colours with value count'''
    return_dict = dict(colors)

    set = set.split(', ')
    for c in set:
        count, color = c.split()
        return_dict[color] += int(count)
    
    #print("set:", return_dict)
    return return_dict


def star1():
    # sum of ID's of possible gmaes
    sum = 0

    for i, game in enumerate(data_games_sets):
        not_exceeded = True

        for set in game:
            counted = count_colors_in_set(set)

            # check if no colour exceeded it's limit
            if not (counted['red'] <= 12 \
            and counted['green'] <= 13 \
            and counted['blue'] <= 14):
                not_exceeded = False

        if not_exceeded == True:
            sum += i + 1
            #print(i + 1, game, counted, sum)
    
    print(sum)

def star2():
    powers_of_sets = []

    for game in data_games_sets:
        colors_counted_in_game = dict(colors)

        for set in game:
            counter = count_colors_in_set(set)

            # save highest number of cubes per colour per game
            for c in counter:
                if counter[c] > colors_counted_in_game[c]:
                    colors_counted_in_game[c] = counter[c]

        # sppend product of the number of cubes for each colour
        powers_of_sets.append(math.prod([colors_counted_in_game[c] for c in colors_counted_in_game]))

    print(sum(powers_of_sets))



star1()
star2()