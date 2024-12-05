"""
Advent of Code 2024 - Day 2

This script contains my solution for **Advent of Code 2024, Day 2**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_2_input.txt` located in the same directory as this script.
- Example: `python DAY_2.py`

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

# 1'st STAR
print(sum([any(inner) for inner in [[all(inner_inner_list) for inner_inner_list in zip(*inner_list)] for inner_list in [[[not (element-level[i+1]<=0 or element-level[i+1]>3 or element<level[i+1]), not (level[i+1]-element<=0 or level[i+1]-element>3 or element>level[i+1])] for i, element in enumerate(level[:-1])] for level in [list(map(int, line.split())) for line in open("day_2_input.dat")]]]]))

# 2'nd STAR
print(sum([temp if (temp:=any([(lambda level: all(0<level[i+1]-level[i]<=3 for i in range(len(level)-1)) or all(0<level[i]-level[i+1]<=3 for i in range(len(level)-1)))(level[:i]+level[i+1:]) for i in range(len(level))])) else all(0<level[i+1]-level[i]<=3 for i in range(len(level)-1)) or all(0<level[i]-level[i+1]<=3 for i in range(len(level)-1)) for level in [list(map(int, line.split())) for line in open("day_2_input.dat")]]))
