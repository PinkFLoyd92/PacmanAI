import os, sys
import pygame
from pygame.locals import *
from Sprites.wall import Wall
from Sprites.pacmanAgent import PacmanAgent
from Sprites.food import Dot
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
"Main tutorial -> http://www.learningpython.com/2006/03/12/creating-a-game-in-python-using-pygame-part-one/"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

class PacmanMain:
    "This class handles the main initialization and creation of the game"
    def __init__(self, width=800, height=600):
        "initialize pygame"        
        pygame.init()
        "set window size"
        self.width = width
        self.height = height
        "Create the screen"
        self.screen = pygame.display.set_mode((self.width,self.height))

        # Set the title of the window
        pygame.display.set_caption('Pacman')

        # List to hold all the sprites
        self.all_sprite_list = pygame.sprite.Group()
 
# Make the walls. (x_pos, y_pos, width, height)
        self.wall_list = pygame.sprite.Group()
        
        self.loadLayout("./Game-Layout/layout")
 
        # Create the player paddle object
        #self.pacman = PacmanAgent(20, 20)
        self.pacman.walls = self.wall_list
 
        self.all_sprite_list.add(self.pacman)
 
        self.clock = pygame.time.Clock()
    def loadLayout(self, filepath):
        """We load the layout from the file"""
        lineY = 0  #number of the iteration
        lineX = 0  #actual position in X of the sprite.
        f = open(filepath, 'r')
        for line in f:
            lineX = 0  #actual position in X of the sprite.        
            line = line.strip()
            print(line)
            for c in line:
                if(c == "@"):
                    wall = Wall(lineX,lineY*40, 40, 40)
                    self.wall_list.add(wall)
                    self.all_sprite_list.add(wall)
                elif(c == "."):
                    dot = Dot(lineX+10,lineY*40+15, 10, 10)
                    self.all_sprite_list.add(dot)
                elif(c == "P"):
                    self.pacman = PacmanAgent(lineX+20, lineY*40)
                    self.pacman.walls = self.wall_list
                    self.all_sprite_list.add(self.pacman)
                elif(c == "G"):
                    pass
                elif(c == "o"):
                    pass
                lineX += 40
            lineY+=1
    def mainLoop(self):
        "Main loop of the game"
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.pacman.image = pygame.transform.scale(self.pacman.image, (30,30))
                    if event.key == pygame.K_LEFT:
                        self.pacman.image = pygame.image.load("Images/pacman_left.png").convert_alpha()
                        self.pacman.changespeed(-3, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.image = pygame.image.load("Images/pacman_right.png").convert_alpha()
                        self.pacman.changespeed(3, 0)
                    elif event.key == pygame.K_UP:
                        self.pacman.image = pygame.image.load("Images/pacman_top.png").convert_alpha()
                        self.pacman.changespeed(0, -3)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.image = pygame.image.load("Images/pacman_down.png").convert_alpha()
                        self.pacman.changespeed(0, 3)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.pacman.changespeed(3, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.changespeed(-3, 0)
                    elif event.key == pygame.K_UP:
                        self.pacman.changespeed(0, 3)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.changespeed(0, -3)
            self.all_sprite_list.update()
            self.screen.fill(BLACK)
            self.all_sprite_list.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
def main():
    MainWindow = PacmanMain()
    MainWindow.mainLoop()

if __name__ == '__main__':
    main()
