import pygame
import assets as il
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enemies import Alien


class Upgrade(pygame.sprite.Sprite):
        
    def __init__(self, screen, settings, alien: "Alien", target, rarity, category, upgrade_key, upgrade_item):
        super().__init__()
        self.image = il.image_load("images/upgrade_temp.png")
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
    
        self.settings = settings
        self.rect.x = alien.rect.x
        self.rect.y = alien.rect.y
        
        self.target = target
        self.rarity = rarity
        self.category = category
        self.upgrade_key = upgrade_key
        self.upgrade_item = upgrade_item

    def update(self):
        self.rect.y += 2
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def on_collision(self, ship): # todo: remember to change um._spawn()        
        if pygame.sprite.collide_rect(self, ship):
            self.target.upgrade(self.upgrade_key, self.upgrade_item["value"])
            self.kill()
