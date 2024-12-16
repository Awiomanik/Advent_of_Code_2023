"""
Advent of Code 2024 - Day 11

This script contains my solution for **Advent of Code 2024, Day 11**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_11_input.txt` located in the same directory as this script.
- Example: `python DAY_11.py`

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
data = {int(x): 1 for x in open("day_11_input.dat").read().split()}

def blink(stones: dict[int, int], number_of_times: int = 25) -> int:
    for _ in range(number_of_times):
        new_stones = {}
        for stone, counter in stones.items():
            if stone == 0:
                if 1 in new_stones: new_stones[1] += counter
                else:               new_stones[1]  = counter

            elif (temp2 := len(temp := str(stone))) % 2 == 0:
                first = int(temp[:temp2 // 2])
                second = int(temp[temp2 // 2:])

                if first in new_stones: new_stones[first] += counter
                else:                   new_stones[first]  = counter

                if second in new_stones: new_stones[second] += counter
                else:                    new_stones[second]  = counter
            else:
                new = stone * 2024
                if new in new_stones: new_stones[new] += counter
                else:                 new_stones[new]  = counter

        stones = new_stones

    return sum(counter for counter in stones.values())
    

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(blink(data))


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print(blink(data, 75))