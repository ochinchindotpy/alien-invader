import pygame
import assets as il
from enemies import Alien

class Upgrade(pygame.sprite.Sprite):
    # todo: upgrades to the player's ship
    
    def __init__(self, screen, settings, alien: Alien, rarity, category, stat):
        super().__init__()
        self.image = il.image_load("images/upgrade_temp.png")
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.rect.x = alien.rect.x
        self.rect.y = alien.rect.y
        self.info = [rarity, category, stat]

    def update(self):
        self.rect.y += 2
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def on_collision(self, ship):
        if bool(pygame.sprite.collide_rect(self, ship)):
            print(self.info)