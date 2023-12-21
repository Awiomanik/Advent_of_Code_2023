# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 19 


# GET DATA
with open("DATA.txt", 'r') as data_file:
    data = data_file.read().split('\n')
    work_flows = data[:(ind:=data.index(''))]
    # workflows
    # I guess I might have over done this dictionary, 
    # it would be easier to just key it by name an put lists as values,
    # but it's done so I'll go with it
    work_flows = [{'name': \
                        (ws := w.split('{'))[0], \
                   'rules': \
                        [{'condition': rs[0] if len(rs := rule.split(':')) == 2 else None, \
                          'destination': rs[1] if len(rs) == 2 else rs[0][:-1]} \
                            for rule in ws[1].split(',')]} \
                            for w in work_flows]
    # parts
    parts = [{'x': int((ps := part.split(','))[0][3:]), \
              'm': int(ps[1][2:]), \
              'a': int(ps[2][2:]), \
              's': int(ps[3][2:-1])} \
             for part in data[ind+1:]]
    # parts ratings 
    ratings = [p['x'] + p['m'] + p['a'] + p['s'] for p in parts]


# UTILITY FUNCTIONS
def check_condition(condition, part):
    '''Self-explanatory ;)'''
    if condition[1] == '<':
        return part[condition[0]] < int(condition[2:])
    else:
        return part[condition[0]] > int(condition[2:])

def go_through_work_flow(rules, part):
    '''Returns destination to which given part is directed by given rules'''

    for rule in rules:
        if rule['condition'] and check_condition(rule['condition'], part):
            return rule['destination']
        
    return rules[-1]['destination']

def validity(part_num):
    '''Returns final destination of a part based on conditions in work_flows'''
    # set starting work_flows name 
    work_flow = 'in'

    # iterate through conditions and destinations
    while True:
        # get work_flow from work_flows
        work_flow = next((d for d in work_flows if d.get('name') == work_flow), work_flow)
        # get destination name from work_flow
        work_flow = go_through_work_flow(work_flow['rules'], parts[part_num])

        # return 0 if part not accepted
        if work_flow == 'R': return 0
        # return rating if part accepted
        elif work_flow == 'A': return ratings[part_num]

def trace_back(work_flow='in', ranges={r: (1, 4000) for r in 'xmas'}):
    '''
    Recursive generator function returning all possible paths through work_flows
    a part can take depending on it's x, m, a, s values,
    that end as part beeing accepted,
    packed into dictionary as boundary values on which
    the path splits between workflows keyed by category.
    
    Generator element:
    {'x': (int, int), 'm': (int, int), 'a': (int, int), 's': (int, int)}
    '''
    # get rules assigned to a given work_flow
    rules = next((d for d in work_flows if d.get('name') == work_flow), work_flow)['rules']

    # copy ranges in case of splitting paths
    new_ranges = ranges.copy()

    # loop through rules
    for rule in rules:
        # set variables for clarity
        condition, destination = rule['condition'], rule['destination']

        # if there is condition (it's not the last bit of rule), split ranges based on condition
        if condition:
            new_ranges, ranges = split_ranges(ranges, condition)
        # if there is no condition (it's last bit of rule)
        else:
            new_ranges = ranges

        # if redirected or no condition, check if acepted
        if new_ranges:
            # reached end of recursion (part accepted)
            if destination == 'A':
                yield new_ranges
            # did not reach end of recursion, recurse deeper
            elif destination != 'R':
                yield from trace_back(destination, new_ranges)

def split_ranges(ranges, condition):
    '''
    Returns ranges splited into new and current,
    based on condition
    None if no condition didn't split the range
    '''
    # retrive category and other variables
    category = condition[0]
    category_min, category_max = ranges.get(category)
    sign = condition[1]
    value = int(condition[2:])
    new_ranges = ranges.copy()

    # new_ranges (condition met):
    if sign == '>':
        # if condition is not satisfied at all
        if value > category_max:
            new_ranges = None
        # if condition satisfied, update lower bound
        category_min = max(category_min, value + 1)

    else: # sign == '<':
        if value < category_min:
            new_ranges = None
        category_max = min(category_max, value - 1)

    # update new_anges
    if new_ranges:
        new_ranges[category] = (category_min, category_max)


    # current ranges (condition not met)
    # set variables for reversed process
    sign, value = ('>', value-1) if sign == '<' else ('<', value+1)
    category_min, category_max = ranges.get(category)
    current_ranges = ranges.copy()

    if sign == '>':
        # if condition is not satisfied at all
        if value > category_max:
            current_ranges = None
        # if condition satisfied, update lower bound
        category_min = max(category_min, value + 1)

    else: # sign == '<':
        if value < category_min:
            current_ranges = None
        category_max = min(category_max, value - 1)

    # update current_ranges
    if current_ranges:
        current_ranges[category] = (category_min, category_max)

    return new_ranges, current_ranges

def count_combinations(paths):
    '''Returns amount of combinations in all (accepted) paths'''
    total = 0
    for path in paths:
        combinations = 1
        for r in path.values():
            combinations *= (r[1] - r[0] + 1)
        total += combinations
    return total


# MAIN
def star1():
    print("Part 1:", sum([validity(part) for part in range(len(parts))]))

def star2():
    print("Part2:", count_combinations(trace_back()))

star1()
star2()
