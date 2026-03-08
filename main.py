import pygame

from game import GameWorld
from menu import Menu

if __name__ == "__main__":
    pygame.init()
    a = GameWorld()
    b = Menu(a)
    while True:
        if b.state == "play":
            a.play()
        elif b.state == "menu":
            b.play()
