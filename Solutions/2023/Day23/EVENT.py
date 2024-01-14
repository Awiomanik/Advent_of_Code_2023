# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 23


# IMPORTS
import numpy as np
from copy import deepcopy
import sys
import time as tm
from functools import lru_cache


# CONSTANTS
DATA = np.array([[t for t in line] for line in open("DATA.txt", 'r').read().split('\n')])
WIDTH, HEIGHT = DATA.shape
START, END = (1, 0), (WIDTH - 2, HEIGHT - 1)
DIRECTIONS = {"right": (0, 1), "left": (0, -1), "down": (-1, 0), "up": (1, 0)}
ARROWS = {">": "left", "<": "right", "v": "up", "^": "down"}


# increase recursion limit for part 2
sys.setrecursionlimit(10000)


# PART 1
def print_map(MAP, visited=None, info=None, coursor_down=False, tempo=0):
    '''Displaying the map for testing purposes.'''

    # additional informations
    if info: print(info)

    # precoution
    if visited is None: visited = set()

    # display map
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if (x, y) in visited:
                print('O', end='')
            else:
                print(tile, end='')
        print()

    # get back to the beginning of the map
    if not coursor_down:
        print("\033[F" * HEIGHT, end='')
        if info: print("\033[F", end='')

    # wait
    tm.sleep(tempo)

def get_valid_neighbours(POS, PREVIOUS_POS, VISITED):
    '''Returns a list of valid neighbours of a given position.'''

    # check for valid neighbours
    x, y = POS
    valid = []
    for (p, q) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:

        # check validity
        if 0 <= p < WIDTH and 0 <= q < HEIGHT \
        and DATA[q, p] != '#' \
        and (p, q) != PREVIOUS_POS \
        and (p, q) not in VISITED:
            
            # check for slope
            tile = DATA[q, p] 
            direction = get_direction((p, q), POS)
            if tile in ARROWS:
                #print("arrow, arrow[tile], direction:",tile, ARROWS[tile], direction)
                #input()
                if not ARROWS[tile] == direction:
                    valid.append((p, q))
            else:
                valid.append((p, q))

    return valid

@lru_cache(maxsize=None)
def get_direction(POS, PREVIOUS_POS):
    '''Returns the direction of the next step.'''
    
    # default direction
    if not PREVIOUS_POS or not POS: return 'down'

    # unpack tuples
    x, y = POS
    px, py = PREVIOUS_POS

    # return direction
    if x > px: return 'right'
    elif x < px: return 'left'
    elif y > py: return 'down'
    elif y < py: return 'up'

def test_walk_recursive(tempo=0, current_pos=START, previous_pos=START, \
                        current_steps=0, visited=None, current_longest_path=None):
    '''Returns the longest path in a map recursively with visualization option for testing purposes.'''

    # initialize visited and current_longest_path
    if visited is None:
        visited = set()
        current_longest_path = []
    
    # display process
    print_map(DATA, visited, \
    f"current_pos: {current_pos},\tprevious_pos: {previous_pos},\
    \tcurrent_steps: {current_steps}", tempo=tempo)

    # add current position to visited and current_longest_path
    visited.add(current_pos)
    current_longest_path.append(current_pos)

    # get valid neighbours
    valid_neighbours = list(get_valid_neighbours(current_pos, previous_pos, visited))

    # if there are no valid neighbours, return
    if len(valid_neighbours) == 0:
        if current_pos == END:
            # return current steps count and path if reached the end
            return current_steps, current_longest_path  
        else:
            # return None values if reached a dead end
            return None, None  
    
    # walk to the next position
    max_steps = current_steps
    longest_path = current_longest_path
    straight_path = []


    # path splits we need recursion
    for neighbour in valid_neighbours:

        # get the number of steps from the recursive call
        steps_temp, new_path = test_walk_recursive(tempo, neighbour, current_pos, current_steps+1, \
                                                   deepcopy(visited), deepcopy(current_longest_path))

        # continue if no valid path to the end was found
        if steps_temp is None: continue

        # update max_steps and longest_path if steps_temp is greater
        if steps_temp > max_steps:
            max_steps = steps_temp
            longest_path = new_path

    # remove straight path from visited and current_longest_path
    for node in straight_path:
        visited.remove(node)
        current_longest_path.remove(node)

    # return None, None if no valid path to the end was found
    if max_steps == current_steps:
        return None, None

    return max_steps, longest_path  

def walk_recursive(current_pos=START, previous_pos=START, \
                   current_steps=0, visited=None):
    '''Returns the longest path in a map recursively.'''

    # initialize visited
    visited = visited or set()

    # get valid neighbours
    valid_neighbours = get_valid_neighbours(current_pos, previous_pos, visited)

    # if there are no valid neighbours, return
    if not valid_neighbours:
        return current_steps if current_pos == END else None
    
    # add current position to visited
    visited.add(current_pos)
    
    # walk to the next position
    max_steps = current_steps  # initialize max_steps with current_steps

    # straight path
    while len(valid_neighbours) == 1:
        # update positions, visited, steps and valid neighbours
        previous_pos, current_pos = current_pos, valid_neighbours[0]
        visited.add(current_pos)
        current_steps += 1
        valid_neighbours = get_valid_neighbours(current_pos, previous_pos, visited)
        # if reached the end
        if current_pos == END: return current_steps

    # path splits we need recursion
    for neighbour in valid_neighbours:

        # get the number of steps from the recursive call
        steps_temp = walk_recursive(neighbour, current_pos, current_steps+1, visited.copy())

        # update max_steps and longest_path if steps_temp is greater
        max_steps = max(max_steps, steps_temp) if steps_temp else max_steps

    return max_steps


