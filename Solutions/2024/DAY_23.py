"""
Advent of Code 2024 - Day 23

This script contains my solution for **Advent of Code 2024, Day 23**. 
Advent of Code is an annual set of programming puzzles created by Eric Wastl, designed to challenge problem-solving skills and programming techniques. 
You can find more information about Advent of Code here: https://adventofcode.com

## Usage:
- Run the script with a standard Python interpreter.
- Input data should be provided in the form of a text file named `day_23_input.txt` located in the same directory as this script.
- Example: `python DAY_23.py`

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
from itertools import combinations

# Get data
data = open("day_23_input.dat").read().split('\n')
connections: list[tuple[str, str]] = [(connection.split('-')[0], connection.split('-')[1]) 
                                      for connection in data]
connections += [(com1, com2) for com2, com1 in connections]
connection_graph: dict[str, set[str]] = {com: {com2 for com1, com2 in connections if com1 == com} 
                                         for com, _ in connections}


# < --- 1'st STAR --- >
print("\n1'st star solution:\n")
print(len([comb for comb in combinations({node for node in connection_graph if node.startswith('t') or
                  any(neighbor.startswith('t') for neighbor in connection_graph[node])}, 3) 
           if comb[0] in connection_graph[comb[2]] 
           and comb[2] in connection_graph[comb[1]] 
           and comb[1] in connection_graph[comb[0]] 
           and any(node.startswith('t') for node in comb)]))


# < --- 2'nd STAR --- >
print("\n2'nd star solution:\n")
def bron_kerbosh_algorythm(current_clicque: set[str],
                           potential_nodes: set[str],
                           processed_nodes: set[str],
                           cliques: list[set[str]]):
    
    if not potential_nodes and not processed_nodes:
        if any(node.startswith('t') for node in current_clicque) or True:
            cliques.append(current_clicque)
        return

    for node in list(potential_nodes):
        neighbours = connection_graph[node]
        bron_kerbosh_algorythm(current_clicque | {node}, 
                               potential_nodes & neighbours, 
                               processed_nodes & neighbours,
                               cliques)
        potential_nodes.remove(node)
        processed_nodes.add(node)

cliques: list = []
bron_kerbosh_algorythm(set(), set(connection_graph.keys()), set(), cliques)

print(','.join(sorted(sorted(cliques, key=len)[-1])))
