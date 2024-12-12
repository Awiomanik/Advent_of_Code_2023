"""
Advent of Code 2024 - Day 8

This script contains my solution for **Advent of Code 2024, Day 8**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_8_input.txt` located in the same directory as this script.
- Example: `python DAY_8.py`

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
data = [list(line) for line in open("day_8_input.dat").read().split('\n')]
width, height = len(data[0]), len(data)

def get_antinodes(resonant_harmonics: bool = False, printData: bool = False) -> int:
    antinodes = [[False for _ in range(width)] for _ in range(height)]

    for y, line in enumerate(data):
        for x, node in enumerate(line):
            # Found antena
            if node != '.':

                # Collect all matching tiles
                matching_tiles = [(y2, x2) for y2, line2 in enumerate(data)
                                        for x2, node2 in enumerate(line2)
                                                if node2 == node]

                # Loop through matching tiles
                for y2, x2 in matching_tiles:
                    dist_x, dist_y = x - x2, y - y2
                    
                    # Calculate potential positions
                    positions = [(y + dist_y, x + dist_x),
                                (y2 + dist_y, x2 + dist_x)]
                    
                    # Mark valid positions
                    for new_y, new_x in positions:
                        if resonant_harmonics:
                            while (0 <= new_y < height and 0 <= new_x < width):
                                antinodes[new_y][new_x] = True
                                new_y += dist_y
                                new_x += dist_x
                        
                                # Avoid infinite loop
                                if dist_x == 0 or dist_y == 0: 
                                    break
                        else:
                            if 0 <= new_y < height and \
                            0 <= new_x < width and \
                            (new_y, new_x) != (y, x) and \
                            (new_y, new_x) != (y2, x2):
                                antinodes[new_y][new_x] = True

    if printData:
        for y, line in enumerate(antinodes):
            for x, node in enumerate(line):
                print('#' if node else data[y][x], end='')
            print()
    
    # count antinodes
    return sum([sum(line) for line in antinodes])


# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(get_antinodes())


# < --- 2'nd STAR --- >
print("\n2'st star solution:\n")
print(get_antinodes(True))