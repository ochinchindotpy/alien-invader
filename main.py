import pygame
from settings import Settings
from ship import Ship   
import game_functions as gf
from controller import Controller
from alien_handler import EnemyHandler

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
    enemy_handler = EnemyHandler(screen, settings)
    i = 0

    while True:
        fps.tick(60)
        #print(fps.get_fps())

        gf.check_events(ship)
        
        # keyboard listener
        control.handle_input()
        
        # updates
        if ship.dead == -1:
            ship.update()
            ship.bullets.update()
            enemy_handler.kill_aliens(ship.bullets)
            enemy_handler.kill_ship(ship)
            enemy_handler.update()

        ship.die()

        gf.update_screen(settings, screen, ship, enemy_handler.alien_group) # render everything
        

if __name__ == "__main__":
    run_game()
