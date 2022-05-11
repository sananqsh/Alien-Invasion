import sys
import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game, direction="up"):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.color = self.settings.bullet_color

        if direction == "up":
            self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
            self.rect.midtop = ai_game.ship.rect.midtop
        elif direction in ["left", "right"]:
            self.rect = pygame.Rect(0,0, self.settings.bullet_height, self.settings.bullet_width)
            self.rect.midtop = ai_game.ship.rect.center

            # Residing at the left/right side of the ship:
            if direction == "left":
                self.rect.x -= (ai_game.ship.rect.width / 2)
            elif direction == "right":
                self.rect.x += (ai_game.ship.rect.width / 2)


        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.direction = direction


    def update(self):
        """Move the bullet up the screen"""
        if self.direction == "up":
            self.y -= self.settings.bullet_speed
        elif self.direction == "left":
            self.x -= self.settings.bullet_speed
        elif self.direction == "right":
            self.x += self.settings.bullet_speed

        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
