import sys
import pygame
from typing import Callable
from assets import image_load


class Button:
    def __init__(self, screen: pygame.Surface, text: str, position: tuple[int, int], effect: Callable | None = None, *args, **kwargs):
        self.screen = screen
        self.on_press = effect
        self.args = args
        self.kwargs = kwargs
        self.pressed = False
        self.hold = False
        self.text = text
        self.current_image = 0
        images = [image_load("menus/button.png").convert_alpha(),
                  image_load("menus/button_hover.png").convert_alpha()]

        self.squares = []
        self.rect = images[0].get_rect(center=position)
        font = pygame.font.Font(None, 32)
        font_render = font.render(self.text, True, (255, 255, 255))

        for image in images:
            square = image
            self.square = square.copy()
            font_rect = font_render.get_rect(center=self.square.get_rect().center)
            self.square.blit(font_render, font_rect)
            self.squares.append(self.square)
            
        self.square = self.squares[0]


    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self.pressed = pygame.mouse.get_pressed()[0]
        
        if not self.rect.collidepoint(mouse_pos):
            self.change_image(0)
            return
        
        self.change_image(1)
        
        if not self.pressed or not self.on_press:
            return
        
        self.on_press(self, *self.args, **self.kwargs)
        
    def change_image(self, image):
        if self.current_image == image:
            return
        self.square = self.squares[image]

        self.current_image = image


    def blitme(self):
        self.screen.blit(self.square, self.rect)
        
    def test(self):
        print("wow")


def leave_button(self: Button, *args, **kwargs):
    sys.exit("bye")


def options_button(self: Button, *args, **kwargs):
    print("Not implemented")

def play_button(self: Button, *args, **kwargs):
    menu = kwargs.get("menu", None)
    menu.state = "play"
