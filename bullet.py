import pygame
import image_loader as il
#bullet.py
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, ship_rect, x_speed):
        super().__init__()

        self.screen = screen
        self.image = pygame.image.load(il.resource_path("images/bullet.png"))
        self.rect = self.image.get_rect()

        self.x_speed = x_speed

        self.rect.centerx = ship_rect.centerx
        self.rect.bottom = ship_rect.top
    
    def update(self):
        """Updates bullet's state, removes bullet and moves it"""
        if 0 > self.rect.bottom:
            self.kill()
        self.rect.y -= 5
        self.rect.x += self.x_speed

    def blitme(self):
        """draws the bullet"""
        self.screen.blit(self.image, self.rect)
