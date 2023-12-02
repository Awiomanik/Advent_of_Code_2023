# WOJCIECH KOŚNIK-KOWALCZUK
# ADVENT OF CODE 2022
# DAY: 4


# PARAMETERS
data_path = "4_2022_data.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')
    # split data into pairs (str, str)
    pairs = [tuple(d.split(',')) for d in data]

def str2start_end(range_str):
    """
    Convrts a string representing a range into a tuple of start and end integers.
    """
    start, end = range_str.split('-')
    return int(start), int(end) + 1


def check_inclusion(ranges):
    '''
    Takes:      list of tuples of strings represanting ranges as all included values
                [('#-#', ), ]
    Returns:    int how many pairs fully include one another  
    '''
    count = 0

    for range1, range2 in ranges:
        start1, end1 = str2start_end(range1)
        start2, end2 = str2start_end(range2)

        if start1 <= start2 and end1 >= end2 \
        or start2 <= start1 and end2 >= end1:
            count += 1

    return count 

def check_overlap(pairs):
    '''
    Takes:      list of tuples of strings represanting ranges as all included values
                [('#-#', ), ]
    Returns:    int how many pairs overlap  
    '''
    count = 0

    for range1, range2 in pairs:
        start1, end1 = str2start_end(range1)
        start2, end2 = str2start_end(range2)

        if not (end2 <= start1 or start2 >= end1):
            count += 1

    return count


def star1():
    print(check_inclusion(pairs))  
    
def star2():
    print(check_overlap(pairs))


star1()
star2()