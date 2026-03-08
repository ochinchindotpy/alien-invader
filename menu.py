import game_functions as gf
import pygame
from button import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameWorld


color = (255, 0, 255)

class Menu:
    def __init__(self, world: "GameWorld"):
        self.world = world
        self.screen = world.screen
        self.font = pygame.font.Font(None, 32)
        self.state = "menu"

        start_position = (self.screen.get_width()/2, 250)
        self.start_button = Button(self.screen, "PLAY", start_position, play_button, menu=self)
        
        options_position = (self.screen.get_width()/2, 450)
        self.option_button = Button(self.screen, "OPTIONS (wip)", options_position, options_button)
        


        quit_position = (self.screen.get_width()/2, 650)
        self.quit_button = Button(self.screen, "EXIT", quit_position, leave_button)
        self.bg = (0, 0, 0)

    def play(self):
        
        #pygame.init()
        self.world.fps.tick(10)
        gf.check_events()

        self.start_button.update()
        self.option_button.update()
        self.quit_button.update()
        
        self.screen.fill(self.bg)
        
        self.start_button.blitme()
        self.option_button.blitme()
        self.quit_button.blitme()
        
        pygame.display.flip()


if __name__ == '__main__':
    from game import GameWorld
    pygame.init()
    world = GameWorld()
    menu = Menu(world)
    while True:
        menu.play()
