import pygame
import assets as il

#ship.py
class Ship(pygame.sprite.Sprite):
    moving = 0
    player = None

    def __init__(self, screen: pygame.Surface, settings, weapon):
        super().__init__()
        self.dead = -1
        self.weapon = weapon
        self.timer = 0

        # render info
        self.screen = screen
        self.image = il.image_load("images\ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.position_x = self.screen_rect.centerx
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self._animation = [il.image_load(f"images/ship_explosion_{i}.png") for i in range(1, 8)]

        # to be removed
        self.bullet_delay_current = 0
        self.bullet_delay = 0
        self.bullet_timer = 0
        self.max_bullets = 3
        self.bullet_speed = 5

        # upgradeable
        self.speed_percentage = 1
        self.speed_both = 0
        
        self.speed: int = 0
        self.speed_default = settings.ship_speed
        self.shift_speed_default = settings.ship_speed_shift

        self.control_ability = None
        self.tab_ability = None
        self.shift_ability = ...
        self.upgrades = {}

        self.more_upgrades = 0 # remove
        self.slow_move = False
        self.extra_life = False
        
        self.previous = 0
        self.current = 0
        self.diff = 0

    def validate_position(self):
        """Invert your moviment if you try to move out of the screen"""
        if self.rect.right + self.speed * self.moving > self.screen_rect.width:
            self.moving = -1

        elif self.rect.left + self.speed * self.moving < 0:
            self.moving = 1

    def update(self, dt):
        """Checks if you can move and updates your position"""
        self.weapon.update(dt)
        self.validate_position()
        
        self.position_x += (self.speed + self.speed_both) * self.moving * self.speed_percentage
        self.previous = int(self.rect.centerx)
        self.rect.centerx = self.position_x #  (self.speed + self.speed_both) * self.moving * self.speed_percentage
        self.current = int(self.rect.centerx)
        self.diff = int(self.current) - int(self.previous)
        
        self.timer += dt
        if self.timer > 10000: # temporary solution for changing weapon
            self.player.changed = False


    def shoot(self):
        """Shoots a bullet"""
        self.weapon.attack(self)

    def die(self):
        if self.dead >= 0 and self.dead < 8:
            self.image = self._animation[self.dead-1]
            self.dead += 1

    def upgrade(self, stat, change):
        setattr(self, stat, getattr(self, stat) + change)
        if stat not in self.upgrades:
            self.upgrades[stat] = 1
        else:
            self.upgrades[stat] += 1

    def blitme(self):
        """Draws the ship"""
        
        self.screen.blit(self.image, self.rect)

