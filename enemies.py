import random
import pygame
import assets as il

#alien.py
class Alien(pygame.sprite.Sprite):
    def __init__(self, screen, settings, dm, offset_x=0, offset_y=0, has_dash=False):
        super(Alien, self).__init__()
        self.screen = screen
        
        self.image = il.image_load("images/enemy.png")
        if has_dash:
            self.image = il.image_load("images/enemy_with_attack.png")

        self.has_dash = has_dash

        # speed_info
        min_speed = dm.get_speed_info("min_roll")
        max_speed = dm.get_speed_info("max_roll")
        constant = dm.get_speed_info("constant")
        roll = dm.get_speed_info("rolls_quantity")

        self.speed = constant + sum(random.randint(min_speed, max_speed) for _ in range(roll)) # difficult related

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.x = random.randint(50, settings.screen_width) - offset_x
        self.rect.y = self.screen_rect.top - 50 - offset_y
        
        
    def update(self):
        """Update enemy, should be called by the enemy handler"""

        self.rect.y += self.speed

    def attack(self): #difficult related
        # not sure if i will work on this
        ...

    def check_death(self, bullet_group) -> bool:
        hits = pygame.sprite.spritecollide(self, bullet_group, True)
        return bool(hits)


    def check_kill(self, ship) -> bool:
        return pygame.sprite.collide_rect(self, ship)
            
    def blitme(self):
        """Draws the enemy"""
        self.screen.blit(self.image, self.rect)
