import pygame
from enemies import Alien
from random import randint

#alien_handler.py
class EnemyHandler:
    """Enemy handler, Spawns aliens and updates all of them"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.alien_group = pygame.sprite.Group()
        
        self.spawn_delay = 120 # frames
        self.timer = 0.0 # frames

    def update(self):
        """Updates all aliens"""
        
        self.timer += 1.2 - len(self.alien_group)/10
        for alien in self.alien_group:
            alien.update()
            if alien.rect.y > self.settings.screen_height:
                alien.kill()

        if self.timer > self.spawn_delay:
            self.spawn_alien()

    def kill_aliens(self, bullet_group):
        """Ask each ship if they got shot"""
        for alien in self.alien_group:
            if alien.check_death(bullet_group):
                alien.kill()

    def kill_ship(self, ship):
        """Ask if any ship has collided with the player"""
        for alien in self.alien_group:
            if alien.check_kill(ship):
                ship.dead = 1
                print("You lost and aliens successfully invaded earth")
                
                break

    def spawn_alien(self, min=1, max=3):
        """Spawns up to 3 aliens"""
        for i in range(randint(min, max)):
            self.alien_group.add(Alien(self.screen, self.settings, offset_y=randint(-30, 30)))

        self.timer -= self.spawn_delay
        self.spawn_delay = randint(90, 150) * self.settings.difficult
    

