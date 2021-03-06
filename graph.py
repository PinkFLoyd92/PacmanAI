""" All the state of the game will be saved here"""
import networkx as nx
import pygame
from Sprites.food import Dot
from Sprites.ghost import GhostAgent
from Sprites.pacmanAgent import PacmanAgent
import time
from queue import PriorityQueue
import random

RIGHT = 1
LEFT = 2
DOWN = 3
TOP = 4

class Node:
    def __init__(self, graph_node):
        """ Initialize the node with the sprite in that node(graph_node), the type of node(type) """
        self.graph_node = graph_node
        self.parent = None
        self.H = 0.00
        self.G = 0.00
        self.F = 0.00

    def move_cost(self, other_node):
        """ method that computes the cost of the current node to another one"""
        pass

class Pacman_Graph():
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

    def computeCost(self, node, goal):
        return self.manhattan(node,self.node_ghost) + self.manhattan(node,goal)

    def checkTopCollisions(self, new_node):
        for node in self.nodes_list:
            if(node.graph_node.rect.y != new_node.graph_node.rect.y):
                if (new_node.graph_node.rect.x == 730 and new_node.graph_node.rect.y == 455):
                    if(node.graph_node.rect.x == 730 and node.graph_node.rect.y == 415):
                        if (node.graph_node.rect.x == new_node.graph_node.rect.x and new_node.graph_node.rect.y - node.graph_node.rect.y == 40):
                            print("sadas")
                if(node.graph_node.rect.x == new_node.graph_node.rect.x and new_node.graph_node.rect.y - node.graph_node.rect.y == 40):
                    self.graph.add_edge(new_node, node, {"direction": TOP, "weight": 1})
                    self.graph.add_edge(node, new_node, {"direction": DOWN, "weight": 1})
                    # print(new_node)

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
        print(nx.dijkstra_path(self.graph, self.node_pacman, self.lastCreatedNode))

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
                #if(neighbor is not prev_node and isinstance(neighbor.graph_node, Dot) and neighbor.graph_node.has_image):
                if(neighbor != prev_node and isinstance(neighbor.graph_node, Dot) and neighbor.graph_node.has_image):
                    return neighbor
                # elif(neighbor is not prev_node and not neighbor.graph_node.has_image):
                elif(neighbor != prev_node and not neighbor.graph_node.has_image):
                    return self.generateNeighborPill(neighbor, node)

    def generateNextPill(self):
        list_nodes_temp = self.aStar(self.node_pacman, self.node_ghost,self.graph)
        list_nodes = []
        array_nodes = []
        manhattan = {'node':[], 'distance': 0}
        possible_options = self.graph.neighbors(self.node_pacman)
        for node in possible_options:
            path_total = nx.dijkstra_path(self.graph, self.node_ghost, self.node_pacman)
            len_path = len(path_total)
            if(self.manhattan(node,self.node_ghost) > manhattan['distance'] -10 and len_path>4):
                manhattan['node'].append(node)
                manhattan['distance'] = self.manhattan(node,self.node_ghost)
        random.shuffle(manhattan['node'])
        for node in manhattan['node'] :
            if(node.graph_node.has_image ==True):
                return node
        if(len(manhattan['node']) == 0):
            possible_options = self.graph.neighbors(self.node_pacman)
            best = {'node': None, 'distance': 0}
            for node in possible_options:
                if(self.manhattan(node, self.node_ghost)> best['distance']):
                    best['node'] = node
                    best['distance'] = self.manhattan(node, self.node_ghost)
            return best['node']



        return manhattan['node'][0]

    # here we update the node where an agent is moved and return the node
    def updateAgentPosition(self, agent, next_node = None):
        agent_neighbors = self.graph.neighbors(agent)
        agent_edges = self.graph.edges(agent, data= True)

        # creating a dot in agent position
        dot = Dot(agent.graph_node.rect.x, agent.graph_node.rect.y, 10, 10)
        node_dot = Node(dot)
        print("update")
        for edge in agent_edges:
            self.graph.remove_edge(agent, edge[1])
            self.graph.remove_edge(edge[1], agent)
            self.graph.add_edge(node_dot, edge[1], edge[2])
            if(edge[2]['direction'] == TOP):
                self.graph.add_edge(edge[1], node_dot, {"direction": DOWN, "weight": 1})

            elif (edge[2]['direction'] == DOWN):
                self.graph.add_edge(edge[1], node_dot, {"direction": TOP, "weight": 1})
            elif (edge[2]['direction'] == RIGHT):
                self.graph.add_edge(edge[1], node_dot, {"direction": LEFT, "weight": 1})
            elif (edge[2]['direction'] == LEFT):
                self.graph.add_edge(edge[1], node_dot, {"direction": RIGHT, "weight": 1})

        # now we put the new position of the pacman node.

        agent.graph_node.rect.x = next_node.graph_node.rect.x
        agent.graph_node.rect.y = next_node.graph_node.rect.y
        # next_node.graph_node.update_image_state()
        image_dot = None
        if(isinstance(next_node.graph_node,Dot)):
            print("siguiente dot debe actualizarse o no: " + str(next_node.graph_node.has_image))
            if(next_node.graph_node.has_image == True):
                image_dot = True
            else:
                image_dot = False
        next_node.graph_node.kill()

        next_node.graph_node = agent.graph_node
        if(isinstance(agent.graph_node, PacmanAgent)):
            dot.update_image_state()
            self.node_pacman = next_node
            print("update pacman position")
        elif(isinstance(agent.graph_node, GhostAgent)):
            print("update ghost position")
            if(image_dot == False):
                dot.update_image_state()
            self.node_ghost = next_node

        return [dot,next_node]

    def getGhostPath(self):
        try:
            path = nx.dijkstra_path(self.graph, self.node_ghost, self.node_pacman)
            return (nx.dijkstra_path(self.graph, self.node_ghost, self.node_pacman))
        except nx.NetworkXError:
            print("error")
            return self.graph.neighbors(self.node_ghost)

    def printDjistra(self,path):
        try:
            i = 0
            for node in path:
                i = i + 1
                sprite = node.graph_node
                print("el nodo " + str(i) + "tiene" + "en X " + str(sprite.rect.x) + "en Y " + str(sprite.rect.y))
                # time.sleep(1)
        except nx.NetworkXError:
            print("error")

    # startNode, goalNode, graph.
    def aStar(self, start, goal, graph):
        path = []
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
                while current.parent and isinstance(current.parent, Dot):
                    path.append(current)
                    current = current.parent
                    path.append(current)
                return path

            # Remove the item from the open set
            openset.remove(current)
            # Add it to the closed set
            closedset.add(current)
            # Loop through the node's children/siblings
            for node in self.graph.neighbors(current):
                if node is not None and isinstance(node.graph_node,Dot):
                    # If it is already in the closed set, skip it
                    if node in closedset:
                        continue
                    # Otherwise if it is already in the open set
                    if node in openset:
                        # Check if we beat the G score
                        new_g = current.G + self.manhattan(current, node)
                        if node.G < new_g:
                            # If so, update the node to have a new parent
                            node.G = new_g
                            node.parent = current
                    else:
                        # If it isn't in the open set, calculate the G and H score for the node
                        node.G = current.G + self.manhattan(node, self.node_ghost)
                        print("node")
                        print(node.graph_node)
                        print(goal.graph_node)
                        node.H = self.manhattan(node, goal)
                        # Set the parent to our current item
                        node.parent = current

                        # Add it to the set
                        openset.add(node)


    # getting the distance
    def manhattan(self, node1, node2):
        return abs(node2.graph_node.rect.x - node1.graph_node.rect.x) + abs(node2.graph_node.rect.y - node1.graph_node.rect.y)

    # obtenemos el g,h de los nodos.
    def heuristic_goal(self,first,next, goal):
        h = 0
        g = 0
        path = nx.dijkstra_path(self.graph, next, goal)
        length = len(path)
        if(length > 5):
            h = 1
        elif(length<=5):
            h = (length)/5
        if(self.manhattan(first, self.node_ghost)>200):
            g = 0
        elif(self.manhattan(first, self.node_ghost)<=200):
            g = 1 - self.manhattan(first, self.node_ghost)/200
        return [g,h]

    def printPacmanPosition(self):
        pass


    def heuristic(self,a, b):
        return self.manhattan(a,b)

    def a_star_search(self, graph, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0.00)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + self.manhattan(current, next)
                if next not in cost_so_far or new_cost > cost_so_far[next]: # the more the cost is the best.
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far
