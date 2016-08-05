""" All the state of the game will be saved here"""
import networkx as nx

RIGHT = 1
LEFT = 2
DOWN = 3
TOP = 4

class Pacman_Graph(object):
    """ this class is used to represent all the dots, the pacman
    and the ghost in the board
    """
    def __init__(self, args):
        super(Pacman_Graph, self).__init__()
        self.args = args
        self.graph = nx.Graph()
        self.node_pacman = None
        self.node_ghost = None

    def checkTopCollisions(self, new_node):
        for node in self.graph.nodes:
            if(node.rect.y is not new_node.rect.y):
                if(node.rect.x is new_node.rect.x and (new_node.rect.y - node.rect.y == 40)):
                    self.graph.add_edge(new_node, node, {"direction": TOP})
                    self.graph.add_edge(node, new_node, {"direction": DOWN})

    def create_node(self, new_node, prev_node=None):
        """ Each one of the nodes is a Sprite. """
        self.graph.add_node(new_node)
        if(prev_node is not None):
            if(prev_node.rect.y == new_node.rect.y):
                self.graph.add_edge(prev_node, new_node, {"direction": LEFT})
                self.graph.add_edge(new_node, prev_node, {"direction": RIGHT})
                self.checkTopCollisions()
