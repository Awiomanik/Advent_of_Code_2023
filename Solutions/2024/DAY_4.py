"""
Advent of Code 2024 - Day 4

This script contains my solution for **Advent of Code 2024, Day 4**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_4_input.txt` located in the same directory as this script.
- Example: `python DAY_4.py`

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
# [list(row) for row in zip(*data[::-1])] rotates data 90 deg clock-wise
print((lambda data, checkForXMASs: (lambda length: sum(checkForXMASs(list(line)) for line in data)+sum(checkForXMASs(line) for line in [list(row) for row in zip(*data[::-1])])+sum(checkForXMASs(s) for s in [[data[y+i][x+i] for i in range(length) if y+i<len(data) and x+i<len(data[0])] for x, y in list(set([(x,0) for x in range(len(data))]+[(0,y) for y in range(1,len(data[0]))]))])+sum(checkForXMASs(s) for s in [[data[y-i][x+i] for i in range(length) if y-i>=0 and y-i<len(data) and x+i<len(data[0])] for x, y in list(set([(x, len(data) - 1) for x in range(len(data))]+[(0, y) for y in range(len(data[0]))]))]))(len(data) if len(data) > len(data[0]) else len(data[0])))(open("day_4_input.dat").read().split('\n'),(lambda listOfChars: sum(int(listOfChars[i:i+4]==(xmas:=list("XMAS")))+int(listOfChars[-i:-i-4:-1]==xmas) for i in range(len(listOfChars))))))

# 2'nd STAR
print((lambda data: sum(1 for y in range(1,len(data)-1) for x in range(1,len(data[0])-1) if (data[y][x]=='A' and ((data[y-1][x-1]=='M' and data[y+1][x+1]=='S') or (data[y-1][x-1]=='S' and data[y+1][x+1]=='M')) and ((data[y-1][x+1]=='M' and data[y+1][x-1]=='S') or (data[y+1][x-1]=='M' and data[y-1][x+1]=='S')))))([list(line) for line in open("day_4_input.dat").read().split('\n')]))
