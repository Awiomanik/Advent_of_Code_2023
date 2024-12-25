"""
Advent of Code 2024 - Day 16

This script contains my solution for **Advent of Code 2024, Day 16**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_16_input.txt` located in the same directory as this script.
- Example: `python DAY_16.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

import os

# Get data
data = [list(x) for x in open("day_16_input.dat").read().split('\n')]
maze: list[list[bool]] = [[tile in ['.', 'S', 'E'] for tile in row] for row in data]
pos: tuple[int, int] = next(((int(j), int(i)) for i, row in enumerate(data) for j, value in enumerate(row) if value == 'S'))
end: tuple[int, int] = next(((int(j), int(i)) for i, row in enumerate(data) for j, value in enumerate(row) if value == 'E'))
face: str = 'E'

clockwise: dict[str, str] = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
anti_clockwise: dict[str, str] = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}

move: dict[str, tuple[int, int]] = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

def display_maze_state(maze, pos, visited) -> None:
    """
    Prints the current state of the maze with the current position and visited cells.

    Parameters:
    - maze: List of lists representing the maze structure.
    - pos: Tuple (x, y) representing the current position in the maze.
    - visited: Set of tuples representing visited positions in the maze.
    """
    # Create a deep copy of the maze to modify for display
    display_maze = [[' ' if tile else '#' for tile in row] for row in maze]

    os.system("cls")
    print(pos, end)
    print(len(visited))
    # Mark visited cells
    for x, y in visited:
        if display_maze[y][x] == ' ':
            display_maze[y][x] = 'X'  # V for Visited

    # Mark the current position
    x, y = pos
    display_maze[y][x] = 'O'  # P for Player/Current Position

    # Print the maze
    for row in display_maze:
        print(''.join(row))
    print()  # Add a newline for better readability

def dfs(pos: tuple[int, int], face: str) -> tuple[int, int]:

    # Initialize utils
    visited: dict[tuple[tuple[int, int], str], int] = {}
    stack: list[tuple[tuple[int, int], str, int, bool, list[int, int]]] = \
        [(pos, face, 0, False, [pos])]
    best = float('inf')

    while stack:
        curr_pos, curr_face, curr_score, rotated, curr_path = stack.pop()
        #display_maze_state(maze, curr_pos, visited.keys())

        # Prunning
        if curr_score > best: 
            continue

        # More prunning
        if (curr_pos, curr_face) in visited and \
            visited[(curr_pos, curr_face)] < curr_score:
            continue

        # Reached the end
        if curr_pos == end:
            if curr_score < best:
                best = curr_score
                best_paths = [curr_path]
            elif curr_score == best:
                best_paths.append(curr_path)
            continue

        # Mark pos as visited
        visited[(curr_pos, curr_face)] = curr_score

        # Move
        x = curr_pos[0] + move[curr_face][0]
        y = curr_pos[1] + move[curr_face][1]

        if maze[y][x]:
            stack.append(((x, y), curr_face, curr_score + 1, False, curr_path + [(x, y)]))
        if not rotated:
            stack.append((curr_pos, clockwise[curr_face], curr_score + 1000, True, curr_path))
            stack.append((curr_pos, anti_clockwise[curr_face], curr_score + 1000, True, curr_path))

    # Extract all unique positions visited in the best paths
    unique_positions = set()
    for path in best_paths:
        unique_positions.update(path)

    return len(unique_positions), best
    

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print("Computing...", end='\r')
star2, star1 = dfs(pos, face)
print(" " * 15 + '\b' * 15 + str(star1))


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
print(star2)