# PART 2
def get_graph():
    '''Returns a graph of an input data.'''

    # initialize variables
    nodes = {}
    start_node, end_node = (1, 0), (WIDTH - 2, HEIGHT - 1)

    # iterate over the map
    for y, row in enumerate(DATA):
        for x, tile in enumerate(row):
            # skip walls
            if tile == '#':
                continue

            # path found, add it to the graph
            current_node = (x, y)
            neighbors = []

            # check for valid neighbors
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and DATA[ny][nx] != '#':
                    neighbor_node = (nx, ny)
                    neighbors.append(neighbor_node)

            # add node with neighbours to the graph
            nodes[current_node] = neighbors

    return nodes, start_node, end_node

# ot: order tuple
def ot(t):
    '''Returns a tuple in order.'''
    return t if t[0] < t[1] else (t[1], t[0])

def reduce_graph2junctions(GRAPH):
    '''
    Reduces a graph to a graph of junctions and a dictionary of edges.

    Saying that this function is a bit suboptimal would be a slight understatement,
    feel free to optimize it ;)
    
    P.S. shere it with me if you do
    '''

    # initialize variables
    graph = deepcopy(GRAPH)
    edges = {}

    # loop until the iteration with no nodes removed
    while True:
        temp_graph = deepcopy(graph)

        # find nodes to remove
        for node, neighbors in graph.items():
            # skip nodes with more (or less) than 2 neighbors
            if len(neighbors) != 2: continue

            # redirect edges and update weights

            # update neighbors
            n1, n2 = neighbors
            temp_graph[n1][temp_graph[n1].index(node)] = n2
            temp_graph[n2][temp_graph[n2].index(node)] = n1

            # remove node
            del temp_graph[node]
            
            # update weights
            edges[ot((n1, n2))] = edges.get(ot((n1, node)), 1) + edges.get(ot((node, n2)), 1)

            # node was removed, update graph and start over
            break
        # if no nodes were removed, break
        else:
            break
        
        # update graph for the next iteration
        graph = deepcopy(temp_graph)

    # delete excess edges
    for node in GRAPH:
        for node2 in GRAPH:
            key = ot((node, node2))
            if key in edges and (node not in graph or node2 not in graph):
                del edges[ot((node, node2))]

    return graph, edges

def dfs(graph, weights, current_node, destination, \
        visited, current_length, max_length):
    '''Depth-first search.'''

    # mark node as visited
    visited[current_node] = True

    # recursion escape condition
    if current_node == destination:
        max_length[0] = max(max_length[0], current_length)

    # if not at the destination
    else:
        # explore all neighbors
        for neighbor in graph[current_node]:
            # if not visited
            if not visited[neighbor]:
                # recurse into the neighbor
                dfs(graph, weights, neighbor, destination, visited, \
                    current_length + weights[ot((current_node, neighbor))], max_length)

    # unmark node as visited
    visited[current_node] = False

def find_longest_path(graph, weights, start, end):
    '''Returns the longest path in a graph from start node to end node'''

    # initialize variables
    visited = {node: False for node in graph}
    max_length = [0]  # using a list to pass it by reference

    # start dfs recursion
    dfs(graph, weights, start, end, visited, 0, max_length)

    return max_length[0]


# TESTS
def test_display(tempo=0.1):
    print()
    print("TEST DISPLAY")
    print()

    start = tm.time()
    x, path = test_walk_recursive(tempo)

    print()
    print("LONGEST PATH:", path)
    print_map(DATA, path, "## --- FINNISHED --- ##", True)  
    print() 
    print("Result:", x)
    print(f"Time: {tm.time() - start:.2f} seconds")
    print()

def test_multiple(n=100):
    print()
    print("TEST MULTIPLE")
    print()

    start = tm.time()
    for _ in range(n):
        x = walk_recursive()

    print("Result:", x)
    print(f"Time: {tm.time() - start:.2f} seconds")
    print()


# MAIN
def star1():
    print("PART 1:")

    start_time = tm.time()
    result = walk_recursive()

    print(f"Result: {result}")
    print(f"Calculated in {tm.time() - start_time:.2f} seconds")
    print()

def star2():
    print("PART 2:")
    start_time = tm.time()

    print("getting graph...", end='\r')
    graph, start_node, end_node = get_graph()
    graph_obtained_time = tm.time()
    print(f"graph obtained in {graph_obtained_time - start_time:.2f}seconds")

    print("reducing graph...", end='\r')
    junctions, weights = reduce_graph2junctions(graph)
    graph_reduced_time = tm.time()
    print(f"graph reduced in {graph_reduced_time - graph_obtained_time:.2f}seconds")

    print("finding longest path...", end='\r')
    result = find_longest_path(junctions, weights, start_node, end_node)
    found_longest_path_time = tm.time()
    print(f"longest path found in {found_longest_path_time - graph_reduced_time:.2f}seconds")

    print("Part 2:", result)
    print(f"Combined time: {tm.time() - start_time:.2f} seconds")


# RUN
#test_display(0)
#test_multiple(500)
star1()
star2()




