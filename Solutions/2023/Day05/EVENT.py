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

def data2seed_ranges(display=False):
    '''Returns list of tuples with ranges limits'''
    if display:
        print("Preparing ranges")
    
    d = data.copy()

    # get numbers form data
    seeds = [int(s) for s in d.pop(0)[6:].split(' ') if s != '']

    # populate return list
    seed_ranges = []
    for i in range(len(seeds)//2):
        seed_ranges.append((seeds[i*2], seeds[i*2] + seeds[i*2+1]))

        if display:
            print(str(i+1) + "/" + str(len(seeds)//2), "ranges done")
    
    if display:
        print("\nSeed ranges:")
        print(seed_ranges)
        print()

    return seed_ranges

def data2maps(d, display=False):
    '''
    Returns mappings as list of mappings with list of ranges and shifts as dictionaries:
    [[{'range': (int, int), 'shift': int},.. ],.. ]
    '''
    # cut off seeds
    maps_raw = data[2:]

    maps = []
    temp = []

    # populate maps
    for line in maps_raw:
        if line != '':
            temp.append(line)
        else:
            maps.append(temp)
            temp = []
    maps.append(temp)

    # maps to list of lists of dictionaries
    maps = [[{'range': (int((element:=range.split(' '))[1]), int(element[1]) + int(element[2])), \
               'shift': int(element[0]) - int(element[1])} \
                for range in m] \
                for m in [line[1:] for line in maps]]

    if display:
        print("Maps:")
        for m in maps:
            print(m)
        print()
    
    return maps

def map_range(seeds, mapping):
    '''Mapps single seed range by single map range'''
    
    # get limits
    seed_start, seed_end = seeds
    map_start, map_end = mapping['range']

    mapping_shift = mapping['shift']

    # case 1: no overlap
    if seed_end < map_start or map_end <= seed_start:
        #print("no overlap")
        return [seeds]

    # case 2: overlap
    segments = []

    # part before mapping
    if seed_start < map_start:
        segments.append((seed_start, map_start))

    # overlapped part
    overlap_start = max(seed_start, map_start)
    overlap_end = min(seed_end, map_end)
    segments.append((overlap_start + mapping_shift, overlap_end + mapping_shift))

    # part after mapping
    if seed_end >= map_end:
        segments.append((map_end, seed_end))

    #print(mapping, segments)
    return segments

def map_range_all_mappings(seeds, mappings):
    '''Maps every seed range in seeds with every mapping range in lists in mappings'''
    resulting_seeds = seeds.copy()

    # sequentially apply each mapping to the seeds
    for mapping in mappings:
        new_seeds = []
        #print("map", mapping)
        # for each updated seed range
        for seed_range in resulting_seeds:
            mapped_ranges = [seed_range]
            # for each range in a single mapping
            for mapping_range in mapping:
                # apply the current mapping range to all mapped ranges so far
                mapped_ranges_temp = [new_range for mapped_range \
                                      in mapped_ranges for new_range \
                                      in map_range(mapped_range, mapping_range)]
                # if mapping range included our range break out of the single mapping
                if mapped_ranges_temp != mapped_ranges:
                    mapped_ranges = mapped_ranges_temp
                    break

            new_seeds.extend(mapped_ranges)
        resulting_seeds = new_seeds

    return resulting_seeds


def star1():
    # get data
    maps = get_mappings_dicts(data)
    seeds = get_individual_seeds(data)

    # map data
    s = []
    for seed in seeds:
        s.append(all_mapings(seed, maps))

    #find min
    print("Part 1:", min(s))

def star2(display=False):
    ranges = data2seed_ranges(display)
    mappings = data2maps(data, display)

    mapped_ranges = map_range_all_mappings(ranges, mappings)
    if display:
        print("Mapped Ranges:")
        for m in mapped_ranges:
            print(m)

    lowest_number = min(mapped_ranges)[0]
    print("Part 2:", lowest_number)


star1()
star2(False)