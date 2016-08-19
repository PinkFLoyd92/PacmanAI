""" All the state of the game will be saved here"""
import networkx as nx
import pygame
from Sprites.food import Dot
RIGHT = 1
LEFT = 2
DOWN = 3
TOP = 4

class Node:
    def __init__(self, graph_node):
        """ Initialize the node with the sprite in that node(graph_node), the type of node(type) """
        self.graph_node = graph_node
        self.H = 0
        self.G = 0
        self.F = 0

    def move_cost(self, other_node):
        """ method that computes the cost of the current node to another one"""
        pass

class Pacman_Graph(object):
    """ this class is used to represent all the dots, the pacman
    and the ghost in the board
    """
    def __init__(self):
        super(Pacman_Graph, self).__init__()
        self.graph = nx.DiGraph()
        self.node_pacman = None
        self.node_ghost = None
        self.lastCreatedNode = None
        self.nodes_list = []

    def checkTopCollisions(self, new_node):
        for node in self.nodes_list:
            if(node.graph_node.rect.y != new_node.graph_node.rect.y):
                if (new_node.graph_node.rect.x == 730 and new_node.graph_node.rect.y == 455):
                    if(node.graph_node.rect.x == 730 and node.graph_node.rect.y == 415):
                        if (node.graph_node.rect.x == new_node.graph_node.rect.x and new_node.graph_node.rect.y - node.graph_node.rect.y == 40):
                            pass
                if(node.graph_node.rect.x == new_node.graph_node.rect.x and new_node.graph_node.rect.y - node.graph_node.rect.y == 40):
                    self.graph.add_edge(new_node, node, {"direction": TOP, "weight": 1})
                    self.graph.add_edge(node, new_node, {"direction": DOWN, "weight": 1})

    def create_node(self, new_node, pacman=False, ghost=False):
        """ Each one of the nodes is a Sprite (dot and the agents). """
        self.graph.add_node(new_node)
        if(self.lastCreatedNode is not None):
            if(self.lastCreatedNode.graph_node.rect.y == new_node.graph_node.rect.y and (new_node.graph_node.rect.x - self.lastCreatedNode.graph_node.rect.x == 40)):
                self.graph.add_edge(self.lastCreatedNode, new_node, {"direction": LEFT, "weight": 1})
                self.graph.add_edge(new_node, self.lastCreatedNode, {"direction": RIGHT, "weight": 1})
                self.checkTopCollisions(new_node)
                # print(self.graph.neighbors(new_node))
        self.nodes_list.append(new_node)
        self.lastCreatedNode = new_node
        if(self.lastCreatedNode.graph_node.rect.x == 730 and self.lastCreatedNode.graph_node.rect.y == 455):
            pass
        if pacman is not False:
            self.node_pacman = new_node
        elif ghost is not False:
            self.node_ghost = new_node

    def getChildren(self, node):
        pass

    def print_graph(self):
        print(self.graph.number_of_nodes())
        print(self.graph.number_of_edges())
        for n, nbrs in self.graph.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['direction']
                print(data)

        print(self.node_ghost)
        print(self.node_pacman)
        # print(nx.dijkstra_path(self.graph, self.node_pacman, self.lastCreatedNode))

    def getClosestPills(self, node):
        """returns an array with the next nodes that have a pill in them"""
        array_nodes = []
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            if(isinstance(neighbor.graph_node, Dot)):
                if(neighbor.graph_node.has_image):
                    array_nodes.append(neighbor)
                elif(not neighbor.graph_node.has_image):
                    array_nodes.append(self.generateNeighborPill(neighbor, node))  # generate each neighbor pill
        return array_nodes

    def generateNeighborPill(self, node, prev_node):
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            if(isinstance(neighbor.graph_node, Dot)):
                if(neighbor is not prev_node and isinstance(neighbor.graph_node, Dot) and neighbor.graph_node.has_image):
                    return neighbor
                elif(neighbor is not prev_node and not neighbor.graph_node.has_image):
                    return self.generateNeighborPill(neighbor, node)
