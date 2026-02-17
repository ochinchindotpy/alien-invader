import pygame
from bullet import Bullet
import assets as il


#ship.py
class Ship(pygame.sprite.Sprite):
    moving = 0
    bullets = pygame.sprite.Group()
    player = None

    def __init__(self, screen: pygame.Surface, settings):
        super().__init__()
        self.dead = -1
        
        # render info
        self.screen = screen
        self.image = il.image_load("images\ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self._animation = [il.image_load(f"images/ship_explosion_{i}.png") for i in range(1, 8)]

        # upgradeable
    
        self.bullet_delay_current = settings.fire_speed
        self.bullet_delay = settings.fire_speed
        self.bullet_timer = 0
        self.max_bullets = 3
        self.bullet_speed = 5

        self.speed_percentage = 1
        self.speed_both = 0
        self.speed_default = settings.ship_speed
        self.shift_speed_default = settings.ship_speed_shift

        self.control_ability = None
        self.tab_ability = None
        self.shift_ability = ...


        self.more_upgrades = 0 # remove
        self.slow_move = False
        self.extra_life = False

    def validate_position(self):
        """Invert your moviment if you try to move out of the screen"""
        if self.rect.right + self.speed * self.moving > self.screen_rect.width:
            self.moving = -1

        elif self.rect.left + self.speed * self.moving < 0:
            self.moving = 1

    def update(self, dt):
        """Checks if you can move and updates your position"""
        self.bullet_timer += dt
        self.validate_position()

        # bug: for some reason, sometimes (after getting speed_default) it feels like it's faster to move right than left
        self.rect.centerx += (self.speed + self.speed_both) * self.moving * self.speed_percentage

    def shoot(self):
        """Shoots a bullet"""
        if self.slow_move:
            self.moving = 0
        if len(self.bullets) <= self.max_bullets:
            self.bullets.add(Bullet(self.screen, self.rect, self.speed*self.moving, self.bullet_speed))
            self.bullet_timer = 0

    def die(self):
        if self.dead >= 0 and self.dead < 8:
            self.image = self._animation[self.dead-1]
            self.dead += 1

    def upgrade(self, stat, change):
        setattr(self, stat, getattr(self, stat) + change)

    def blitme(self):
        """Draws the ship"""
        
        self.screen.blit(self.image, self.rect)

