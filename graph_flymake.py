""" All the state of the game will be saved here"""
import networkx as nx

class Pacman_Graph(object):
    """ this class is used to represent all the dots, the pacman
    and the ghost in the board
    """
    def __init__(self, args):
        super(Pacman_Graph, self).__init__()
        self.args = args
        self.graph = nx.Graph()
        self.currentNode = None

    def create_node(self, prev_node=None):
        """ Each one of the nodes is a Sprite. """
       self.graph.add_node() 
