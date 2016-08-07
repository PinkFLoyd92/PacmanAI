""" All the state of the game will be saved here"""
import networkx as nx


class Node:
    def __init__(self, type, graph_node, node_pacman, node_ghost):
        """ Initialize the node with the sprite in that node(graph_node), the type of node(type) """
        self.type = type  # pacman or dot or ghost.
        self.graph_node = graph_node
        self.node_ghost = node_ghost
        self.node_pacman = node_pacman
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other_node):
        """ method that computes the cost of the current node to another one"""
       pass 
RIGHT = 1
LEFT = 2
DOWN = 3
TOP = 4

class Pacman_Graph(object):
    """ this class is used to represent all the dots, the pacman
    and the ghost in the board
    """
    def __init__(self):
        super(Pacman_Graph, self).__init__()
        self.graph = nx.Graph()
        self.node_pacman = None
        self.node_ghost = None
        self.lastCreatedNode = None
        self.nodes_list = []

    def checkTopCollisions(self, new_node):
        for node in self.nodes_list:
            if(node.rect.y is not new_node.rect.y):
                if(node.rect.x is new_node.rect.x and (new_node.rect.y - node.rect.y == 40)):
                    self.graph.add_edge(new_node, node, {"direction": TOP})
                    self.graph.add_edge(node, new_node, {"direction": DOWN})

    def create_node(self, new_node, pacman=False, ghost=False):
        """ Each one of the nodes is a Sprite (dot and the agents). """
        self.graph.add_node(new_node)
        if(self.lastCreatedNode is not None):
            if(self.lastCreatedNode.rect.y == new_node.rect.y and (new_node.rect.x - self.lastCreatedNode.rect.x == 40)):
                self.graph.add_edge(self.lastCreatedNode, new_node, {"direction": LEFT})
                self.graph.add_edge(new_node, self.lastCreatedNode, {"direction": RIGHT})

        self.checkTopCollisions(new_node)
        self.nodes_list.append(new_node)
        self.lastCreatedNode = new_node
        if pacman is not False:
            self.node_pacman = new_node
        elif ghost is not False:
            self.node_ghost = new_node

    def print_graph(self):
        print(self.graph.number_of_nodes())
        print(self.graph.number_of_edges())
        # print(self.graph.edges())
        for n, nbrs in self.graph.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['direction']
                print(data)

        print(self.node_ghost)
        print(self.node_pacman)
