import pygame
from bullet import LaserBullet
import random
import math

class Weapon:
    """Base class for other SubWeapons"""
    # todo: ship should use a child of this class 
    # every time the ship shoots, it calls ship.weapon.attack()
    # weapon.attack() should return a respective Bullet class 
    modifiers = {
        "bullet_delay": {"collected": 0, "variation": -5*60},
        "max_bullets": {"collected": 0, "variation": 1},
        "bullet_speed": {"collected": 0, "variation": 1.5}
    }


    def __init__(self, settings):
        self.fire_speed = settings.fire_speed
   
    def attack(self, ship):
        """Every"""
        if not self.validate_attack():
            return
        
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
        if stat not in self.modifiers.keys:
            raise ValueError("Tried to modify a stat that does not exist")
        setattr(self, stat, getattr(self, stat) + change)

class LaserWeapon(Weapon):
    def __init__(self, settings):
        self.bullets = pygame.sprite.Group()
        self.max_bullets = 3
        self.bullet_speed = 5
        self.bullet_delay_current = settings.fire_speed
        self.bullet_delay = settings.fire_speed
        self.bullet_timer = 0
        self.timer = 0

    def _do_attack(self, ship):
        self.bullets.add(LaserBullet(ship.screen, ship.rect, ship.speed*ship.moving, self.bullet_speed))
    
    def __str__(self):
        return "Laser Weapon"


class SpreadWeapon(Weapon):
    def __init__(self, settings):
        self.bullets = pygame.sprite.Group()
        self.max_bullets = 20
        self.bullets_per_attack = 3
        self.bullet_speed = 5
        self.bullet_delay_current = settings.fire_speed * 1.5
        self.bullet_delay = settings.fire_speed * 1.5
        self.bullet_timer = 0
        self.timer = 0
        
    def _do_attack(self, ship):
        angles = 60 / self.bullets_per_attack

        for i in range(self.bullets_per_attack):
            angle = angles*(i-1) + random.randint(-7, 7)
            angle_rad = math.radians(angle)
            x_speed = self.bullet_speed * math.sin(angle_rad)
            y_speed = self.bullet_speed * math.cos(angle_rad)
            print(f"x = {x_speed}, y = {y_speed}, angle = {angle}, angle_rad = {angle_rad}")
            
            self.bullets.add(LaserBullet(ship.screen, ship.rect, x_speed, y_speed))

    def __str__(self):
        return "Spread Weapon"

class ContinuousWeapon(Weapon):
    def __init__(self, settings):
        self.bullets = pygame.sprite.Group()
        self.max_bullets = 20
        self.bullets_per_attack = 3
        self.bullet_speed = 5
        self.bullet_delay_current = settings.fire_speed * 1.5
        self.bullet_delay = settings.fire_speed * 1.5
        self.bullet_timer = 0 # no
        self.timer = 0 # no
        self._first_press = False
        self.ship = None
        self.is_attacking = False

    def attack(self, ship):
        if self.ship is None:
            print("x")
            self.ship = ship

    def update(self, dt):
        if self.ship is None:
            return
        if self.is_attacking:
            self.bullets.add(LaserBullet(self.ship.screen, self.ship.rect, 0, 10))

