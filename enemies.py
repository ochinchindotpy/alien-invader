import random
import pygame
import image_loader as il

#alien.py
class Alien(pygame.sprite.Sprite):
    def __init__(self, screen, settings, offset_x=0, offset_y=0):
        super(Alien, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(il.resource_path("images/enemy.png"))
        self.speed = 1 + sum(random.randint(0, 2) for _ in range(5))
        self.collided = False

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.x = random.randint(50, settings.screen_width) - offset_x
        self.rect.y = self.screen_rect.top - 50 - offset_y
        
        
    def update(self):
        """Update enemy, should be called by the enemy handler"""

        self.rect.y += self.speed

    def attack(self):
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
