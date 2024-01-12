import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ Manage Ship """
    def __init__(self, game):
        """ Initialize the ship and the starting position """
        super().__init__()
        # Get the screen and settings attribute of the game instance
        self.screen = game.screen
        self.settings = game.settings
        # get the screens rect attribute to determine the location of the ship
        self.screen_rect = game.screen.get_rect()

        # Load the ship image and get its rect attribute
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start new ship at the bottom middle of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store float for exact location
        self.x = float(self.rect.x)

        # Initialize movement flag
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """ Center the ship on the screen """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """ Update the ships position based on the flag """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """ Draw the ship at the current position """
        self.screen.blit(self.image, self.rect)
