import pygame
import assets as il
#bullet.py
class LaserBullet(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, ship_rect, x_speed, y_speed):
        super().__init__()

        self.screen = screen
        self.image = il.image_load("images/bullet.png")
        self.rect = self.image.get_rect()

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.rect.centerx = ship_rect.centerx
        self.rect.bottom = ship_rect.top

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

    def blitme(self):
        """draws the bullet"""
        self.screen.blit(self.image, self.rect)


class Continuous(pygame.sprite.Sprite):
    def __init__(self, screen, ship_rect):
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