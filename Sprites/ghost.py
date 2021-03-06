import pygame

 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

#http://www.programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py 


class GhostAgent(pygame.sprite.Sprite):
        # Constructor function
    def __init__(self, x, y, name):
        # Call the parent's constructor
        super().__init__()

        self.image = pygame.image.load("Images/ghosts/"+name+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10,10))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
 
    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y
        
    def update(self, x = None, y  = None):
        """ Update the ghost position. """
        # Move left/right
        self.rect.x += self.change_x
        # print(self.rect.x)
        # print(self.rect.y)
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
    
