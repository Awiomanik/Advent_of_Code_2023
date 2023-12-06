# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 5

# PARAMETERS
data_path = "DATA.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    #print("DATA:\n", data)

# UTILITY FUNCTIONS
def get_mappings_dicts(d):
    '''
    Gets mappings data from data list of strings
    Returns list of subsequent mapping lists of ranges dicts
            [[{'source': #, 'destination': #, 'length': #}, ...], ...]
    '''
    # start after seeds and empty row
    maps_temp = d[2:]
    maps_final = []
    mapping_ranges = []

    for range in maps_temp:
        if range != '':
            mapping_ranges.append(range)
        else:
            maps_final.append(mapping_ranges)
            mapping_ranges = []

    # maps final contains list of lists of strings describing mappings ranges
    maps_final.append(mapping_ranges)

    # discard description strings and convert strings into dicts
    return [[{'source': int((sp := span.split(' '))[1]), \
              'destination': int(sp[0]), \
              'length': int(sp[2])} \
                for span in m] \
                for m in [line[1:] for line in maps_final]]

def get_individual_seeds(d):
    '''Get first line of data, extract prefix, split into numbers, convert to intigers'''
    return [int(s) for s in d[0][6:].split(' ') if s != '']

def single_maping(number, maping):
    '''
    Takes:      number and list of mapping pharallel dicts
    Returns:    number mapped with applicable dict or number if out of every dict range
    '''
    for m in maping:
        s, d, l = m['source'], m['destination'], m['length']

        if number in range(s, s+l):
            number = number - s + d
            break

    return number

def all_mapings(seed, maps):
    '''Retuns seed mapped through all subsequent dicts in mapping list'''
    for m in maps:
        seed = single_maping(seed, m)

    return seed


def star1():
    # get data
    maps = get_mappings_dicts(data)
    seeds = get_individual_seeds(data)

    # map data
    s = []
    for seed in seeds:
        s.append(all_mapings(seed, maps))

    #find min
    print(min(s))


def star2():
    pass


star1()
#star2()