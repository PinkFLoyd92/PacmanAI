import sys

import pygame
import time
from Sprites.food import Dot
from Sprites.ghost import GhostAgent
from Sprites.pacmanAgent import PacmanAgent
from Sprites.wall import Wall
from graph import Pacman_Graph
from graph import Node
# from pygame.locals import *
if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)


class PacmanMain:
    "This class handles the main initialization and creation of the game"
    def __init__(self, width=800, height=530):
        "initialize pygame"
        pygame.init()
        "set window size"
        self.width = width
        self.height = height
        "Create the screen"
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Set the title of the window
        pygame.display.set_caption('Pacman')

        # List to hold all the sprites
        self.all_sprite_list = pygame.sprite.Group()

        # list of the ghosts
        self.ghosts_list = pygame.sprite.Group()

        # List to hold the dots
        self.all_dots_list = pygame.sprite.Group()
        # Make the walls. (x_pos, y_pos, width, height)
        self.wall_list = pygame.sprite.Group()
        self.graph = Pacman_Graph()
        self.loadLayout("./Game-Layout/layout")
        self.pacman.dots_to_eat = self.all_dots_list
        # Create the player paddle object
        # self.pacman = PacmanAgent(20, 20)
        self.pacman.walls = self.wall_list
        self.all_sprite_list.add(self.pacman)
        self.clock = pygame.time.Clock()

    def loadLayout(self, filepath):
        """We load the layout from the file"""
        lineY = 0  # number of the iteration
        lineX = 0  # actual position in X of the sprite.
        counterGhosts = 0  # counter of the number of ghosts in the game
        f = open(filepath, 'r')
        for line in f:
            lineX = 0  # actual position in X of the sprite
            line = line.strip()
            for c in line:
                if(c == "@"):
                    wall = Wall(lineX, lineY*40, 35, 35)
                    self.wall_list.add(wall)
                    self.all_sprite_list.add(wall)
                elif(c == "."):
                    dot = Dot(lineX+10, lineY*40+15, 10, 10)
                    # print(dot.rect.y)
                    self.all_sprite_list.add(dot)
                    self.all_dots_list.add(dot)
                    dot_node = Node(dot)
                    self.graph.create_node(dot_node, False, False)
                elif(c == "P"):
                    self.pacman = PacmanAgent(lineX+10, lineY*40 + 15)
                    self.pacman.walls = self.wall_list
                    self.all_sprite_list.add(self.pacman)
                    pacman_node = Node(self.pacman)
                    self.graph.create_node(pacman_node, True, False)
                elif(c == "G"):
                    if(counterGhosts == 0):
                        ghost = GhostAgent(lineX+10, lineY*40 + 15, "blinky")
                        ghost.walls = self.wall_list
                        self.ghosts_list.add(ghost)
                        self.all_sprite_list.add(ghost)
                        ghost_node = Node(ghost)
                        self.graph.create_node(ghost_node, False, True)
                    counterGhosts += 1
                elif(c == "o"):
                    pass
                lineX += 40
            lineY += 1
        # self.graph.updatePacmanPosition()

    def mainLoop(self):
        "Main loop of the game"
        i = 0
        goal = None
        new_ghost_path = self.graph.getGhostPath()
        if (goal == None):
            goal = self.graph.generateNextPill()
        array_aStar = self.graph.aStar(self.graph.node_pacman, goal, self.graph)
        self.graph.printDjistra(array_aStar)
        while 1:
            #try to eat dot in position
            self.pacman.tryToEatDot()
            print("el nodo esta en " + str(self.graph.node_pacman.graph_node.rect.x) + ", " + str(self.graph.node_pacman.graph_node.rect.y))
            if(goal == None):
                goal = self.graph.generateNextPill()

            #list of movements that are followed in order to go to that pill.
            # array_aStar = self.graph.aStar(self.graph.node_pacman, goal, self.graph)
            if(len(array_aStar) == 1):
                goal = self.graph.generateNextPill()
                array_aStar = self.graph.aStar(self.graph.node_pacman, goal, self.graph)

            # we move PacmanAgent to our new node.
            new_dot2 = self.graph.updateAgentPosition(self.graph.node_pacman, array_aStar[1])[0]
            del (array_aStar[0])
            self.all_dots_list.add(new_dot2)
            self.all_sprite_list.add(new_dot2)
            self.screen.fill(BLACK)
            self.all_sprite_list.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

            #update ghost movement.............
            new_dot = self.graph.updateAgentPosition(self.graph.node_ghost,new_ghost_path[1])[0]
            self.all_dots_list.add(new_dot)
            self.all_sprite_list.add(new_dot)
            self.screen.fill(BLACK)
            self.all_sprite_list.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
            del(new_ghost_path[0])
            new_ghost_path = self.graph.getGhostPath()
            time.sleep(1)

            self.screen.fill(BLACK)
            self.all_sprite_list.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


def main():
    MainWindow = PacmanMain()
    MainWindow.mainLoop()

if __name__ == '__main__':
    main()
