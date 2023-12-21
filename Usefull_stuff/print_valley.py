from functools import reduce
import time

def print_valley(valley, tempo, return_coursor=True):
    '''Print valley state '''
    # print top edge
    print("\r\u256d" + "\u257c" * len(valley[0]) + "\u256e")
    # print valley
    for line in valley[::-1]:
        print("\r\u257d" + reduce(lambda x, y: x+y, line) + "\u257f")
    # print bottm edge
    print("\r\u2570" + "\u257e" * len(valley[0]) + "\u256f", flush=True, end='')

    # tempo of animation
    time.sleep(tempo)

    # return coursor to the top
    if return_coursor:
        for _ in range(len(valley) + 1):
            print("\033[A", flush=True, end='')
        print('\r', end='')

    print(flush=True, end='')