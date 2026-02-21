import pygame
import weapons as w

#controller.py
class Controller:
    def __init__(self, ship, settings):
        self.ship = ship
        self.changed = True
        self.actions = {
            pygame.K_s: self.stop,
            pygame.K_d: self.move_right,
            pygame.K_a: self.move_left,
            pygame.K_SPACE: self.attack,
            pygame.K_F2: self.change
        }
        self.settings = settings

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
                action()


    def move_right(self):
        self.ship.moving = 1 

    def move_left(self):
        self.ship.moving = -1

    def attack(self):
        #if self.ship.bullet_delay > self.ship.bullet_timer: # don't shoot if not ready
        #    return
        #self.ship.shoot()
        #self.ship.bullet_delay_current = self.ship.bullet_delay

        self.ship.shoot()

    def stop(self):
        self.ship.moving = 0

    def change(self): # temporary solution for changing weapon
        if self.changed:
            return

        if type(self.ship.weapon) == w.LaserWeapon:
            self.ship.weapon = w.SpreadWeapon(self.settings)
            print(type(self.ship.weapon))
        else:
            self.ship.weapon = w.LaserWeapon(self.settings)
            print(type(self.ship.weapon))
        self.changed = True
        self.ship.timer = 0