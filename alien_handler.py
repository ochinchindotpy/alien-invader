import pygame
from enemies import Alien
from random import randint

#alien_handler.py
class EnemyHandler:
    """Enemy handler, Spawns aliens and updates all of them"""

    def __init__(self, screen, settings, difficult_manager):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.dm = difficult_manager
    
        self.alien_group = pygame.sprite.Group()
        self.dead_aliens: list = []

        self.spawn_delay = self.dm.spawn_info["base_delay"] # 120 by default

        self.timer = 0.0 # frames

    def update(self, ship):
        """Updates all aliens"""
        self.dead_aliens = []
        self.timer += 1.2 # - len(self.alien_group)/10

        for alien in self.alien_group:
            alien.update()
            
            if alien.rect.y > self.settings.screen_height:
                alien.kill()
                continue

            self.kill_aliens(alien, ship.weapon.bullets)
            self.kill_ship(alien, ship)


        if self.timer > self.spawn_delay:
            self.spawn_alien()

    def kill_aliens(self, alien, bullet_group):
        """Asks an alien if they got shot"""
        if alien.check_death(bullet_group):
            alien.kill()
            self.dead_aliens.append(alien)

    def kill_ship(self, alien, ship):
        """Asks an alien if they have collided with the player"""
        if alien.check_kill(ship):
            ship.dead = 1
            print("You lost and aliens successfully invaded earth")

    def spawn_alien(self):  # difficult related
        """Spawns aliens based on DifficultManager info"""
        min_spawn = self.dm.get_spawn_info("spawner_min")
        max_spawn = self.dm.get_spawn_info("spawner_max")

        for i in range(randint(min_spawn, max_spawn)):
            self.alien_group.add(Alien(self.screen, self.settings, self.dm, offset_y=randint(-30, 30)))


        self.timer -= self.spawn_delay

        self.spawn_delay = self.dm.spawn_info["base_delay"] # 120 by default
        min_delay = self.spawn_delay - self.dm.get_spawn_info("delay_offset_p") # at least 90 by default
        max_delay = self.spawn_delay + self.dm.get_spawn_info("delay_offset_n") # at most 120 by default

        self.spawn_delay = randint(min_delay, max_delay) * self.dm.difficult
    

