"""
Advent of Code 2024 - Day 19

This script contains my solution for **Advent of Code 2024, Day 19**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_19_input.txt` located in the same directory as this script.
- Example: `python DAY_19.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from functools import lru_cache

# Get data
data = open("day_19_input.dat").read().split('\n\n')
towels: list[str] = data[0].split(', ')
patterns: list[str] = data[1].split('\n')

# Helper recursive function
@lru_cache(None)
def recurse(pattern: str, count: bool = False):
    if not pattern:
        return True
    
    counter = 0
    for towel in towels:
        if pattern.startswith(towel):
            counter += (temp:=recurse(pattern[len(towel):], count))
            if not count and  temp > 0: 
                return True
            
    return counter if count else False


# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(sum(recurse(pattern) for pattern in patterns))


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print(sum(recurse(pattern, True) for pattern in patterns))