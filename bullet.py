import pygame
import assets as il

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ship import Ship
    from game import GameWorld


#bullet.py
class LaserBullet(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, ship_rect: pygame.rect.Rect, x_speed: float, y_speed: float, max_kills=1):
        super().__init__()

        self.max_kills = max_kills
        self.screen = screen
        self.image = il.image_load("images/bullet.png")
        self.rect = self.image.get_rect()

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.rect.centerx = ship_rect.centerx
        self.rect.bottom = ship_rect.top-1

        self.true_x = self.rect.x
        self.true_y = self.rect.y

    def update(self):
        """Updates bullet's state, removes bullet and moves it"""
        if 0 > self.rect.bottom:
            self.kill()
        
        self.true_x += self.x_speed
        self.true_y -= self.y_speed
        
        self.rect.x = self.true_x
        self.rect.y = self.true_y

    def on_collision(self, target):
        self.max_kills -= 1
        if self.max_kills == 0:
            self.kill()
        target.kill()
        print("You have slain an enemy")

    def blitme(self):
        """draws the bullet"""
        self.screen.blit(self.image, self.rect)


class Continuous(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, ship_rect: pygame.rect.Rect):
        super().__init__()
        self.rect = pygame.Rect(0,0, 3, 5)
        self.rect.centerx = ship_rect.centerx
        self.rect.y = ship_rect.y
        self.color = (140, 0, 70)
        self.screen = screen

    def update(self):
        self.rect.height += 3
        self.rect.top -= 3

    def blitme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
