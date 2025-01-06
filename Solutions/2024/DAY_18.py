"""
Advent of Code 2024 - Day 18

This script contains my solution for **Advent of Code 2024, Day 18**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_18_input.txt` located in the same directory as this script.
- Example: `python DAY_18.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from time import time
from collections import deque
import sys
from pathlib import Path
# Dynamically add the Usefull_stuff directory to sys.path
current_dir = Path(__file__).resolve().parent
usefull_stuff_dir = current_dir.parent.parent / "Usefull_stuff"
sys.path.insert(0, str(usefull_stuff_dir))
from coord import COORD


# Get data
data = [tuple(int(x) for x in byte.split(',')) 
        for byte in open("day_18_input.dat").read().split('\n')]

# Utils
memory2simulate: int = 2 ** 10
size: COORD = COORD(71, 71)
memory_space: list[list[bool]] = [[(x, y) in data[:memory2simulate]
                                   for x in range(size.x)] 
                                   for y in range(size.y)]


# < --- 2'nd STAR --- >
start: COORD = COORD(0, 0)
end: COORD = size - 1
visited: dict[COORD, int] = {}
stack: deque = deque([(0, start)])
moves: tuple[COORD] = (COORD(0, 1), COORD(0, -1), COORD(1, 0), COORD(-1, 0))
steps: int = sys.maxsize

# Breath-first search
while stack:
    # Unpack the stack element
    cost, pos = stack.popleft()

    # Prunning
    if cost > steps:
        continue

    # Reached the end
    if pos == end:
        steps = min(cost, steps)
        continue

    # Explore 
    cost += 1
    for coord in moves:
        temp: COORD = coord + pos

        if temp.inside(size) and \
            ((temp not in visited) or visited[temp] > cost) and \
            not memory_space[temp.y][temp.x]:
            stack.append((cost, temp))
            visited[temp] = cost

print("\n1'st star solution:\n")
print(steps)


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print("Computing...", end='\r')
found_path = False
while True:
    visited: dict[COORD, int] = {}
    stack: deque = deque([(0, start)])

    # Corrupt further
    current_byte: tuple = data[memory2simulate]
    memory_space[current_byte[1]][current_byte[0]] = True
    memory2simulate += 1
    
    found_path: bool = False

    # Breath-first search
    while stack:
        # Unpack the stack element
        cost, pos = stack.popleft()

        # Reached the end
        if pos == end:
            found_path = True
            break

        # Explore 
        cost += 1
        for coord in moves:
            temp: COORD = coord + pos

            if temp.inside(size) and \
                not memory_space[temp.y][temp.x] and \
                ((temp not in visited) or visited[temp] > cost):
                stack.append((cost, temp))
                visited[temp] = cost

    if not found_path:
        break

print("               ", end='\r')
print(str(current_byte).replace(' ', '').replace('(', '').replace(')', ''))