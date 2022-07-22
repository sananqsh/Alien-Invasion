import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """General class to manage assets and behavior"""
    def __init__(self, size="Medium"):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings(size)
        self._set_screen(size)

        self.stats = GameStats(self)

        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def _set_screen(self, size):
        if size == "Fullscreen":
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.bg_color = self.settings.bg_color
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_KEYDOWN_events(event)
            elif event.type == pygame.KEYUP:
                self._check_KEYUP_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos = None):
        """Start a new game when player clicks Play."""
        if not self.stats.game_active:
            if mouse_pos:
                button_clicked = self.play_button.rect.collidepoint(mouse_pos)
                if button_clicked:
                    self._start_game()
            else:
                self._start_game()

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

    def _check_KEYDOWN_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        if event.key == pygame.K_SPACE:
            self._fire_bullet("up")
        if event.key == pygame.K_z:
            self._fire_bullet("left")
        if event.key == pygame.K_x:
            self._fire_bullet("right")
        if event.key == pygame.K_p:
            self._check_play_button()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_KEYUP_events(self, event):
        """"Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game(self):
        # Reset game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_score()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _update_bullets(self):
        self.bullets.update()
        # Get rid of the bullets that disappeared.
        for bullet in self.bullets.copy():
            if bullet.y <= 0 or bullet.x <= 0 or bullet.x >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Resopnd to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # The value associated with each bullet is a list of aliens it has
        #   collided with
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_intensity()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ship_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(self.settings.time_after_ship_hit)
        else:
            self.stats.game_active = False

    def _update_aliens(self):
        """
            Check if the fleet is at an edge
                then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_fleet_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._drop_fleet()
                self._change_fleet_direction()
                break

    def _check_fleet_bottom(self):
        """Check if any aliens reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _drop_fleet(self):
        """Drop the entire fleet."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

    def _change_fleet_direction(self):
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        for bullet in self.bullets:
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.scoreboard.show_scores()

        if not self.stats.game_active:
            pygame.mouse.set_visible(True)
            self.play_button.draw_button()

        # Make most recent screen visible:
        pygame.display.flip()

    def _fire_bullet(self, direction="up"):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, direction)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

if __name__ == "__main__":
    # Make a game instance, and run it
    # size = input("Enter game screen size:")
    ai = AlienInvasion("Fullscreen")
    ai.run_game()
