import pygame
from bullet import Bullet, Continuous
import random
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings import Settings


class Weapon:
    """Base class for other SubWeapons
    Ship has an instance of a subclass of this class"""
    modifiers = { # todo: work on this
        "bullet_delay": {"collected": 0, "variation": -5*60},
        "max_bullets": {"collected": 0, "variation": 1},
        "bullet_speed": {"collected": 0, "variation": 1.5},
        "max_kills": {"collected": 0, "variation": 1}
    }

    bullets = pygame.sprite.Group()

    def __init__(self, settings):
        self.fire_speed = settings.fire_speed
   
    def attack(self, ship):
        """Basic implementation of attack. Subclass just need to change their own _do_attack"""
        if not self.validate_attack():
            return
        
        print("shooting")
        self.update_before_attack(ship)
        
        self._do_attack(ship)

        self.update_after_attack(ship)

    def _do_attack(self, ship):
        raise NotImplemented("Weapon is a base class, do not try to attack with it")

    def update(self, dt):
        self.bullet_timer += dt

    def update_before_attack(self, ship):
        if ship.slow_move:
            ship.moving = 0

    def update_after_attack(self, ship):
        self.bullet_timer = 0

    def validate_attack(self):
        if self.bullet_delay > self.bullet_timer: # don't shoot if not ready
            return False
        if len(self.bullets) >= self.max_bullets:
            return False
        return True

    def upgrade(self, stat, change):
        if stat not in self.modifiers.keys():
            raise ValueError("Tried to modify a stat that does not exist")
        setattr(self, stat, getattr(self, stat) + change)

    def _reset_stat(self, settings: "Settings", weapon):
        data = settings.get_weapon_settings(weapon)
        for stat, value in data.items():
            setattr(self, stat, value)
        
        self.bullet_timer = 0
        self.timer = 0
        self.max_kills = 1



class LaserWeapon(Weapon):
    def __init__(self, settings):
        self._reset_stat(settings, str(self))

    def _do_attack(self, ship):
        self.bullets.add(Bullet(ship.screen, ship.rect, ship.speed*ship.moving, self.bullet_speed, self.max_kills))
    
    def __str__(self):
        return "Laser Weapon"


class SpreadWeapon(Weapon):
    def __init__(self, settings):
        self._reset_stat(settings, str(self))

    def update_before_attack(self, ship):
        super().update_before_attack(ship)
        if ship.slow_move:
            self.rng = self.rng_slow_mode
        else:
            self.rng = self.rng_angle


    def _do_attack(self, ship):
        angles = 120 / self.bullets_per_attack
        rng = (-self.rng, self.rng)

        for i in range(self.bullets_per_attack):
            angle = angles*(i-1) + random.randint(*rng)
            angle_rad = math.radians(angle)
            x_speed = ship.speed * ship.moving + self.bullet_speed * math.sin(angle_rad)
            y_speed = self.bullet_speed * math.cos(angle_rad)
            print(f"x = {x_speed}, y = {y_speed}, angle = {angle}, angle_rad = {angle_rad}")
            
            self.bullets.add(Bullet(ship.screen, ship.rect, x_speed, y_speed))

    def update_after_attack(self, ship):
        super().update_after_attack(ship)
        self.rng = self.rng_angle

    def __str__(self):
        return "Spread Weapon"
    

class ContinuousWeapon(Weapon):
    # once you attack, you get into attacking mode
    # in attacking mode, you shoot a single laser
    # that laser takes time to kill, like 1s of shooting
    # you can't move while in attacking mode
    # you need to wait 0.5s to get out of attack mode
    def __init__(self, settings):
        self.max_bullets = 1
        self.bullet_speed = 5
        self.bullet_delay_current = 500
        self.bullet_delay = 500
        self.bullet_timer = 0 # no
        self.timer = 0 # no
        self._first_press = False
        self.is_attacking = False

    def _do_attack(self, ship):
        self.is_attacking = not self.is_attacking
        if self.is_attacking:
            self.bullets.add(Continuous(ship.screen, ship.rect))
        self.ship = ship

    def validate_attack(self):
        if self.is_attacking and self.bullet_timer > 500:
            return True
        return super().validate_attack()

    def update_before_attack(self, ship):
        super().update_before_attack(ship)


    def update(self, dt):
        super().update(dt)
        if self.is_attacking:
            self.ship.moving = 0
