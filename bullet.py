import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, game):
        """ Create bullet object at the current position of the ship """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Create bullet at (0,0) and then set current position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        # Store bullets position as float
        self.y = float(self.rect.y)

    def update(self):
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw Bullet to screen """
        pygame.draw.rect(self.screen, self.color, self.rect)
