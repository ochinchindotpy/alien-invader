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

#main.py
def run_game():
    pygame.init()
    settings = Settings()
    pygame.display.set_caption("Alien Invasion")
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    fps = pygame.time.Clock()
    weapon =  ContinuousWeapon(settings)
    ship = Ship(screen, settings, weapon)
    control = Controller(ship, settings)
    ship.player = control
    difficult = DifficultManager(settings)
    enemy_handler = EnemyHandler(screen, settings, difficult)
    upgrade_manager = UpgradeManager(screen, settings, enemy_handler)
    debug = Debug(screen, True)

    while True:
        fps.tick(60)
        #print(fps.get_fps())
        dt = fps.get_time()

        gf.check_events(debug)



        # keyboard listener
        control.handle_input()
        # updates if player has not died
        gf.update_logic(ship,
                        difficult,
                        enemy_handler,
                        upgrade_manager, 
                        dt)

        debug.set_lines(
        #    f"ship speed: {(ship.speed + ship.speed_both) * ship.moving * ship.speed_percentage}",
        #    f"attack speed: {ship.bullet_delay_current}",
        #    f"extra life: {ship.extra_life}"
        #     f"Holding: {ship.weapon}",
        #     f"Can change? {ship.timer > 10000}",
        #     f"{"Press F2 to change weapon" if ship.timer > 10000 else ""}",
            f"timer = {ship.weapon.bullet_timer}"
        )

        ship.die() # if player died plays explosion animation

        # render everything
        gf.update_screen(settings, screen, ship, enemy_handler.alien_group, upgrade_manager.upgrades_in_screen, debug) 

if __name__ == "__main__":
    run_game()
