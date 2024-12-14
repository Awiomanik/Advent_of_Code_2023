"""
Advent of Code 2024 - Day 10

This script contains my solution for **Advent of Code 2024, Day 10**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_10_input.txt` located in the same directory as this script.
- Example: `python DAY_10.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

# Get data
data = [[int(elem) for elem in list(row)] for row in open("day_10_input.dat").read().split('\n')]
width, height = len(data[0]), len(data)

# Recursive function to foolow every path and check wheather it reaches 9
def recurse(x, y,  distinct: bool = False, ends: set[tuple[int, int]] = None, current: int = 0) -> int:
    # Initialize set of visited ends if not done
    if ends is None and not distinct: 
        ends = set()

    # Reached end of recursion
    if current == 9: 
        # Searching for all distincct paths (2'nd star)
        if distinct: 
            return 1
        # Check whether end tile was reached before
        if (x, y) in ends: 
            return 0 
        # On a new tile add 1 to return
        ends.add((x, y))
        return 1

    # Recursively check all valid paths and count them
    return sum(recurse(new_x, new_y, distinct, ends, current + 1) 
               for new_x, new_y in [(x+1, y), (x-1, y),(x, y+1),(x, y-1)] 
               if 0 <= new_x < width and 0 <= new_y < height and data[new_y][new_x] == current + 1)

# Find trail starting points and recursively validate all possible paths
def find_trails(distinct: bool = False) -> int:
    return sum(recurse(x, y, distinct) for x in range(width) 
                                       for y in range(height) 
                                       if data[y][x] == 0)

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(find_trails())

# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print(find_trails(True))