import pygame

class Ship:
    """A class to manage ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set inital position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        self.settings = ai_game.settings
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship`s position based on the movement flags."""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x
