# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 24


# IMPORTS
from itertools import combinations
import mpmath as mp


# CONSTANTS
# [{"pos": (x, y, z), "vel": (x, y, z)},.. ]
with open("DATA.txt") as d:
    HAIL = [{key: tuple([int(num) \
        for num in part.split(' ') if num]) \
            for key, part in zip(["pos", "vel"], tuple(line.replace(',', '').split('@')))} \
                for line in d.read().split("\n")]
AMOUNT = len(HAIL)
BOUNDS = 200000000000000, 400000000000000


# FUNCTIONS
def get_line(x, y, dx, dy):
    # y = ax + b
    return (a := dy / dx), y - a * x, x, y, dx, dy

def count_intersections(lines):
    counter = 0
    for pair in combinations(lines, 2):

        # check if parallel
        if pair[0][0] == pair[1][0]: continue

        # calculate intersection
        a1, b1, x1, _, dx1, _ = pair[0]
        a2, b2, x2, _, dx2, _ = pair[1]
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        # if intersection in future
        if  ((dx1 < 0 and x < x1) or (dx1 > 0 and x > x1))\
        and ((dx2 < 0 and x < x2) or (dx2 > 0 and x > x2)):
            
            # if intersection inside area
            if x > BOUNDS[0] and x < BOUNDS[1] and y > BOUNDS[0] and y < BOUNDS[1]:
                counter += 1

    return counter

def throw_rock():
    # That's a true shot in the dark, but when I try to grasp this in my mind
    # it seems that if we find a line that intersects with 3 other lines
    # It should be a single solution (with some luck) and so it would be THE solution.
    #
    # Now let's do some algebra
    #
    # Well, for a single hailstone we have:
    # x + dx*t = x1 + dx1 * t
    #
    # So we can find the time when two hailstones will be in the same place:
    # (x - x1) / (dx1 - dx) = (y - y1) / (dy1 - dy) = (z - z1) / (dz1 - dz)
    #
    # Now let's isolate rock trajectrory:
    # x*dy - x*dy1 - x1*y1 + x1*dy = y*dx1 - y*dx - y1*dx1 + y1*dx
    # (x*dy - y*dx) = (x*dy1 - y*dx1) + (y1*dx1 - x1*dy1) + (x1*y - y1*x)
    # *same for y and z*
    #
    # now, I wont transfer it from paper to here, but if we substitute our equations,
    # we get set of nine equations in the form of:
    # x*(dy1 -dy2) - y*(dx1 - dx2) - dx*(y1 - y2) + dy*(x1 - x2) = (y2*dx2 - x2*dy2) - (y1*dx1 - x1*dy1)
    # 
    # We can solve it with matrices:

    # get first three hailstones
    hail = HAIL[:3]
    pos1, vel1 = hail[0].values()
    pos2, vel2 = hail[1].values()
    pos3, vel3 = hail[2].values()
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    x3, y3, z3 = pos3
    dx1, dy1, dz1 = vel1
    dx2, dy2, dz2 = vel2
    dx3, dy3, dz3 = vel3

    # populate matrices
    left_side_matrix = [
        [dy1 - dy2,   dx2 - dx1,   0.0,         y2 - y1,   x1 - x2,   0.0    ],
        [dy1 - dy3,   dx3 - dx1,   0.0,         y3 - y1,   x1 - x3,   0.0    ],
        [dz2 - dz1,   0.0,         dx1 - dx2,   z1 - z2,   0.0,       x2 - x1],
        [dz3 - dz1,   0.0,         dx1 - dx3,   z1 - z3,   0.0,       x3 - x1],
        [0.0,         dz1 - dz2,   dy2 - dy1,   0.0,       z2 - z1,   y1 - y2],
        [0.0,         dz1 - dz3,   dy3 - dy1,   0.0,       z3 - z1,   y1 - y3]
    ]

    right_side_matrix = [
        (y2*dx2 - x2*dy2) - (y1*dx1 - x1*dy1),
        (y3*dx3 - x3*dy3) - (y1*dx1 - x1*dy1),
        (x2*dz2 - z2*dx2) - (x1*dz1 - z1*dx1),
        (x3*dz3 - z3*dx3) - (x1*dz1 - z1*dx1),
        (z2*dy2 - y2*dz2) - (z1*dy1 - y1*dz1),
        (z3*dy3 - y3*dz3) - (z1*dy1 - y1*dz1)
    ]

    # and so we can use matrixes to solve this system of equations as follows:
    # left_side_matrix * rock = right_side_matrix
    #
    # let's rearrange it:
    # rock = left_side_matrix^-1 * right_side_matrix
    # and so:
    mp.mp.dps = 100 # arbitrary precision, probably more than enough, but it does it in a blink of an eye
    left_side_matrix_precise = mp.matrix(left_side_matrix)
    right_side_matrix_precise = mp.matrix(right_side_matrix)
    rock = mp.lu_solve(left_side_matrix_precise, right_side_matrix_precise)

    # return the sum of starting coordinates of the rock
    return int(rock[0] + rock[1] + rock[2])


# MAIN
def star1():
    lines = [get_line(*hail["pos"][:2], *hail["vel"][:2]) for hail in HAIL]
    print("Part 1:", count_intersections(lines))

def star2():
    print("Part 2:", throw_rock())  


# EXECUTE
star1()
star2()




