"""
Class that representes the food in the board.
"""
import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

class Dot(pygame.sprite.Sprite):
    """ Dot of the Pacman Game. """
    def __init__(self, pos_x, pos_y, width, height):
        """ Constructor for the dot class. """
        # Call the parent's constructor
        super().__init__()

        # Make a blue wall, of the size specified in the parameters
        # self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("Images/dot.png").convert_alpha()
        # self.image.fill(BLUE)
        self.image = pygame.transform.scale(self.image, (width, height))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x
        self.has_image = True
        self.width = width
        self.height = height

    def get_image_state(self):
        """ return boolean telling if the dot has or does not have image. """
        return self.has_image


    def update_image_state(self):
        """ return boolean telling if the dot has or does not have image. """
        self.has_image = False
        self.image = pygame.image.load("Images/Empty.png").convert_alpha()
        self.image = pygame.Surface([self.width, self.height])
