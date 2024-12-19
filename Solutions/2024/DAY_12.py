"""
Advent of Code 2024 - Day 12

This script contains my solution for **Advent of Code 2024, Day 12**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_12_input.txt` located in the same directory as this script.
- Example: `python DAY_12.py`

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
data = [list(row) for row in open("day_12_input.dat").read().split('\n')]
WIDTH: int = len(data[0])
HEIGHT: int = len(data)

# Separates regions of plants the same type
def devide(specie: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    specie: set[tuple[int, int]] = set(specie)
    regions: list[list[tuple[int, int]]] = []
    
    def dfs(start: tuple[int, int], current_region: list[tuple[int, int]]):
        """Depth-First Search to find all connected plots."""
        stack = [start]

        while stack:
            x, y = stack.pop()

            if (x, y) not in specie:
                continue

            specie.remove((x, y))
            current_region.append((x, y))

            # Check all possible neighbours
            stack.extend([(x + dx, y + dy) 
                          for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] 
                          if (x + dx, y + dy) in specie])
    
    # Populate regions
    while specie:
        current_region = []
        dfs(next(iter(specie)), current_region)
        regions.append(current_region)

    return regions

# Split data into separete regions
def split() -> list[list[tuple[int, int]]]:
    species: set[str] = {plot for row in data for plot in row}
    species_regions: dict[str, list[tuple[int, int]]] = {specie: [] for specie in species}
    all_regions: list[list[tuple[int, int]]] = []

    for specie in species:
        for i, row in enumerate(data):
            for j, plot in enumerate(row):
                if specie == plot:
                    species_regions[specie].append((j, i))

        # Split specie into regions using depth-first search
        all_regions.extend(devide(species_regions[specie]))

    return all_regions

# < --- 1'st STAR --- >
print("\n1'st star solution:\n")

# Get data splitted into regions
regions: list[list[tuple[int, int]]] = split()

# Count the price per region (perimeter * area)
# Perimeter is calculated by taking every plot and summing it's empty neighbours
total_priece: int = 0
for region in regions:                           
    total_priece += sum(sum(1 
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if (nx:=x+dx) < 0 
                        or (ny:=y+dy) < 0 
                        or nx >= WIDTH 
                        or ny >= HEIGHT 
                        or (nx, ny) not in region) for x, y in region) \
                            * len(region)

print(total_priece)


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
# This one was tricky, sorry for such convoluted code 🤷‍♂️

# Here after some doodling,
# I realized that the fances must be even,
# There is the same amount of horizontal and vertical ones
counter = 0
for region in regions:  
    top: list[tuple[int, int]] = [(x, y) for x, y in region 
                                  if (ny:=y+1) >= HEIGHT or (x, ny) not in region]
    bot: list[tuple[int, int]] = [(x, y) for x, y in region 
                                  if (ny:=y-1) < 0 or (x, ny) not in region]

    sub_counter = 0
    for edges in [top, bot]:
        for row in range(HEIGHT):
            # Get all edges from this in this row and sort them from left to right
            row_edges = sorted([x for x, y in edges if y == row])

            # Go from left to right and check if there are gaps
            sub_sub_counter = 1 if row_edges and row_edges[0] == 0 else 0
            x_prev = -1
            for x in row_edges:
                if x - x_prev != 1: 
                    sub_sub_counter += 1
                x_prev = x

            sub_counter += sub_sub_counter
    
    counter += sub_counter * len(region)

print(counter * 2)