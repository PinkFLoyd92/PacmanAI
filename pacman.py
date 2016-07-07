import os, sys
import pygame
from pygame.locals import *
from Sprites.wall import Wall
from Sprites.pacmanAgent import PacmanAgent

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
        
        wall = Wall(10, 0, 20, 20)
        self.wall_list.add(wall)
        self.all_sprite_list.add(wall)
 
        wall = Wall(10, 200, 100, 10)
        self.wall_list.add(wall)
        self.all_sprite_list.add(wall)
 
        # Create the player paddle object
        self.pacman = PacmanAgent(50, 50)
        self.pacman.walls = self.wall_list
 
        self.all_sprite_list.add(self.pacman)
 
        self.clock = pygame.time.Clock()
    def loadLayout(self):
        """We load the layout from the file"""
        pass
    def mainLoop(self):
        "Main loop of the game"
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pacman.changespeed(-3, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.changespeed(3, 0)
                    elif event.key == pygame.K_UP:
                        self.pacman.changespeed(0, -3)
                    elif event.key == pygame.K_DOWN:
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
