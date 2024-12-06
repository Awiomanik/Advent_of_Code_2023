"""
Advent of Code 2024 - Day 3

This script contains my solution for **Advent of Code 2024, Day 3**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_3_input.txt` located in the same directory as this script.
- Example: `python DAY_3.py`

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

# 1'nd STAR
print(sum([int(mul6[0]) * int(mul6[1]) for mul6 in [ mul5 for mul5 in [mul4 for mul4 in [mul3.split(',') for mul3 in [mul.split(')')[0] for mul in open("day_3_input.dat").read().split("mul(")] if mul3[0].isdigit() and mul3[-1].isdigit() and len(mul3)>=3 and len(mul3)<=7] if len(mul4)==2] if mul5[0].isdigit() and mul5[1].isdigit()]]))

# 2'nd STAR
print(sum([int(mul6[0]) * int(mul6[1]) for mul6 in [ mul5 for mul5 in [mul4 for mul4 in [mul3.split(',') for mul3 in [mul2.split(')')[0] for mul2 in ' '.join([mul if i==0 else mul.split("do()")[1] if len(mul.split("do()"))==2 else ' '.join(mul.split("do()")[1:]) for i, mul in enumerate(open("day_3_input.dat").read().split("don't()"))]).split("mul(")] if mul3[0].isdigit() and mul3[-1].isdigit() and len(mul3)>=3 and len(mul3)<=7] if len(mul4)==2] if mul5[0].isdigit() and mul5[1].isdigit()]]))
