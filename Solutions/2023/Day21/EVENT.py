# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 21

# CONSTANTS
steps2make = 26501365

from functools import reduce
import sys
sys.path.append(r"..\..\..\Usefull_stuff")
from loading_bar import LoadingBar as lb



# GET DATA
with open("DATA.txt", "r") as d:
    DATA = d.read().split("\n")
    WIDTH, HEIGHT = len(DATA[0]), len(DATA) # I realized their the same too late


# UTILITY FUNCTIONS
def find_start():
    '''Finds the starting position'''
    for y in range(WIDTH):
        for x in range(HEIGHT):
            if DATA[y][x] == "S":
                return x, y
            
def find_valid_neighbors(coords):
    '''Finds valid neighbors'''
    # unpack coords
    x, y = coords

    # list of valid neighbors
    neighbors = set()

    # check all 4 directions
    for (x1, y1) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:

        # if neighbor in bounds and not a rock
        if 0 <= x1 < WIDTH and 0 <= y1 < HEIGHT and DATA[y1][x1] != "#": 
            neighbors.add((x1, y1))

    return neighbors

def print_garden(step, plots): # for testing purposes
    '''Prints the plots'''

    print("step:", step)
    grid = [reduce(lambda x, y: x+y, [DATA[y][x] if not (x, y) in plots else 'O' for x in range(WIDTH)]) for y in range(HEIGHT)]
    print("\n".join(grid))
    print()

def walk(start=find_start(), steps=64):
    '''Walks the path'''

    # initialize
    current_plots = {start}
    bar = lb(steps) # loading bar for progress tracking

    # iterate for the specified number of steps
    for i in range(steps):
        # display progress
        bar.update(i+1, skip_every_other=10)

        # update current_plots
        all_neighbors = set()
        for plot in current_plots: 
            valid_neighbors = find_valid_neighbors(plot)
            all_neighbors |= valid_neighbors

        current_plots = all_neighbors

    # close loading bar
    bar.close(False) 

    return current_plots

def flood_fill(start=find_start()):
    '''Flood fills the garden'''

    # initialize
    current_plots = {start}
    #print("flooding...", end="")

    # iterate until all plots are filled
    amount = 0
    while True:

        # update current_plotsw
        all_neighbors = set()
        for plot in current_plots: 
            valid_neighbors = find_valid_neighbors(plot)
            all_neighbors |= valid_neighbors

        current_plots |= all_neighbors

        if len(current_plots) == amount: break
        amount = len(current_plots)

    #print("\rflooding done")
    return current_plots

