import pygame
from enemies import Alien
from random import randint
from difficult import DifficultManager

#alien_handler.py
class EnemyHandler:
    """Enemy handler, Spawns aliens and updates all of them"""

    def __init__(self, screen, settings, difficult_manager: DifficultManager):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.dm = difficult_manager

        self.alien_group = pygame.sprite.Group()
        
        self.spawn_delay = self.dm.spawn_info["base_delay"] # 120 by default

        self.timer = 0.0 # frames

    def update(self):
        """Updates all aliens"""
        
        self.timer += 1.2 # - len(self.alien_group)/10

        for alien in self.alien_group:
            alien.update()
            if alien.rect.y > self.settings.screen_height:
                alien.kill()

        if self.timer > self.spawn_delay:
            self.spawn_alien()

    def kill_aliens(self, bullet_group):
        """Asks each ship if they got shot"""
        for alien in self.alien_group:
            if alien.check_death(bullet_group):
                alien.kill()

    def kill_ship(self, ship):
        """Asks each ship if they have collided with the player"""
        for alien in self.alien_group:
            if alien.check_kill(ship):
                ship.dead = 1
                print("You lost and aliens successfully invaded earth")
                break

    def spawn_alien(self):  # difficult related
        """Spawns aliens based on DifficultManager info"""
        min = self.dm.get_spawn_info("spawner_min")
        max = self.dm.get_spawn_info("spawner_max")

        for i in range(randint(min, max)):
            self.alien_group.add(Alien(self.screen, self.settings, self.dm, offset_y=randint(-30, 30)))
        
        self.timer -= self.spawn_delay
        self.spawn_delay = randint(90, 150) * self.dm.difficult
    

