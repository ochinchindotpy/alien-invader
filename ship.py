import pygame
import assets as il
from typing import TYPE_CHECKING
from ability.teleport import Teleport
from ability.dash import Dash


if TYPE_CHECKING:
    from weapons import Weapon 
    from controller import Controller
    

#ship.py
class Ship(pygame.sprite.Sprite):
    moving = 0
    player: "Controller" = ...

    def __init__(self, screen: pygame.Surface, settings, weapon: "Weapon"):
        super().__init__()
        self.dead = -1
        self.weapon = weapon
        self.timer = 0

        # render info
        self.screen = screen
        self.image = il.image_load(r"images\ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.position_x = self.screen_rect.centerx
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self._animation = [il.image_load(f"images/ship_explosion_{i}.png") for i in range(1, 8)]

        # upgradeable
        self.speed_percentage = 1
        self.speed_both = 0
        
        self.speed_default = settings.ship_speed
        self.shift_speed_default = settings.ship_speed_shift

        self.control_ability = Teleport(self)
        self.tab_ability = None
        self.shift_ability = ...
        self.upgrades = {}

        self.slow_move = False
        self.extra_life = False
        self.invencible = False
        self._invecible_timer = 0
        


    @property
    def speed(self):
        base = self.shift_speed_default if self.slow_move else self.speed_default
        base += self.speed_both
        base *= self.speed_percentage
        base *= self.moving
        return base

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
        
        self.position_x += self.speed #(self.speed + self.speed_both) * self.moving * self.speed_percentage
        self.previous = int(self.rect.centerx)
        self.rect.centerx = self.position_x #  (self.speed + self.speed_both) * self.moving * self.speed_percentage
        self.current = int(self.rect.centerx)
        self.diff = int(self.current) - int(self.previous)
        
        self.update_invencible(dt)

        self.control_ability.update(dt)

        self.timer += dt
        if self.timer > 2000: # temporary solution for changing weapon
            self.player.changed = False

    def shoot(self):
        """Shoots a bullet"""
        self.weapon.attack(self)

    def death_animation(self):
        """Plays death animation"""
        if self.dead == -1 or self.dead > 6:
            return
        self.image = self._animation[self.dead]
        self.dead += 1
        

    def take_hit(self):
        """Kills ship"""

        if self.invencible:
            return
        
        if bool(self.extra_life):
            self.extra_life = False
            self.invencible = True
            self._invecible_timer = 0
            return

        self.dead = 0
        print("You lost and aliens successfully invaded earth")

    def update_invencible(self, dt):
        if not self.invencible:
            return
        self._invecible_timer += dt
        if self._invecible_timer > 5000:
            self.invencible = False

    def upgrade(self, stat, change):
        """Should be called by Upgrade to change stats"""
        setattr(self, stat, getattr(self, stat) + change)
        if stat not in self.upgrades:
            self.upgrades[stat] = 1
        else:
            self.upgrades[stat] += 1

    def blitme(self):
        """Draws the ship"""
        self.screen.blit(self.image, self.rect)

