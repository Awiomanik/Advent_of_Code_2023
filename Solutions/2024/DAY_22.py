"""
Advent of Code 2024 - Day 22

This script contains my solution for **Advent of Code 2024, Day 22**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_22_input.txt` located in the same directory as this script.
- Example: `python DAY_22.py`

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
data = [int(price) for price in open("day_22_input.dat").read().split('\n')]

def next_secret_number(secret_num: int) -> int:
    step1: int = (secret_num << 6 ^ secret_num) & 16777215
    step2: int = (step1 ^ step1 >> 5) & 16777215
    return (step2 ^ step2 << 11) & 16777215

def day(num: int) -> int:
    for _ in range(2000):
        num = next_secret_number(num)
    return num

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(sum([day(price) for price in data]))

# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print("Computing...", end='\r')

bananas_per_sequence: dict[list[int], int] = {}
for seed in data:
    num: int = seed
    diffs: list[int] = []
    buyers_diffs_seen: set[list[int]] = set()

    for i in range(2000):
        new_num: int = next_secret_number(num)
        diffs.append((new_num % 10) - (num % 10))

        if i > 2: # off-by-one on top of off-by-one (god, it took me definitely too long!)
            sequence: tuple[int, int, int, int] = tuple(diffs[-4:])

            if sequence not in buyers_diffs_seen:
                if sequence not in bananas_per_sequence:
                    bananas_per_sequence[sequence] = [new_num % 10]
                else:
                    bananas_per_sequence[sequence].append(new_num % 10)

            buyers_diffs_seen.add(sequence)

        num = new_num

print(sum(max(bananas_per_sequence.items(), key = lambda val: sum(val[1]))[1]), ' ' * 13)

# > 1793