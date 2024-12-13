"""
Advent of Code 2024 - Day 9

This script contains my solution for **Advent of Code 2024, Day 9**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_9_input.txt` located in the same directory as this script.
- Example: `python DAY_9.py`

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
data = open("day_9_input.dat").read()

# Creating disk from map
def create_disk() -> list[int]:
    disk: list[int] = []
    fileNum: int = 0
    file: bool = True
    
    for indicator in data:
        for _ in range(int(indicator)):
            if file:
                disk.append(fileNum)
            else:
                disk.append(None)
        if file:
            fileNum += 1
        file = not file

    return disk

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")

# Create a disk
disk: list[int] = create_disk()

index: int = len(disk) - 1
empty: int = 0

while index > empty:
    # Find first empty spot
    while disk[empty] is not None: empty += 1

    # Find last not empty spot
    while disk[index] is None: index -= 1

    # Get last element and put it in the first empty spot
    last = disk[index]
    disk[empty] = last

    # Decrement index
    index -= 1

print(sum(i*elem for i, elem in enumerate(disk[:index + 1])))


# < --- 2'nd STAR --- >
def move_block(i: int, blockLen: int, last_i: int) -> None:
    for j in range(i, i + blockLen):
        disk[j] = last
    for j in range(last_i, last_i + blockLen):
        disk[j] = None

print("\n2'nd star solution:\n")

# Create a disk
disk = create_disk()

# Get empty regions
empty_regions: list[int, int] = []
whether_empty: bool = False
current_index: int = 0

for indicator in data:
    indicator = int(indicator)
    if whether_empty: 
        empty_regions.append((current_index, indicator))

    current_index += indicator
    whether_empty = not whether_empty

# Defragment the disk
index: int = len(disk) - 1
while index >= 0:
    #print(' '.join('.' if i is None else str(i) for i in disk))

    # Find last not empty spot
    while disk[index] is None: index -= 1
    last = disk[index] 
    lastIndex = index-1   
    while disk[lastIndex] == last:
        lastIndex -= 1
    lastIndex += 1
    lastLen = index - lastIndex + 1

    for empty_i, (i, gap) in enumerate(empty_regions):
        if i < index:
            if gap == lastLen:
                # Mark gap as filled
                empty_regions.pop(empty_i)
                move_block(i, lastLen, lastIndex)
                break

            elif gap > lastLen:
                # Limit the gap
                empty_regions[empty_i] = (i + lastLen, gap - lastLen)
                move_block(i, lastLen, lastIndex)
                break
        else:
            break

    index -= lastLen

result: int = sum(i*elem for i, elem in enumerate(disk) if elem)
print(result, "        ")
