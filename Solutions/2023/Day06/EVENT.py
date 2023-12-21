# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 6

from functools import reduce
import math as mt
import time as tm

# GET DATA
data = [(50, 242), (74, 1017), (86, 1691), (85, 1252)]
#test data
#data = [(7, 9), (15, 40), (30, 200)]


# UTILITY FUNCTIONS
def all_times(time, dist):

    winning_run  = 0
    for hold in range(time):
        if hold*(time-hold) > dist:
            winning_run += 1

    return(winning_run)

def convert_data_for_star2(d):
    resoult = []

    for d in data:
        resoult.append((str(d[0]), str(d[1])))

    resoult = reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), resoult)

    return (int(resoult[0]), int(resoult[1]))

def star2_brute_force(t, d):
    return all_times(t, d)
def star2_algrithmically(t, d):
    # Let t be the the total race time.
    # Let d be record distance.
    #
    # The distance D that the boat will swim 
    # is given by it's speed defined as the time of holding the button T
    # and time left to swim (t-T).
    # Question is how many of such descrite intiger times T 
    # wil give us a value larger than d.
    # 
    # We are looking for intigers in range given by inequality:
    # -T^2 + tT - D > 0
    # Let the distnace between them be cold delta_t, then:
    delta_t = mt.sqrt(t**2 - 4*d)
    return int((delta_t))


def star1():
    resoult = []
    
    for d in data:
        resoult.append(all_times(d[0], d[1]))

    print("star1:", reduce(lambda x, y: x*y, resoult))

def star2():
    d = convert_data_for_star2(data)

    t1 = tm.time()
    print("star2 using brute force:", star2_brute_force(d[0], d[1]))
    t2 = tm.time()
    print("star2 using mathematics:", star2_algrithmically(d[0], d[1]))
    t3 = tm.time()

    print(f"Brute force algorythm took:     {t2-t1:.4f}s")
    print(f"Mathematical algorythm it took: {t3-t2:.4f}s")
    print(f"Ratio: {(t3-t2)/(t2-t1):.6f} to 1")


star1()
star2()