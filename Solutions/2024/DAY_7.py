"""
Advent of Code 2024 - Day 7

This script contains my solution for **Advent of Code 2024, Day 7**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_7_input.txt` located in the same directory as this script.
- Example: `python DAY_7.py`

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
data = [(int((temp:=d.split(': '))[0]), [int(x) for x in temp[1].split()]) for d in open("day_7_input.dat").read().split('\n')]

# Recursive function to test all permutations of operations
def recurse(target: int, components: list[int], result: int, concatanate: bool=False, index: int=0) -> bool:
    return result == target if len(components) == index else \
                (recurse(target, components, result * components[index], concatanate, index+1) or \
                recurse(target, components, result + components[index],  concatanate, index+1) or \
                (concatanate and recurse(target, components, int(str(result) + str(components[index])), concatanate, index+1)) \
                    if result <= target else False)

# < --- 1'st STAR --- >        
print("\n1'st star solution:\n")
print(sum(result for result, nums in data if recurse(result, nums[1:], nums[0])))

# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print(sum(result for result, nums in [(result, nums) for result, nums in data if not recurse(result, nums[1:], nums[0])] if recurse(result, nums[1:], nums[0], True)))