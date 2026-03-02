import pygame
from settings import Settings
import game_functions as gf
from ship import Ship   
from controller import Controller
from alien_handler import EnemyHandler
from difficult import DifficultManager
from upgrade_manager import UpgradeManager
from debugging import Debug
from weapons import LaserWeapon, SpreadWeapon, ContinuousWeapon
from score import Score
#from menu import Menu

# game.py
class GameWorld:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        pygame.display.set_caption("Alien Invasion")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.fps = pygame.time.Clock()
        self.weapon =  LaserWeapon(self.settings)
        self.ship = Ship(self.screen, self.settings, self.weapon)
        self.control = Controller(self.ship, self.settings)
        self.ship.player = self.control
        self.difficult = DifficultManager(self.settings)
        self.enemy_handler = EnemyHandler(self.screen, self.settings, self.difficult)
        self.upgrade_manager = UpgradeManager(self.screen, self.settings, self.enemy_handler, self)
        self.debug = Debug(self.screen, True)
        self.score = Score(self)

        self._estado = "menu"
        #self.menu = Menu(self)


    def play(self):
        """Main loop"""
        
        while True:
        #if self._estado == "menu":
        #    self.menu.play()
        #    print(self._estado)
        #    return

            self.fps.tick(60)
            dt = self.fps.get_time()

            gf.check_events(self.debug)

            # keyboard listener
            self.control.handle_input()
            # updates if player has not died
            gf.update_logic(self.ship, self.difficult, self.enemy_handler, self.upgrade_manager, self.score, dt)

            self.debug.set_lines(
            #    f"ship speed: {(ship.speed + ship.speed_both) * ship.moving * ship.speed_percentage}",
            #    f"attack speed: {ship.bullet_delay_current}",
            #    f"extra life: {ship.extra_life}"
            #    f"Holding: {self.ship.weapon}",
            #    f"Bullet delay: {self.ship.weapon.fire_speed}"
            #    f"max bullets: {self.ship.weapon.max_bullets}"
            #    f"bullet speed: {self.ship.weapon.bullet_speed}"
            #    f"Can change? {ship.timer > 10000}",
            #    f"{"Press F2 to change weapon" if ship.timer > 10000 else ""}",
            #    f"timer = {ship.weapon.bullet_timer}"
                f"score: {self.score}"
            )
            
            # plays explosion animation if player died 
            self.ship.die()
            
            # render everything
            gf.update_screen(self.settings, self.screen, self.ship, self.enemy_handler.alien_group, self.upgrade_manager.upgrades_in_screen, self.debug) 
        
