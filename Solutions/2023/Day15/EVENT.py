# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 15


# PARAMETERS
data_path = "DATA.txt"


# GET DATA
with open(data_path, 'r') as data_file:
    data = data_file.read().split(',')


# UTILITY FUNCTIONS
def hash(string):
    '''
    Hashing function
    Returns intiger in range [0-255]
    '''
    result = 0

    for char in string:
        result += ord(char)
        result *= 17
        result = result%256

    return result

def data2boxes():
    '''
    Returns contents of boxes after executing instructions in data,
    as a dictionary keyed by box number with values corresponding to its content
    {box (int): [(label (str), focal length (str)),.. ],.. }
    '''
    # initialize dictionary of boxes of lists of lenses
    boxes = {key: [] for key in range(256)}

    # iterate over instruction steps
    for step in data:
        # subrtacting instruction
        if '-' in step:
            current_label = step[:-1]
            current_box = hash(current_label)

            # remove lens
            for lens in boxes[current_box]:
                if lens[0] == current_label:
                    boxes[current_box].remove(lens)
                    break

        # setting instruction
        else:
            current_label, current_focal = step.split('=')
            current_box = hash(current_label)

            # set lens in box
            # swap lenses
            for lens in boxes[current_box]:
                if lens[0] == current_label:
                    boxes[current_box][boxes[current_box].index(lens)] = (current_label, current_focal)
                    break

            # add lens
            else:
                boxes[current_box].append((current_label, current_focal))

    return boxes

def focusing_power(boxes):
    '''Returns focusing power of given lens configuration'''

    result = []
    for key, value in boxes.items():
        if value != []:
            for i, lens in enumerate(value):
                result.append((1 + key) * (i+1) * int(lens[1]))
    
    return sum(result)

# MAIN FUNCTIONS
def star1():
    print("Part 1:", sum([hash(d)for d in data]))
                    
def star2():
    print("Part 2:", focusing_power(data2boxes()))

star1()
star2()
