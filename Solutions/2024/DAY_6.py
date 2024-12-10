"""
Advent of Code 2024 - Day 6

This script contains my solution for **Advent of Code 2024, Day 6**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_6_input.txt` located in the same directory as this script.
- Example: `python DAY_6.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

# IMPORTS
from os import system

# my utils:
import sys
from pathlib import Path
# Dynamically add the Usefull_stuff directory to sys.path
current_dir = Path(__file__).resolve().parent
usefull_stuff_dir = current_dir.parent.parent / "Usefull_stuff"
sys.path.insert(0, str(usefull_stuff_dir))
from coord import COORD
from loading_bar import LoadingBar as Bar

# PARAMETERS
whether_animate_search_for_solution_star_1: bool = False
whether_animate_search_for_solution_star_2: bool = False

# Get data
data: list[list[str]] = [list(char) for char in open("day_6_input.dat").read().split('\n')]


# < --- 1'st STAR --- >
# Utils
width: int = len(data[0])
height: int = len(data)
size: COORD = COORD(width, height)
visited: list[list[bool]] = [[False for _ in range(height)] for _ in range(width)]
guard_pos: COORD = None
guard_dir: COORD = None
direction: dict[str, COORD] = {
    '>': COORD(1, 0),
    '<': COORD(-1, 0),
    '^': COORD(0, -1),
    'v': COORD(0, 1)
}
rot: dict[COORD, COORD] = {
    COORD(1, 0): COORD(0, 1),    # '>' to 'v'
    COORD(0, 1): COORD(-1, 0),   # 'v' to '<'
    COORD(-1, 0): COORD(0, -1),  # '<' to '^'
    COORD(0, -1): COORD(1, 0)    # '^' to '>'
}
if whether_animate_search_for_solution_star_1: lab = data
laboratory: list[list[bool]] = [row[:] for row in visited]
"""True - obsticle, False - empty spot"""

# Map the laboratory and find the guard
for y, line in enumerate(data):
    for x, char in enumerate(line):
        # Map the laboratory
        if char == '#':
            laboratory[y][x] = True

        elif char in ['^', 'v', '<', '>']:
            # Set variables
            guard_pos = COORD(x, y)
            guard_dir = direction[char]
            visited[y][x] = True

            # For 2'nd STAR
            start_pos = guard_pos
            start_dir = guard_dir

            # Animation
            if whether_animate_search_for_solution_star_1: lab[y][x] = '.'

# Walk of the guardian
while True:

    # Update guards position and savve it to the temporary variable
    temp_pos = guard_pos + guard_dir
    
    # Guard walked out of the laboratory
    if temp_pos < 0 or temp_pos > size: 
        break

    # Obsticle encountered, rotate the guard
    if laboratory[temp_pos.y][temp_pos.x]:
        guard_dir = rot[guard_dir]

    # Move the guard
    else:
        guard_pos = temp_pos
        visited[guard_pos.y][guard_pos.x] = True

    # Walk animation
    if whether_animate_search_for_solution_star_1:
        system("cls")
        for y, line in enumerate(lab):
            for x, char in enumerate(line):
                if guard_pos == COORD(x, y):
                    print(next((k for k, v in direction.items() if v == guard_dir), 'X'), end='')
                else:
                    print(char, end='')
            print()

        print("\nGuards position: ", guard_pos)
        print("\nGuards direction: ", 
              next((k for k, v in direction.items() if v == guard_dir), 'X'))

print("\n1'st star solution:\n")
print(sum([sum(line) for line in visited]))


# < --- 2'nd STAR --- >
# Utils
counter: int = 0
print("\n2'nd star solution:\n")
if not whether_animate_search_for_solution_star_2: bar: Bar = Bar(height)

# Iterate over different places to set the obsticle
for x in range(width):
    for y in range(height):

        # Do not place the obsticle if the guardian won't encounter it
        if not visited[y][x]: continue

        # Do not stack obsticles on top of each other
        # That is just a waste of energy
        if laboratory[y][x]: continue

        # Do not place the obsticle on the guard!!!
        # Interaction with people from the past can easly lead to time-paradoxes and
        # in consequence fructure the fabric of spece-time itself!
        if COORD(x, y) == start_pos: continue

        # Reset variables for this iteration
        visited2: dict[COORD, COORD] = {}
        obsticle = COORD(x, y)
        guard_pos = start_pos
        guard_dir = start_dir

        # Walk of the Guard
        while True:

            # Update guards position and savve it to the temporary variable
            temp_pos = guard_pos + guard_dir
            
            # Guard walked out of the laboratory
            if 0 > temp_pos or temp_pos > size: 
                break

            # Obsticle encountered, rotate the guard
            if laboratory[temp_pos.y][temp_pos.x] or temp_pos == obsticle:
                guard_dir = rot[guard_dir]

            # Move the guard and check if he looped
            else:
                # Move the guard
                guard_pos = temp_pos
                
                # check if he looped
                if guard_pos in visited2 and visited2[guard_pos] == guard_dir:
                    counter += 1

                    # Print foud solution for animation
                    if whether_animate_search_for_solution_star_2:
                        system("cls")
                        for y, row in enumerate(laboratory):
                            for x, tile in enumerate(row):
                                if (COORD(x, y)) in visited:
                                    print(next((k for k, v in direction.items() 
                                                if v == visited[COORD(x, y)]), 'X'), end='')
                                else:
                                    print(' ', end='')
                            print()
                        print("Solution number", counter)
                        print(f"Obsticle at ({x}, {y})")
                        #input("\nPress enter to continue")
                        
                    # Do an early break when solution is found
                    break

                # Update the visited2 dictionary
                visited2[guard_pos] = guard_dir

    # Update progress bar
    if not whether_animate_search_for_solution_star_2: bar.update(x+1, str(counter))

# Close the loading bar
if not whether_animate_search_for_solution_star_2: bar.close()

print(counter)