def extract_diamond(plots, start=find_start()):
    return {plot for plot in plots if abs(plot[0] - start[0]) + abs(plot[1] - start[1]) <= WIDTH // 2}

def extract_corners(plots, corner, start=find_start()):
    if corner == "lt":
        return {plot for plot in plots if abs(plot[0] - start[0]) + abs(plot[1] - start[1]) > WIDTH // 2 and plot[0] < start[0] and plot[1] < start[1]}
    elif corner == "rt":
        return {plot for plot in plots if abs(plot[0] - start[0]) + abs(plot[1] - start[1]) > WIDTH // 2 and plot[0] > start[0] and plot[1] < start[1]}
    elif corner == "lb":
        return {plot for plot in plots if abs(plot[0] - start[0]) + abs(plot[1] - start[1]) > WIDTH // 2 and plot[0] < start[0] and plot[1] > start[1]}
    elif corner == "rb":
        return {plot for plot in plots if abs(plot[0] - start[0]) + abs(plot[1] - start[1]) > WIDTH // 2 and plot[0] > start[0] and plot[1] > start[1]}

def count_gardens(steps):
    
    diagonal = (steps - (WIDTH // 2)) // WIDTH
    print("diagonal:", diagonal)

    # diagonal = 1/4 outer = 1/4 (inner+1)
    # there are 4 vertices
    # outer + inner from the same edge fully encapsulate the garden

    # 1 + 2 + 3 + 4 + ... + n = n(n+1)/2
    # n = diagonal - 1
    fully_encapsulated = 1 + 4 * ((diagonal + 1) * (diagonal + 2) // 2)
    # fully encapsulated contains inner diamonds and almost all edges
    # we have 4 vertecies and 4 outer left 
    # 2 vertices with 4 edges fully encapsulat the 2 gardens
    # we have 2 vertices to count
    # 2 vertices encapsulate 1 garden and 1 diamond, so

    gardens = fully_encapsulated + 3

    # one more diamond needs to be accounted for

    return gardens

def calculate_parity(plots) -> (int, int):
    '''
    Calculates the parity of the plots
    Returns a tuple (even, odd)
    '''
    even = 0
    odd = 0
    for plot in plots:
        x, y = plot
        if (x + y) % 2 == 0: even += 1
        else: odd += 1

    return even, odd

def test_walk():
    test_cases = [
        (6, 16),
        (10, 50),
        (50, 1594),
        (100, 6536),
        (500, 167004),
        (1000, 668697),
        (5000, 16733044)
    ]

    for steps, expected in test_cases:
        print(f"Testing for {steps} steps")
        result = len(walk(steps=steps))
        print(f"Result: {result}")
        print()
        if result != expected: raise AssertionError(f"For {steps} steps, expected {expected} but got {result}")

def count_gardens(steps) -> (int, int):

    # number of full gardnes from start (inclusive) to the vertex
    diagonal = (steps - (WIDTH // 2)) // WIDTH
    
    #print("diagonal:", diagonal)

    # amount of fully encapsulated gardens per parity
    # sum of even numbers: S = n(n+1)
    even = 4 * (diagonal - 1) * (diagonal - 2) + 1
    # sum of odd numbers: S = (n/2)^2
    odd = 4 * ((diagonal // 2) ** 2)
    
    #print("even:", even)
    #print("odd:", odd)

    # we got amount of fully encapsulated gardens
    # now we need to add the edges and the vertices

    # all edges are the same parity
    fractions = diagonal % 2 == 0
    #print("fractions even:", fractions)

    # add daimonds
    daimonds = diagonal * 4
    #print("daimonds:", daimonds)

    return even, odd, fractions, daimonds, diagonal


# SOLUTION
def star1():
    print("Part 1:", len(walk()))

def star2():
    # check all reachable plots
    all_plots = flood_fill()
    #print_garden("odd", {plot for plot in all_plots if (plot[0] + plot[1]) % 2 == 0})
    #print_garden("even", {plot for plot in all_plots if (plot[0] + plot[1]) % 2 == 1})
    
    # devide them into even and odd
    full_even, full_odd = calculate_parity(all_plots)
    #print("plots:\t", full_even, full_odd)
    #print()

    diamond_plots = calculate_parity(extract_diamond(all_plots))
    #print_garden("odd", {plot for plot in extract_diamond(all_plots) if (plot[0] + plot[1]) % 2 == 0})
    #print_garden("even", {plot for plot in extract_diamond(all_plots) if (plot[0] + plot[1]) % 2 == 1})
    #print("diamond:", diamond_plots)

    l_d = calculate_parity(extract_corners(all_plots, "lt"))
    l_t = calculate_parity(extract_corners(all_plots, "lb"))
    r_d = calculate_parity(extract_corners(all_plots, "rt"))
    r_t = calculate_parity(extract_corners(all_plots, "rb"))
    #print("corners:")
    #print("lt:", l_d_even, l_d_odd)
    #print("lb:", l_t_even, l_t_odd)
    #print("rt:", r_d_even, r_d_odd)
    #print("rb:", r_t_even, r_t_odd)

    # calculate the number of gardens
    even, odd, fractions, diamonds, diagonal = count_gardens(steps2make)

    # calculate the number of plots
    plots = (odd * full_odd + even * full_even)
    plots += (diamond_plots[int(fractions)] * diamonds)
    plots += (l_d[int(fractions)] * diagonal \
            + l_t[int(fractions)] * diagonal \
            + r_d[int(fractions)] * diagonal \
            + r_t[int(fractions)] * diagonal)

    print("Part 2:", plots)

#test_walk()
star1()
star2()








