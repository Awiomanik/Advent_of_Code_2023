# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: (test from 2022)


# PARAMETERS
data_path = "25_2022_data.txt"

# CONSTANTS
SNAFU_digit2Decimal_digit = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}
Decimal_digit2SNAFU_digit = {value: key for key, value in SNAFU_digit2Decimal_digit.items()}

# GET DATA
data = []
with open(data_path, 'r') as data_file:
    data = data_file.read().split('\n')


# UTILITY FUNCTIONS
def SNAFU2Decimal(SNAFU_num_string):
    '''
    Takes:      str Number in SNAFU units
    Returns:    int Number in Decimal format
    '''
    resoult = 0

    for i, digit in enumerate(list(SNAFU_num_string)[::-1]):
        resoult += SNAFU_digit2Decimal_digit[digit] * (5 ** i)
        
    return resoult

def Decimal2SNAFU(decimal_num):
    '''
    Takes:      int Number in Decimal format
    Returns:    str Number in SNAFU units
    '''
    resoult = ''
    ord_mag = SNAFU_order_of_magnitude_from_decimal(decimal_num) - 1
    
    # Iterate over digits from the largest one
    # and choose digit that is closest to 0
    while ord_mag >= 0:

        # all numbers that can be reached with one digit
        reduced_numbers = [abs(decimal_num - (digit * (5 ** ord_mag))) \
                           for digit in [2, 1, 0, -1, -2]][::-1]
        
        # choosing digit that minimizes abs(number)
        digit_of_reduced = reduced_numbers.index(min(reduced_numbers)) - 2

        # update number, resoult and order of magnitude
        decimal_num = decimal_num - digit_of_reduced * 5 ** ord_mag
        resoult += Decimal_digit2SNAFU_digit[digit_of_reduced]
        ord_mag -= 1

        #print("Order:   ",ord_mag)
        #print("dec num: ",decimal_num)
        #print("red num: ",reduced_numbers)
        #print("Resoult: ",resoult)
        #print()

    return resoult

def SNAFU_order_of_magnitude_from_decimal(decimal_num):
    '''Returns number of digits in SNAFU units based on Decimal number'''
    order_of_magnitude = 0
    while True:
        decimal_num = decimal_num - 2 * 5**order_of_magnitude
        if decimal_num <= 0:
            return order_of_magnitude + 1
        order_of_magnitude += 1


def star1():

    print(Decimal2SNAFU(sum([SNAFU2Decimal(n) for n in data])))
    
def star2():

    print("Shortest total distnce is", distance1 + distance2 + distance3)


# Testing:
example_S2D = [("1=-0-2", 1747),
                    ("12111", 906),
                    ("2=0=", 198),
                    ("21", 11),
                    ("2=01", 201),
                    ("111", 31),
                    ("20012", 1257),
                    ("112", 32),
                    ("1=-1=", 353),
                    ("1-12", 107),
                    ("12", 7),
                    ("1=", 3),
                    ("122", 37)]

example_D2S = [(1, "1"),
                (2, "2"),
                (3, "1="),
                (4, "1-"),
                (5, "10"),
                (6, "11"),
                (7, "12"),
                (8, "2="),
                (9, "2-"),
                (10, "20"),
                (15, "1=0"),
                (20, "1-0"),
                (2022, "1=11-2"),
                (12345, "1-0---0"),
                (314159265, "1121-1110-1=0")]

# SNAFU2Decimal():
def test_SNAFU2Decimal():
    print("SNAFU2Decimal() TEST:")
    print(SNAFU2Decimal("20") == 10)
    print(SNAFU2Decimal("2=") == 8)
    print(SNAFU2Decimal("2=-01") == 976)
    print(all([SNAFU2Decimal(e[0]) == e[1] for e in example_S2D]))
    print(all([SNAFU2Decimal(e[1]) == e[0] for e in example_D2S]))
    print(SNAFU2Decimal("0") == 0)
    print()

# Decimal2SNAFU():
def test_Decimal2SNAFU():
    print("Decimal2SNAFU() TEST:")
    print(Decimal2SNAFU(10) == "20")
    print(Decimal2SNAFU(8) == "2=")
    print(Decimal2SNAFU(976) == "2=-01")
    print(Decimal2SNAFU(353) == "1=-1=")
    print(Decimal2SNAFU(1747) == "1=-0-2")
    print(all([Decimal2SNAFU(e[1]) == e[0] for e in example_S2D]))
    print(all([Decimal2SNAFU(e[0]) == e[1] for e in example_D2S]))
    print(Decimal2SNAFU(0) == "0")
    print()

# SNAFU_order_of_magnitude_from_decimal():
def test_SNAFU_order_of_magnitude_from_decimal():
    print("SNAFU_order_of_magnitude_from_decimal() TEST:")
    print(all([SNAFU_order_of_magnitude_from_decimal(num[1]) == len(num[0]) for num in example_S2D]))
    print(all([SNAFU_order_of_magnitude_from_decimal(num[0]) == len(num[1]) for num in example_D2S]))
    print(SNAFU_order_of_magnitude_from_decimal(67832538764538649) == \
          len(Decimal2SNAFU(67832538764538649)) == 25)
    print(SNAFU_order_of_magnitude_from_decimal(0) == 1)
    print()

#test_SNAFU2Decimal()
#test_Decimal2SNAFU()
#test_SNAFU_order_of_magnitude_from_decimal()

star1()
#star2()
