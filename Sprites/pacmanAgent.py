import pygame
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)


# http://www.programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
class PacmanAgent(pygame.sprite.Sprite):
    """Class of the pacman agent"""
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        # self.image = pygame.Surface([15, 15])
        # self.image.fill(WHITE)
        self.image = pygame.image.load("Images/pacman_right.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        self.walls = None
        self.dots_to_eat = None

    def changespeed(self, pos_x, pos_y):
        """ Change the speed of the player. """
        self.change_x += pos_x
        self.change_y += pos_y

    def tryToEatDot(self):
        """Eat a dot, update the dots counter"""
        block_hit_list = pygame.sprite.spritecollide(self, self.dots_to_eat, False)
        for dot in block_hit_list:
            # self.dots_to_eat.remove(dot)
            # dot.get_image_state()
            # dot.kill()
            if dot.get_image_state() is True:
                dot.update_image_state()

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x
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
