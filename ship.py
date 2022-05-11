import pygame

class Ship:
    """A class to manage ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set inital position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False


    def blitme(self):
        """Draw the ship at its current position"""
        rotate_angle = 0
        if self.moving_right:
            rotate_angle = -self.settings.ship_rotate_scale
        elif self.moving_left:
            rotate_angle = +self.settings.ship_rotate_scale

        if rotate_angle != 0:
            self.screen.blit(pygame.transform.rotate(self.image, rotate_angle), self.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship`s position based on the movement flags."""
        if self.moving_up and self.rect.y > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.y < self.screen_rect.bottom - self.rect.height:
            self.y += self.settings.ship_speed
        if self.moving_left and self.rect.x > self.screen_rect.left:

            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.x < self.screen_rect.right - self.rect.width:
            self.x += self.settings.ship_speed

        self.rect.y = self.y
        self.rect.x = self.x
