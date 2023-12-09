# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 1

# PARAMETERS
data_path = "DATA.txt"

#CONSTANTS
str_digit = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

str_digit_rev = {
    'eno': 1,
    'owt': 2,
    'eerht': 3,
    'ruof': 4,
    'evif': 5,
    'xis': 6,
    'neves': 7,
    'thgie': 8,
    'enin': 9
}


# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')

def digits_num(value):
    '''Resturns first an last digit in a string (int, int)'''
    digit1 = 0
    digit2 = 0


    # first to appear digit
    for i in value:
        if i.isdigit():
            digit1  = int(i)
            break
    
    # last to apear digit (first from the end)
    for i in range(len(value)-1,-1,-1):
        if value[i].isdigit():
            digit2 = int(value[i])
            break

    return digit1, digit2

def digits_num_or_str(value):
    '''Resturns first an last digit (also if represanted as string) in a string (int, int)'''

    #reversed string so that .find() will return last digit
    value_rev = value[::-1]

    # FIRST DIGIT
    digit_num = 0
    index_num = len(value)

    digit_str = 0
    index_str = len(value)


    # find first num digit and it's index
    for c in value:
        if c.isdigit():
            digit_num = int(c)
            index_num = value.index(c)
            break

    # find first str digit and it's index
    for s in str_digit.keys():
        temp_index = value.find(s)
        if temp_index != -1: # if found
            if temp_index <= index_str:
                index_str = temp_index
                digit_str = str_digit[s]

    # Compare first indecies to find first appearance
    if index_num < index_str:
        digit1 = digit_num
    else:
        digit1 = digit_str

    # LAST DIGIT
    # reset variables
    digit_num = 0
    index_num = len(value)

    digit_str = 0
    index_str = len(value)

    # find last num digit (first in reversed string) and it's index
    for c in value_rev:
        if c.isdigit():
            digit_num = int(c)
            index_num = value_rev.index(c)
            break

    # find last (first in reversed string) str digit and it's index
    for s in str_digit_rev.keys():
        temp_index = value_rev.find(s)
        if temp_index != -1: # if found
            if temp_index <= index_str:
                index_str = temp_index
                digit_str = str_digit_rev[s]

    # Compare last indecies to find last appearance
    if index_num < index_str:
        digit2 = digit_num
    else: 
        digit2 = digit_str

    #print(value)
    #print(digit1*10 + digit2)
    #print()

    return digit1, digit2


def star1():
    resoult = []
    for d in data:
        tens, units = digits_num(d)
        resoult.append(tens*10 + units)

    #print(resoult)
    print(sum(resoult))

def star2():
    resoult = []
    for d in data:
        tens, units = digits_num_or_str(d)
        resoult.append(tens*10 + units)

    #print(resoult)
    print(sum(resoult))


star1()
star2()