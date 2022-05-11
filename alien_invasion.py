import sys

import pygame

from settings import Settings

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

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.bg_color = self.settings.bg_color


    def _set_screen(self, size):
        if size == "Fullscreen":
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_KEYDOWN_events(event)
            elif event.type == pygame.KEYUP:
                self._check_KEYUP_events(event)


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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet("up")
        elif event.key == pygame.K_z:
            self._fire_bullet("left")
        elif event.key == pygame.K_x:
            self._fire_bullet("right")
        elif event.key == pygame.K_q:
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


    def _update_bullets(self):
        self.bullets.update()
        # Get rid of the bullets that disappeared.
        for bullet in self.bullets.copy():
            if bullet.y <= 0 or bullet.x <= 0 or bullet.x >= self.settings.screen_width:
                self.bullets.remove(bullet)


    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        self.aliens.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw_bullet()

        # Make most recent screen visible:
        pygame.display.flip()


    def _fire_bullet(self, direction="up"):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, direction)
            self.bullets.add(new_bullet)


    def _create_fleet(self):
        """Create a fleet of aliens."""
        #First, make an alien
        alien = Alien(self)
        self.aliens.add(alien)

if __name__ == "__main__":
    # Make a game instance, and run it
    # size = input("Enter game screen size:")
    ai = AlienInvasion("Small")
    ai.run_game()
