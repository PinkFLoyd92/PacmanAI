import os, sys
import pygame
from pygame.locals import *


if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')


class Block(pygame.sprite.Sprite):
    "Class that represents a block in the pacman game"
    def __init__(self,args):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()
