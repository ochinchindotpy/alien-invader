import pygame


#controller.py
class Controller:
    def __init__(self, ship):
        self.ship = ship

        self.actions = {
            pygame.K_s: self.stop,
            pygame.K_d: self.move_right,
            pygame.K_a: self.move_left,
            pygame.K_SPACE: self.attack,
        }

    def handle_input(self):
        """Handles all inputs"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.ship.speed = self.ship._shift_speed_default
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
        if self.ship.bullet_delay > 0: # don't shoot if not ready
            return
        self.ship.shoot()
        self.ship.bullet_delay = self.ship._bullet_delay_default


    def stop(self):
        self.ship.moving = 0
