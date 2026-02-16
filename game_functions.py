import pygame
import sys


#game_funtions.py

def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def update_screen(setting, screen, ship, enemies):
    screen.fill(setting.bg_color)
    ship.blitme() # draws the ship
    
    for bullet in ship.bullets:
         bullet.blitme()
    
    for enemy in enemies:
        enemy.blitme()
    
    pygame.display.flip() # update display

