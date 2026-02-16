import pygame
from settings import Settings
from ship import Ship   
import game_functions as gf
from controller import Controller
from alien_handler import EnemyHandler
from difficult import DifficultManager

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

    while True:
        fps.tick(60)
        #print(fps.get_fps())
        dt = fps.get_time()
        gf.check_events(ship)
        
        # keyboard listener
        control.handle_input()
        
        # updates, if player died
        if ship.dead == -1:
            ship.update()
            ship.bullets.update()
            difficult.update(dt)
            enemy_handler.kill_aliens(ship.bullets)
            enemy_handler.kill_ship(ship)
            enemy_handler.update()
            

        ship.die()

        # render everything
        gf.update_screen(settings, screen, ship, enemy_handler.alien_group) 

if __name__ == "__main__":
    run_game()
