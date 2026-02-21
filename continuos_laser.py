import pygame
class Laser(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen


    def blitme(self):
        self.screen.blit(self.image, self.rect)

