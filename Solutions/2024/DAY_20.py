"""
Advent of Code 2024 - Day 20

This script contains my solution for **Advent of Code 2024, Day 20**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_20_input.txt` located in the same directory as this script.
- Example: `python DAY_20.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

import sys
from pathlib import Path
# Dynamically add the Usefull_stuff directory to sys.path
current_dir = Path(__file__).resolve().parent
usefull_stuff_dir = current_dir.parent.parent / "Usefull_stuff"
sys.path.insert(0, str(usefull_stuff_dir))
from coord import COORD


# Get data
data = open("day_20_input.dat").read().split('\n')

racetrack: list[list[bool]] = [[not char == '#' for char in line] for line in data]
width: int = len(racetrack[0])
height: int = len(racetrack)
size: int = width * height
start: COORD = COORD(next((row.index('S'), y) for y, row in enumerate(data) if 'S' in row))
end: COORD = COORD(next((row.index('E'), y) for y, row in enumerate(data) if 'E' in row))

moves: tuple[COORD] = (COORD(0, 1), COORD(0, -1), COORD(1, 0), COORD(-1, 0))
cheats20: tuple[COORD] = tuple(COORD(dx, dy) 
                                for dy in range(-20, 21) 
                                for dx in range(-20, 21) 
                                    if 0 < abs(dx) + abs(dy) <= 20)

def dfs(start: COORD):

    # Stack to store the state for iteration
    stack = [(start, [start])]
    visited = set()  # Use a set for O(1) membership checks

    while stack:
        pos, path = stack.pop()

        # Break condition
        if pos == end:
            return path

        # Mark current position as visited
        visited.add(pos)

        # Explore moves
        for move in moves:
            new_pos = pos + move

            # Check if the new position is valid and not visited
            if new_pos not in visited and racetrack[new_pos.y][new_pos.x]:
                stack.append((new_pos, path + [new_pos]))

    return None

def cheat(huge_jump = False, debug: bool = False, threshold: int = 100):
    # Get path without shortcuts
    dfs_path = dfs(start)
    path: dict[COORD, int] = {coord: i for i, coord in enumerate(dfs_path)}
    old_time = len(dfs_path)
    
    # Debugging log
    if debug:
        print("Initial Path")
        for y1 in range(height):
            for x1 in range(width):
                print('O' if COORD(x1, y1) in path else data[y1][x1], end='')
            print()  # New line at the end of each row
        print(f"Path Length: {old_time}")
        print(f"Path Coordinates: {list(path.keys())}")
        print("-" * (width + 10))
        input("Press Enter to continue...")

    # Collect cheats into dictionary
    cheat_groups = {}
    for pos, start_index in path.items():
        if not huge_jump:
            for move in moves:
                next_pos = pos + move

                # Move through walls
                if next_pos not in path:
                    for move2 in moves:
                        cheat_step = next_pos + move2

                        # Found a move that gets back on path
                        if cheat_step != pos and cheat_step in path:
                            end_index = path[cheat_step]

                            # Get the time with shortcut
                            new_time = start_index + 2 + (old_time - end_index)

                            # Add time to the dictionary of shortcuts if it meets the threshold
                            if new_time <= old_time - threshold:
                                cheat_groups[old_time - new_time] = \
                                    cheat_groups.get(old_time - new_time, 0) + 1

                                # Debug log
                                if debug:
                                    connected_path = (
                                        dfs_path[:start_index + 1] +
                                        [pos, next_pos, cheat_step] +
                                        dfs_path[end_index:]
                                    )
                                    print(f"Trying cheat from {pos} via {next_pos} to {cheat_step}")
                                    for y1 in range(height):
                                        for x1 in range(width):
                                            coord = COORD(x1, y1)
                                            if coord in connected_path:
                                                char = (
                                                    'X' if coord in [pos, next_pos, cheat_step]
                                                    else str(connected_path.index(coord) % 10)
                                                )
                                            else:
                                                char = str(data[y1][x1])
                                            print(char, end='')
                                        print()
                                    print(f"New Time: {new_time}, Old Time: {old_time}")
                                    input("Press Enter to continue...")

        else:
            for jump in list(cheats20):
                cheat_step = pos + jump

                if 0 <= cheat_step.x < width:
                    if 0 <= cheat_step.y < height:
                        if cheat_step in path:
                            end_index = path[cheat_step]

                            # Compute time with shortcut
                            new_time = start_index + abs(jump.x) + abs(jump.y) + (old_time - end_index)                            
                        
                            # Check if the shortcut meets the threshold
                            if new_time <= old_time - threshold:
                                cheat_groups[old_time - new_time] = \
                                    cheat_groups.get(old_time - new_time, 0) + 1

                                # Debug log
                                if debug:
                                    print("\n--- Debugging Cheat Attempt ---")
                                    print(f"Starting Position: {pos}")
                                    print(f"Jump Vector: {jump}")
                                    print(f"Cheat Step: {cheat_step}")
                                    print(f"Start Index: {start_index}, End Index: {end_index}")
                                    print(f"New Time: {new_time}, Old Time: {old_time}")
                                    print(f"Time saved: {old_time - new_time}")
                                    print(f"Threshold for saving: {threshold} picoseconds")
                                    
                                    # Visualize the connected path
                                    connected_path = (
                                        dfs_path[:start_index + 1] +
                                        [pos, cheat_step] +
                                        dfs_path[end_index:]
                                    )
                                    print("\nGrid Visualization:")
                                    for y1 in range(height):
                                        for x1 in range(width):
                                            coord = COORD(x1, y1)
                                            if coord in connected_path:
                                                char = (
                                                    'X' if coord in [pos, cheat_step]
                                                    else str(connected_path.index(coord) % 10)
                                                )
                                            else:
                                                char = str(data[y1][x1])
                                            print(char, end='')
                                        print()
                                    
                                    print(f"Cheat saved {old_time - new_time} picoseconds.")
                                    input("Press Enter to continue...")
                                    print()

    # Count shortcuts
    counter = sum(cheat_groups.values())

    # Debug log
    if debug:
        print("\nCheat Summary:")
        for elem in sorted(cheat_groups.items()):
            print(f"There are {elem[1]} cheats that save {elem[0]} picoseconds.")

    return counter


# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(cheat())


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print(cheat(True))
