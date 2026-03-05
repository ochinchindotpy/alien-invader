import random
import pygame
import assets as il
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from difficult import DifficultManager
    from settings import Settings
    from ship import Ship


#alien.py
class Alien(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.surface.Surface, settings: "Settings", speed, offset_x=0, offset_y=0, has_dash=False):
        super(Alien, self).__init__()
        self.screen = screen
        has_dash = settings.enemies_have_dash # temp

        self.image = il.image_load("images/enemy.png")
        if has_dash:
            self.image = il.image_load("images/enemy_with_attack.png")
        
        
        self.has_dash = has_dash
        self.attack_range = int(self.screen.get_width()*0.4)

        # speed_info
        self.speed = speed

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.x = random.randint(50, settings.screen_width) - offset_x
        self.rect.y = self.screen_rect.top - 50 - offset_y
        
    def update(self):
        """Update enemy, should be called by the enemy handler"""
        self.rect.y += self.speed

    def attack(self, ship: "Ship"):
        if not self.has_dash:
            return
        
        will_hit = 50 > abs(ship.rect.x - self.rect.x)
        close_enough = self.rect.y > self.attack_range

        if will_hit and close_enough:
            self.speed = max(7, self.speed*2)
            self.has_dash = False

    def check_death(self, bullet_group) -> list:
        hits = pygame.sprite.spritecollide(self, bullet_group, False)
        return hits

    def check_kill(self, ship) -> bool:
        return pygame.sprite.collide_rect(self, ship)
            
    def blitme(self):
        """Draws the enemy"""
        self.screen.blit(self.image, self.rect)
