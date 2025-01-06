"""
Advent of Code 2024 - Day 25

This script contains my solution for **Advent of Code 2024, Day 25**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_25_input.txt` located in the same directory as this script.
- Example: `python DAY_25.py`

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

# Get data
data = open("day_25_input.dat").read().split('\n\n')
keys_ = [elem.split('\n') for elem in data if elem.split('\n')[0] == '.' * 5]
locks_ = [elem.split('\n') for elem in data if elem.split('\n')[0] == '#' * 5]
keys: list[tuple[int]] = []
for key in keys_:
    temp_key = [0, 0, 0, 0, 0]
    for row in key:
        for i, column in enumerate(row):
            if column == '#':
                temp_key[i] += 1
    keys.append(tuple(temp_key))
locks: list[tuple[int]] = []
for lock in locks_:
    temp_lock = [0, 0, 0, 0, 0]
    for row in lock:
        for i, column in enumerate(row):
            if column == '#':
                temp_lock[i] += 1
    locks.append(tuple(temp_lock))


# < --- 1'st STAR --- >
start = time()

counter: int = 0
for lock in locks:
    for key in keys:
        combined: tuple[int] = tuple(map(sum, zip(lock, key)))

        if all([x <= 7 for x in combined]):
            counter += 1



print("\n1'st star solution:\n")
print(counter)
print(f"Solution found in {time() - start:.2f}s")