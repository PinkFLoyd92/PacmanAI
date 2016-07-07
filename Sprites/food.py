import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

class Dot(pygame.sprite.Sprite):
    """ Dot of the Pacman Game. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        #self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("Images/dot.png").convert_alpha()
        #self.image.fill(BLUE)
        self.image = pygame.transform.scale(self.image, (width,height))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
