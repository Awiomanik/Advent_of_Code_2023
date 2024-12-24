"""
Advent of Code 2024 - Day 15

This script contains my solution for **Advent of Code 2024, Day 15**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_15_input.txt` located in the same directory as this script.
- Example: `python DAY_15.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from copy import deepcopy
import sys
from pathlib import Path
# Dynamically add the Usefull_stuff directory to sys.path
current_dir = Path(__file__).resolve().parent
usefull_stuff_dir = current_dir.parent.parent / "Usefull_stuff"
sys.path.insert(0, str(usefull_stuff_dir))
from coord import COORD

# Get data
data: list[str] = open("day_15_input.dat").read().split('\n\n')
warehouse: dict[COORD, str] = {COORD(x, y): cell
                                for y, row in enumerate(data[0].split('\n'))
                                for x, cell in enumerate(row)}
instructions: list[str] = list(data[1].replace('\n', ''))
WIDTH = max(coord.y for coord in warehouse.keys()) + 1
HEIGHT = max(coord.x for coord in warehouse.keys()) + 1

# Movement dictionary
move: dict[str, COORD] ={
    '^': COORD(0, -1),
    '<': COORD(-1, 0),
    'v': COORD(0, 1),
    '>': COORD(1, 0)
}

def display_state(warehouse: dict[COORD, str], current_direction: str, manual: bool = True) -> None:
    # Build and print the grid row by row
    print("Current direction:", current_direction, "\n")
    for y in range(0, HEIGHT):
        print(''.join(cell if (cell:=warehouse[COORD(x, y)]) != '@' else current_direction 
                        for x in range(0, WIDTH)))
    
    # Wait for user to move on to the next cell
    if manual: input("\nPress enter to move to next frame...")


# < --- 1'st STAR --- >
print("\n1'st star solution:\n")

# Find initial robot coordinates
robot: COORD = next(coord for coord, cell in warehouse.items() if cell == '@')

# Copy the warehouse initial state to save it for 2'nd star
state: dict[COORD, str] = deepcopy(warehouse)

# Execute robot movements
for dir in instructions:

    # Display currnet state
    #os.system("cls")
    #display_state(state, dir, False)
    
    # Get next cell to check
    current_cell: COORD = robot

    # Check every cell on the way to find an empty spot
    while ((next_cell := state[current_cell]) != '#'):
        
        # Check for empty spot
        if next_cell == '.':
            # Update the map
            state[current_cell] = 'O'
            state[robot] = '.'
            state[robot + move[dir]] = '@'
            
            # Update robot position
            robot += move[dir]

            # Jump to next instruction
            break

        # Get next cell
        current_cell += move[dir]

# Sum-up all GPS coordinates of the boxes
print(sum(coord.x + coord.y * 100 for coord, cell in state.items() if cell == 'O'))


# < --- 2'nd STAR --- >
# Expand the warehouse and save as state
stateXL: dict[COORD, str] = {}
expand: dict[str, tuple[str, str]] = {
    '#': ('#', '#'),
    'O': ('[', ']'),
    '.': ('.', '.'),
    '@': ('@', '.')
}
for coord, cell in warehouse.items():
    stateXL[COORD(coord.x * 2, coord.y)], stateXL[COORD(coord.x * 2 + 1, coord.y)] = expand[cell]
WIDTH *= 2

# Find initial robot coordinates
robot: COORD = next(coord for coord, cell in stateXL.items() if cell == '@')

# Execute robots movements
for dir in instructions:
    
    # Display currnet state
    #os.system("cls")
    #display_state(stateXL, dir, False)

    # Horizontal move
    if dir in ['<', '>']:
        
        # Get next cell to check
        current_cell: COORD = robot

        # Memorize all affected cellls to push the boxes
        cells2update: dict[COORD, str] = {robot: dir}

        # Check every cell on the way to find an empty spot
        while (stateXL[current_cell] != '#'):
            
            # Check for empty spot
            if stateXL[current_cell] == '.':

                # Update the map
                for coord, cell in cells2update.items():
                    # Ommit current cell as it is empty cell (do not move it)
                    if coord == current_cell: continue
                    stateXL[coord + move[dir]] = cell
                stateXL[robot] = '.'

                # Update robot position
                robot += move[dir]

                # Jump to next instruction
                break

            # Get next cell
            current_cell += move[dir]
            cells2update[current_cell] = stateXL[current_cell]
            #print(cells2update)
    
    else: # dir in ['^', 'v']:
        # Initialize dicts of importnat cells
        cells2update: dict[COORD, str] = {robot: dir}
        first_cell2check: COORD = robot + move[dir]
        cells2check: dict[COORD, str] = {first_cell2check: stateXL[first_cell2check]}
        if stateXL[first_cell2check] in ['[', ']']:
            pair_offset = move['>'] if stateXL[first_cell2check] == '[' else move['<']
            cells2check[first_cell2check + pair_offset] = stateXL[first_cell2check + pair_offset]
            cells2update[robot + pair_offset] = '.'
        

        # Check all cells for empty spots
        while '#' not in cells2check.values():

            # Check if all blocks can be moved
            if all(cell == '.' for cell in cells2check.values()):
                
                # Update the map
                for coord, cell in cells2update.items():
                    stateXL[coord + move[dir]] = cell
                # Clear old robot position
                stateXL[robot] = '.'
                
                # Update robot position
                robot += move[dir]

                # Jump to next instruction
                break

            new_cells2check: dict[COORD, str] = {}
            for coord, cell in cells2check.items():
                if cell != '.':
                    new_coord = coord + move[dir]
                    new_cell = stateXL[new_coord]

                    # Early break before wall
                    if new_cell == '#': break

                    # Add to cells to update
                    cells2update[coord] = cell
                    if cell in ['[', ']']:
                        pair_offset = move['<'] if cell == ']' else move['>']
                        if coord + pair_offset - move[dir] not in cells2update:
                            cells2update[coord + pair_offset - move[dir]] = '.'

                    # Add to cells to check
                    new_cells2check[new_coord] = new_cell
                    if new_cell in ['[', ']']:
                        pair_offset = move['<'] if new_cell == ']' else move['>']
                        new_cells2check[new_coord + pair_offset] = stateXL[new_coord + pair_offset]

            else:
                cells2check = new_cells2check
                continue
            break

print("\n2'nd star solution:\n")
# Sum-up all GPS coordinates of the boxes
print(sum(coord.x + coord.y * 100 for coord, cell in stateXL.items() if cell == '['))