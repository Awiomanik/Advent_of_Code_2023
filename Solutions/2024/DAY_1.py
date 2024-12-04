"""
Advent of Code 2024 - Day 1

This script contains my solution for **Advent of Code 2024, Day 1**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_1_input.txt` located in the same directory as this script.
- Example: `python DAY_1.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

# NOTE:
# This one-liner is part of a fun challenge I have with friends to solve Advent of Code puzzles
# compactly in a single command in the console. It prioritizes brevity and creativity over clarity or readability.
#
# If you're looking to understand the logic, consider breaking it down step-by-step.
# For more details on the puzzles, visit https://adventofcode.com.
#
# I don’t expect to complete the entire calendar this way, as maintaining one-liners for every puzzle
# might become impractical. If you're looking for more readable solutions, check out later days
# or solutions from previous years—they're probably far easier to understand. For now, though,
# the goal is to push the limits with one-liners for as long as it makes sense.
#
# USAGE:
# >> python -c "one-liner-here"
# (Note: Remember to escape double quotes [ " -> \" ] when passing strings in the console.)

# 1st STAR
print(sum([abs(x-y) for x,y in zip(*[sorted(column) for column in list(map(list,(zip(*[map(int,line.split()) for line in open("day_1_input.dat")]))))])]))

# 2nd STAR
print((lambda columns:sum([element_left_col*sum([1 if element_right_col==element_left_col else 0 for element_right_col in columns[1]]) for element_left_col in columns[0]]))(list(map(list,(zip(*[map(int,line.split()) for line in open("day_1_input.dat")]))))))
