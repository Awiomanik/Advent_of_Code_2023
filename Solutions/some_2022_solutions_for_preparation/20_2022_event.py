# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 20 (2022)

# PARAMETERS
data_path = "test2_data.txt"

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')

# UTILITY FUNCTIONS
def swap(seq, index_from, index_to):
    '''Shift element on index_from position to index_to position'''
    element = seq.pop(index_from)
    return seq[:index_to] + [element] + seq[index_to:]

def mixing(message, l, order_of_operations):
    '''\"Mixing\" decryption method'''
    for i in range(l):
        from_position = order_of_operations.index(i)
        move_by = message[from_position]
        if move_by != 0:
            to_position = (from_position + move_by) % (l-1) ##### <<<<< ----- HERE, WHY -1 ?!
            message = swap(message, from_position, to_position)
            order_of_operations = swap(order_of_operations, from_position, to_position)

    return message, order_of_operations

def find_coords(message, l):
    '''Find elements shfted by 1000, 2000 and 3000 places from 0'''
    zero = message.index(0)
    numbers = []
    for i in range(1,4):
        numbers.append(message[(zero + i*1000) % l])

    return numbers


# SOLUTIONS
def star1():
    l = len(data)
    order = [i for i in range(l)]
    message, _ = mixing([int(i) for i in data], l, order)
    numbers = find_coords(message, l)

    print("NUMBERS:  ", numbers)
    print("SUM:      ", sum(numbers))


def star2():
    l = len(data)
    message = [d*811589153 for d in [int(i) for i in data]]
    order = [i for i in range(l)]
    for _ in range(10):
        message, order = mixing(message, l, order)
    num = find_coords(message, l)

    print("NUMBERS:  ", num)
    print("SUM:      ", sum(num))

# RUN ALL
star1()
star2()