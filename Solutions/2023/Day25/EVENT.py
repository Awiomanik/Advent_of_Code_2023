# ADVENT OF CODE 2023
# WOJCIECH KOŚNIK-KOWALCZUK
# DAY: 25


from copy import deepcopy
from collections import defaultdict
from itertools import combinations
import networkx as nx


# GET DATA
with open("DATA.txt", 'r') as data_file:
    data = data_file.read().split('\n')
    data = {(c := component.split(": "))[0]: c[1].split(' ') for component in data}


# UTILITY FUNCTIONS
def build_graph():
    '''
    Builds a graph from the DATA constant.

    Returns:
    - A tuple containning two graph representations:
        - A dictionary with vertex IDs valued by sets of IDs of vertices connected to the key vertex.
        - A networkx graph representation of the same data.
    '''

    # create a mapping of nodes to integers
    nodes = set(node for connections in data.values() for node in connections)
    nodes.update(data.keys())
    node_to_int = {node: i for i, node in enumerate(nodes)}

    # create a dict_graph
    dict_graph = defaultdict(set)

    # iterate over data to get vertecies
    for component, connections in data.items():
        component = node_to_int[component]

        # add established connections to vertex
        dict_graph[component].update(node_to_int[con] for con in connections)

        # add backward connections to vertex
        for con in connections:
            con = node_to_int[con]
            dict_graph[con].add(component)

    # initialize networkx graph representation
    networkx_graph = nx.Graph()

    # populate networkx graph
    for node, connections in dict_graph.items():
        for connection in connections:
            networkx_graph.add_edge(node, connection)    

    return dict_graph, networkx_graph

def count_groups(graph):
    '''
    Identifies the connected components (groups) in the given graph and calculates the product of their sizes.

    Args:
    - A dictionary with vertex IDs valued by sets of IDs of vertices connected to the key vertex.

    Returns:
    - Product of sizes of components in the graph if there are exactly two components, None otherwise.
    '''

    # initialize variables
    visited = set()
    components = []

    # recursive function for depth-first search
    def dfs(node, component):
        # mark node as visited and add it to the current component
        visited.add(node)
        component.add(node)
        # recursively visit all unvisited neighbors
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)

    # iterate over all nodes in the graph
    for node in graph:
        if node not in visited:
            # create a new component and perform depth-first search on it
            component = set()
            dfs(node, component)
            components.append(component)

    # return the product of sizes of components if there are exactly two components
    if len(components) == 2: return len(components[0]) * len(components[1])
    return None

def cut_wire(graph, connection):
    '''
    Cuts the wire between two modules in the given graph.

    Args:
    - graph: A dictionary with vertex IDs valued by sets of IDs of vertices connected to the key vertex.
    - connection: A tuple of two vertex IDs representing the connection to cut.
    '''

    # remove the connection from the graph (if it exists)
    try:
        graph[connection[0]].remove(connection[1])
    except:
        pass

    # remove reverse connection from the graph (if it exists)
    try:
        graph[connection[1]].remove(connection[0])
    except:
        pass

def generate_ordered_triplets(sorted_wires):
    '''
    Generates all possible triplets of wires in descending order of their usage counts.

    Parameters:
    - sorted_wires: A list of tuples where each tuple contains a wire and its usage count, sorted by usage count.

    Yields:
    - A tuple containing three wires.
    '''

    # iterate over sorted wires
    for i in range(len(sorted_wires)):
        for j in range(i+1, len(sorted_wires)):
            for k in range(j+1, len(sorted_wires)):

                # yield the triplet
                yield (sorted_wires[i][0], sorted_wires[j][0], sorted_wires[k][0])

def find_wires_to_cut(graph, sorted_wires):
    '''
    Finds the combination of three wires in the given graph that separates it into two components \
    and returns the product of sizes of those components.
    
    Args:
    - graph: A dictionary with vertex IDs valued by sets of IDs of vertices connected to the key vertex.
    - sorted_wires: A list of tuples of two vertex IDs representing the wires sorted by their usage counts in descending order.
    
    Returns:
    - Product of sizes of components in the graph if there are exactly two components, None otherwise.'''

    # iterate over all possible triplets of wires in descending order of their usage counts
    for triplet in generate_ordered_triplets(sorted_wires):

        # create a copy of the graph
        current_graph = deepcopy(graph)

        # cut the wires
        cut_wire(current_graph, triplet[0])
        cut_wire(current_graph, triplet[1])
        cut_wire(current_graph, triplet[2])

        # check if the graph is still connected
        if (g := count_groups(current_graph)): return g


# FINAL SOLUTION
def final_solution_for_year_2023_omg_nice_we_did_it_guys():
    '''
    In the last task this year I did not find some super creative solution,
    I was adheard to the original (quite brute-forcy) idea of cutting subsequent triplets of wires
    and checking if the graph is still connected and to three simple rules: optimize, optimize, optimize!
    Somehow I managed to get the solution in under a secound, which is not bad at all.
    Thank you for reading this code and I hope you enjoyed the adventure as much as I did!
    See you next year, WKK.
    '''
    
    # build dictionary graph representation
    print("Initializing graphs...", end='')
    dict_graph, networkx_graph = build_graph()
    print("\r - Graphs initialized!    ")
    
    # get the usage count of each wire
    print("Generating wires usage count...", flush=True, end='')
    wires_use_count = nx.edge_betweenness_centrality(networkx_graph)
    print("\r - Wires usage count generated!    ")


    # sort the wires based on their usage counts in descending order
    print("Sorting wires...", flush=True, end='')
    sorted_wires = sorted(wires_use_count.items(), key=lambda x: x[1], reverse=True)
    print("\r - Wires sorted!    ")

    # print the answear
    print("The answear for the final task in 2023 Advent of code adventure is:", find_wires_to_cut(dict_graph, sorted_wires))


# RUN THE FINAL SOLUTION
final_solution_for_year_2023_omg_nice_we_did_it_guys()

