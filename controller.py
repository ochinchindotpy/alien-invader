import pygame
import weapons as w
from ship import Ship 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings import Settings

#controller.py
class Controller:
    def __init__(self, ship, settings: "Settings"):
        self.ship:Ship = ship
        self.changed = True
        self.actions = {
            pygame.K_s: self.stop,
            pygame.K_d: self.move_right,
            pygame.K_a: self.move_left,
            pygame.K_SPACE: self.attack,
            pygame.K_F2: self.change,
            pygame.K_1: self.enemies
        }
        self.settings = settings
        self.previous = {}

    def handle_input(self):
        """Handles all inputs"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.ship.speed = self.ship.shift_speed_default
            self.ship.slow_move = True
        else:
            self.ship.speed = self.ship.speed_default
            self.ship.slow_move = False

        for key, action in self.actions.items():
            if keys[key]:
                action(key)

        self.previous = keys

    def deny_hold(self, key):
        return self.previous[key]
        

    def move_right(self, key):
        self.ship.moving = 1 

    def move_left(self, key):
        self.ship.moving = -1

    def attack(self, key):
        if self.deny_hold(key):
            return
        self.ship.shoot()

    def stop(self, key):
        self.ship.moving = 0

    def change(self, key): # temporary solution for changing weapon
        if self.deny_hold(key):
            return

        if type(self.ship.weapon) == w.LaserWeapon:
            self.ship.weapon = w.SpreadWeapon(self.settings)
        else:
            self.ship.weapon = w.LaserWeapon(self.settings)

    def enemies(self, key):
        if self.deny_hold(key):
            return
        self.settings.enemies_have_dash = not self.settings.enemies_have_dash
        