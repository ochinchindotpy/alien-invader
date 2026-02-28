import sys
import os
import pygame


def image_load(relative_path):
    """Get absolute path to resource, works for PyInstaller"""
    try:
        base_path = sys._MEIPASS
        print(base_path)
    except Exception:
        base_path = os.path.abspath(".")
    return pygame.image.load(os.path.join(base_path, relative_path))


def get_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)
