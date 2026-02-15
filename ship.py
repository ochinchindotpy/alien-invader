import pygame
from bullet import Bullet
import image_loader as il


#ship.py
class Ship(pygame.sprite.Sprite):
    moving = 0
    bullets = pygame.sprite.Group()
    player = None

    def __init__(self, screen: pygame.Surface, settings):
        super().__init__()
        self.dead = -1
        self.screen = screen
        self.image = pygame.image.load(il.resource_path("images/ship.png"))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.bullet_delay = settings.fire_speed
        self._bullet_delay_default = settings.fire_speed
        self.speed_default = settings.ship_speed
        self.shift_speed_default = settings.ship_speed_shift
        self.slow_move = False
        self._animation = [pygame.image.load(il.resource_path(f"images/ship_explosion_{i}.png")) for i in range(1, 8)]

    def validate_position(self):
        """Invert your moviment if you try to move out of the screen"""
        if self.rect.right + self.speed * self.moving > self.screen_rect.width:
            self.moving = -1

        elif self.rect.left + self.speed * self.moving < 0:
            self.moving = 1

    def update(self):
        """Checks if you can move and updates your position"""
        self.bullet_delay -= 1
        self.validate_position()

        self.rect.centerx += self.speed * self.moving

    def shoot(self):
        """Shoots a bull"""
        if self.slow_move:
            self.moving = 0
        if len(self.bullets) < 4:
            self.bullets.add(Bullet(self.screen, self.rect, self.speed*self.moving))

    def die(self):
        if self.dead >= 0 and self.dead < 8:
            print(len(self._animation))
            print(self._animation)
            self.image = self._animation[self.dead-1]
            self.dead += 1
            print(self.dead)
            

    def blitme(self):
        """Draws the ship"""
        
        self.screen.blit(self.image, self.rect)

