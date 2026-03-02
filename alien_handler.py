import pygame
from enemies import Alien
from random import randint

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ship import Ship
    from difficult import DifficultManager
    from bullet import Bullet
    from settings import Settings


#alien_handler.py
class EnemyHandler:
    """Enemy handler, Spawns aliens and updates all of them"""

    def __init__(self, screen: pygame.surface.Surface, settings: "Settings", difficult_manager):
        self.screen: pygame.surface.Surface = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.dm: "DifficultManager" = difficult_manager
    
        self.alien_group = pygame.sprite.Group()
        self.dead_aliens: list = []

        self.spawn_delay = self.dm.spawn_info["base_delay"] # 120 by default

        self.timer = 0 # frames

    def update(self, ship: "Ship"):
        """Updates all aliens"""
        self.dead_aliens = []
        self.timer += 1 # - len(self.alien_group)/10
        alien: Alien

        for alien in self.alien_group:
            alien.update()
            alien.attack(ship)

            if alien.rect.y > self.settings.screen_height:
                alien.kill()
                continue

            self.on_collision(alien, ship.weapon.bullets)
            self.kill_ship(alien, ship)
            self._update_dead_alien(alien)

        if self.timer > self.spawn_delay:
            self.spawn_alien()

    def on_collision(self, alien: Alien, bullet_group):
        """Asks an alien if they got shot"""
        hits = alien.check_death(bullet_group)
        bullet: "Bullet"
        for bullet in hits:
            bullet.on_collision(alien)

    def kill_ship(self, alien: Alien, ship: "Ship"):
        """Asks an alien if they have collided with the player"""
        if alien.check_kill(ship):
            ship.dead = 1
            print("You lost and aliens successfully invaded earth")

    def _update_dead_alien(self, alien: Alien):
        """Checks if alien died and add it to the list of dead_aliens"""
        if alien.alive():
            return
        self.dead_aliens.append(alien)

    def _generate_speed(self):
        min_speed = self.dm.get_speed_info("min_roll")
        max_speed = self.dm.get_speed_info("max_roll")
        constant = self.dm.get_speed_info("constant")
        roll = self.dm.get_speed_info("rolls_quantity")
        
        return constant + sum(randint(min_speed, max_speed) for _ in range(roll))

    def spawn_alien(self):
        """Spawns aliens based on DifficultManager info"""
        min_spawn = self.dm.get_spawn_info("spawner_min")
        max_spawn = self.dm.get_spawn_info("spawner_max")

        for _ in range(randint(min_spawn, max_spawn)):
            speed = self._generate_speed()
            self.alien_group.add(Alien(self.screen, self.settings, speed, offset_y=randint(-50, 50)))

        self.timer -= self.spawn_delay

        self.spawn_delay = self.dm.get_spawn_info("base_delay") # 120 by default
        min_delay = self.spawn_delay - self.dm.get_spawn_info("delay_offset_p") # at least 90 by default
        max_delay = self.spawn_delay + self.dm.get_spawn_info("delay_offset_n") # at most 120 by default

        self.spawn_delay = randint(min_delay, max_delay) / self.dm.difficult
    

