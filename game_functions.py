import pygame
import sys


#game_funtions.py

def check_events(debug):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                debug.debug_mode = not debug.debug_mode

def update_logic(ship, difficult, enemy_handler, upgrade_manager, dt):
    if ship.dead == -1:
        ship.update(dt)
        ship.weapon.bullets.update()
        difficult.update(dt)
        enemy_handler.update(ship)
        upgrade_manager.update(dt, ship)


def update_screen(setting, screen, ship, enemies, upgrades_troops, debug):
    screen.fill(setting.bg_color)
    ship.blitme() # draws the ship
    
    for bullet in ship.weapon.bullets:
         bullet.blitme()
    
    for enemy in enemies:
        enemy.blitme()
    for upgrade in upgrades_troops:
        upgrade.blitme()
    
    debug.blitme()
        

    pygame.display.flip() # update display

