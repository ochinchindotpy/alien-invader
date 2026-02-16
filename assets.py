import sys
import os
import pygame

def image_load(relative_path):
    """Get absolute path to resource, works for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return pygame.image.load(os.path.join(base_path, relative_path))
