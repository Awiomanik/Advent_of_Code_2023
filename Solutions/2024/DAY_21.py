"""
Advent of Code 2024 - Day 21

This script contains my solution for **Advent of Code 2024, Day 21**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_21_input.txt` located in the same directory as this script.
- Example: `python DAY_21.py`

## Credits:
- **Puzzle Design**: Eric Wastl (Advent of Code creator).
- **Solution Author**: Wojciech Kośnik-Kowalczuk - I developed this solution as part of my personal journey through Advent of Code.
- **Special Thanks**: To the global Advent of Code community for sharing insights and fostering a collaborative learning environment.

## Notes:
- Optimization opportunities might exist and will be revisited as time permits.
- Feel free to reach out with feedback, suggestions, or optimizations for this solution.

Happy Coding! 🎄✨
"""

from time import time
from itertools import permutations
from functools import lru_cache
import sys
from pathlib import Path
# Dynamically add the Usefull_stuff directory to sys.path
current_dir = Path(__file__).resolve().parent
usefull_stuff_dir = current_dir.parent.parent / "Usefull_stuff"
sys.path.insert(0, str(usefull_stuff_dir))
from coord import COORD

# Get data
data = open("day_21_input.dat").read().split('\n')
codes: list[list[int]] = [[int(elem) if elem.isdigit() else -1 for elem in code] for code in data]

# Util dictionaries
keypad: dict[int, COORD] = {
    -1: COORD(2, 3), # 'A'
    0: COORD(1, 3),
    1: COORD(0, 2),
    2: COORD(1, 2),
    3: COORD(2, 2),
    4: COORD(0, 1),
    5: COORD(1, 1),
    6: COORD(2, 1),
    7: COORD(0, 0),
    8: COORD(1, 0),
    9: COORD(2, 0)
}
keypad_dir: dict[str, COORD] = {
    '^': COORD(1, 0), 
    'A': COORD(2, 0),
    '<': COORD(0, 1),
    'v': COORD(1, 1),
    '>': COORD(2, 1)
}

@lru_cache(None)
def validate_path(start: COORD, steps: tuple[str], forbidden_key: COORD = COORD(0, 3)) -> bool:
    current = start
    for step in steps:
        if step == '>':
            current += COORD(1, 0)
        elif step == '<':
            current += COORD(-1, 0)
        elif step == 'v':
            current += COORD(0, 1)
        elif step == '^':
            current += COORD(0, -1)

        if current == forbidden_key:
            return False
        
    return True

# Movement around the numeric keypad
@lru_cache(maxsize=None)
def move(pos: COORD, target: COORD, directional_pad: bool = False) -> list[tuple[str]]:
    shift_x: int = target.x - pos.x
    shift_y: int = target.y - pos.y

    # Horizontal movement
    path: str = ('>' * max(0, shift_x) + '<' * max(0, -shift_x) +
                 'v' * max(0, shift_y) + '^' * max(0, -shift_y))

    # Generate all combinations
    paths = set(permutations(path))
    forbidden = COORD(0, 0) if directional_pad else COORD(0, 3)
    return [tuple(path) + ('A',) for path in paths if validate_path(pos, path, forbidden)]

def recursive_build_paths(paths, built_path=()):
    """Recursively construct paths."""
    if not paths:
        return [built_path]
    first, *rest = paths
    return [built_path + tuple(segment) for segment in first for built_path in recursive_build_paths(rest)]

all_possible_key_pairs: dict[tuple[str, str], list[tuple[str]]] = {
    (prev, foll): move(keypad_dir[prev], keypad_dir[foll], True)
    for prev, foll in permutations(['A', '^', 'v', '>', '<'], 2)
    if prev != foll
}



# < --- 1'st STAR --- >
start_time = time()
total_counter = 0
steps = 25
total = len(codes) * steps

for code_i, code in enumerate(codes):
    num_pad_output = []
    for prev, foll in zip([-1] + code, code):
        num_pad_output.append(move(keypad[prev], keypad[foll]))

    num_pad_output = recursive_build_paths(tuple(num_pad_output))
    next_out = num_pad_output

    for i in range(steps):
        print(f"{code_i * steps + i}/{total}        ", end='\r')
        next_dir_pad_output = []
        for path in next_out:
            path_segments = []
            for prev, foll in zip(['A'] + list(path), path):
                path_segments.append(move(keypad_dir[prev], keypad_dir[foll], True))
            next_dir_pad_output.extend(recursive_build_paths(tuple(path_segments)))
        shortest = min(len(out) for out in next_dir_pad_output)
        next_out = set(out for out in next_dir_pad_output if len(out) == shortest)

    shortest_sequence_len = min(len(path) for path in next_out)
    total_counter += shortest_sequence_len * int(''.join(map(str, code[:-1])))

print(f"Total Counter: {total_counter}")
print(f"Solution completed in {time() - start_time:.2f}s")


# < --- 2'nd STAR --- >
start = time()
print("\n2'nd star solution:\n")

sys.exit()
# Precompute all possble lengths
all_possible_key_pairs: dict[tuple[str, str], tuple[tuple[str]]] = {(prev, foll): () 
    for prev, foll in permutations(['A', '^', 'v', '>', '<'], 2) if prev != foll}

for prev, foll in all_possible_key_pairs:
    all_possible_key_pairs[(prev, foll)] = move(keypad_dir[prev], keypad_dir[foll], True)


# Use precomputed moves to generate path lengths 
def recurse(prev: str, foll: str, depth: int = 25):
    stack = [(path, depth) for path in all_possible_key_pairs[(prev, foll)]]
    best = sys.maxsize

    while stack:
        path, depth = stack.pop()

        if depth == 0:
            best = min(len(path), best)
            continue

        paths = all_possible_key_pairs[(prev, foll)]
        for path in paths:
            temp_path = []
            for prev, foll in zip(['A'] + list(path), path):
                temp_path.extend((path, depth - 1) for path in all_possible_key_pairs[(prev, foll)])
            print(path)
            print(depth)
            temp_path


for x in all_possible_key_pairs.items():
    print(x)



sys.exit()


counter: int = 0
for code_i, code in enumerate(codes):

    # Numeric-pad 
    num_pad_output: list[list[str]] = []
    for prev, foll in zip([-1] + code, code):
        num_pad_output.append(move(keypad[prev], keypad[foll]))
    num_pad_output = recursive_build_paths(tuple(num_pad_output))

    # First directional-pad
    next_out = num_pad_output
    for _ in range(24):
        dir_pad_output: list[list[list[str]]] = []
        for path in next_out:
            path_out: list[list[str]] = []

            for prev, foll in zip(['A'] + list(path), path):
                path_out.append(move(keypad_dir[prev], keypad_dir[foll], True))
            dir_pad_output.extend(recursive_build_paths(tuple(path_out)))
        next_out = dir_pad_output
        

    # Second directional-pad
    dir_pad_output2: list[list[list[str]]] = []
    for i, path in enumerate(dir_pad_output):
        print(f"Processing code: {code_i}/{len(codes)} ({code}) | Progress: {i}/{len(dir_pad_output)}", end='\r')
        path_out: list[list[str]] = []

        for prev, foll in zip(['A'] + list(path), path):
            path_out.append(move(keypad_dir[prev], keypad_dir[foll], True))
        dir_pad_output2.extend(recursive_build_paths(tuple(path_out)))

    shortest_sequence_len = min(len(path) for path in dir_pad_output2)

    counter += shortest_sequence_len * int(''.join(str(c) for c in code[:-1]))

print(counter, ' ' * 100)
print(f"Solution found in {time() - start:.2f}s")
