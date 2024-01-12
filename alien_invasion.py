import sys

import pygame

from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """ Manage game assets and behavior """

    def __init__(self):
        """ Initialize and create resources """
        pygame.init()
        # Initialize clock for frame rate
        self.clock = pygame.time.Clock()
        # import game settings
        self.settings = Settings()
        # Game window

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Caption of the screen
        pygame.display.set_caption("Alien Invasion")

        # Store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Initialize the ship
        self.ship = Ship(self)
        # Create a group to hold the bullets
        self.bullets = pygame.sprite.Group()
        # Create a group to hold the aliens
        self.aliens = pygame.sprite.Group()

        # Initialize fleet of aliens
        self._create_fleet()

        # Initialize game status
        self.game_active = False

        # Make the button
        self.play_button = Button(self, "Play!")

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            # Helper method to check events
            self._check_events()

            # Check if game is not over
            if self.game_active:
                # Update the ships location
                self.ship.update()
                # Update position of bullets
                self._update_bullets()
                # move aliens
                self._update_aliens()

            # Helper method to redraw the screen
            self._update_screen()
            # Set frame rate to 60. The loop runs 60 times a second.
            self.clock.tick(60)

    def _check_events(self):
        """ Respond to key presses and mouse events"""
        # Event loop to watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Movement of the ship
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Start a new Game when player clicks Play """
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            sleep(0.35)
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            # Hide the cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """ Response for key presses """
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Response for key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # Remove bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            self._check_collision()

    def _check_collision(self):
        # Check if bullets hit aliens, if so remove the alien and the bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Destroy existing bullets and create new fleet if all aliens are destroyed.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """ Update the number of ships available when hit """
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # clear the game
            self.bullets.empty()
            self.aliens.empty()

            # Create new aliens and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1)
        elif self.stats.ships_left <= 0:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens reaching the bottom of the screen
        self._check_aliens_bottom()

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_fleet(self):
        """ Create fleet of Aliens """
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height * 1.75
        while current_y < (self.settings.screen_height - 12 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 1.25 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """ Update images on the screen, and flip to new screen """
        # Redraw the screen during each iteration
        self.screen.fill(self.settings.bg_color)

        # Display play button when inactive
        if not self.game_active:
            self.play_button.draw_button()
        else:
            # Display bullets on screen
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # Display the ship on screen
            self.ship.blitme()
            self.aliens.draw(self.screen)

            # Draw the score information.
            self.sb.show_score()

        # Make the most recent screen drawn visible
        pygame.display.flip()
