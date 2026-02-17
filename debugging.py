import pygame
import assets


class Debug:
    def __init__(self, screen, debug_mode=False):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.lines = []
        self.debug_mode = debug_mode

    def set_lines(self, *args):
        self.lines = args

    def blitme(self):
        if not self.debug_mode:
            return

        for i, text in enumerate(self.lines):
            surface = self.font.render(str(text), True, (240, 240, 240))
            self.screen.blit(surface, (20, i * 40))
