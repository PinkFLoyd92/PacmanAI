import networkx as nx
from graph import Pacman_Graph

class Node:
    def __init__(self, graph_node, node_pacman, node_ghost):
        """ Initialize the node with the sprite in that node(graph_node), the type of node(type) """
        self.graph_node = graph_node
        self.node_ghost = node_ghost
        self.node_pacman = node_pacman
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other_node):
        """ method that computes the cost of the current node to another one"""
        pass

class State_Graph:
    def __init__(self):
        """ Class that contains the AI part of the program"""
        self.state_nodes = [] 

    def fillGraph(self, pacman_graph):
        pass

def children(point, grid):
    x, y = point. point
    links = [grid[d[0]][d[1]] for d in [(x-1, y), (x, y - 1), (x, y + 1), (x+1, y)]]
    return [link for link in links if link.value != '%']

def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])

def aStar(start, goal, graph):
    # The open and closed sets
    openset = set()
    closedset = set()
    # Current point is the starting point
    current = start
    # Add the starting point to the open set
    openset.add(current)
    # While the open set is not empty
    while openset:
        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o: o.G + o.H)
        # If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
                path.append(current)
            return path[::-1]
        # Remove the item from the open set
        openset.remove(current)
        # Add it to the closed set
        closedset.add(current)
        # Loop through the node's children/siblings
        for node in children(current, graph):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue
            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                # Set the parent to our current item
                node.parent = current
                # Add it to the set
                openset.add(node)
                # Throw an exception if there is no path
    raise ValueError('No Path Found')
