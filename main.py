import pygame
from settings import Settings
import game_functions as gf
from ship import Ship   
from controller import Controller
from alien_handler import EnemyHandler
from difficult import DifficultManager
from upgrade_manager import UpgradeManager

#main.py
def run_game():
    pygame.init()
    settings = Settings()
    pygame.display.set_caption("Alien Invasion")
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    fps = pygame.time.Clock()
    ship = Ship(screen, settings)
    control = Controller(ship)
    ship.player = control
    difficult = DifficultManager(settings)
    enemy_handler = EnemyHandler(screen, settings, difficult)
    upgrade_manager = UpgradeManager(screen, settings, enemy_handler)

    while True:
        fps.tick(60)
        #print(fps.get_fps())
        dt = fps.get_time()

        gf.check_events(ship)
        
        # keyboard listener
        control.handle_input()
        
        # updates, if player died
        if ship.dead == -1:
            ship.update(dt)
            ship.bullets.update()
            difficult.update(dt)
            enemy_handler.update(ship)
            #upgrade_manager.update(dt, ship)

        ship.die()

        # render everything
        gf.update_screen(settings, screen, ship, enemy_handler.alien_group, upgrade_manager.upgrades_in_screen) 

if __name__ == "__main__":
    run_game()
