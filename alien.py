import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """ Represent single alien in the fleet """
    def __init__(self, game):
        """ Initialize the alien and starting position """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load alien image and set its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start the alien on top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien to the left or right."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
