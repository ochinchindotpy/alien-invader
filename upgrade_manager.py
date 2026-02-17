import pygame
import random
import alien_handler as ah
import settings as s
from upgrades import Upgrade
from enemies import Alien

class UpgradeManager:
    
    upgrades_in_screen = pygame.sprite.Group()
    
    def __init__(self, screen, settings, enemy_handler):
        self.last_upgrade_timer = 0 # is ms
        self.screen = screen
        self.settings: s.Settings = settings
        self.upgrade_frequency = settings.upgrade_frequency * 1000 # in ms --- settings.upgrade_frequency is in seconds 
        self.upgrade_odds = 0.3 # 30% for every alien that can drop upgrade
        self.handler: ah.EnemyHandler = enemy_handler
        self.timer_increase_for_alien = 100

        self.last_upgrades = [] # for bad luck protection
        formatation = {
            "category": {"stat": "value", "text": "Text that  will appear on the screen"}
        }
        self.common_upgrades = {
            "weapon": {"nothing": "reroll"},

            "move_speed": {
                            "default_speed": {"value": 0.5, "text": "Your ship is faster in normal speed!"},
                            "slow_speed": {"value": 0.3, "text": "Your ship got faster in slow mode!"},
                            "speed_percentage": {"value": 0.1, "text": r"Your ship got 10% faster!"},  # 10%
                            "speed_temp": {"value": 3, "duration": 5, "text": "Your ship moves really fast for 5 seconds!"}, 
                            "speed_both": {"value": 0.2, "text": "Your entire ship got faster!"}
                            },

            "fire_speed": {
                            "bullet_delay": {"value": -5*60, "text": "Your guns are recharging faster!"}, # 
                            "max_bullets": {"value": 1, "text": "More bullets!"},
                            #"max_kills": {}, # this will be pretty hard to implement, but ok
                            "bullet_speed": {"value": 1.5, "text": "Faster bullets!"}
            },

            "ability": {
                            "extra_life": {"value": True, "text": "Your ship's hull got more resistent!"},
                            "more_upgrades": {"value": 25, "text": "Killing aliens get you more upgrades!"},
            }
        }
        self.categories = ["weapon", "move_speed", "fire_speed", "ability"]
        self.once = False


    def update(self, dt, ship):
        self.last_upgrade_timer += dt
        if self.last_upgrade_timer > self.upgrade_frequency and not self.once:
            print("ok")
            self.once = True
        for alien in self.handler.dead_aliens:
            self._spawn(alien)
        self.last_upgrade_timer += len(self.handler.dead_aliens) * self.timer_increase_for_alien # killings aliens get you upgrades faster

        for upgrade in self.upgrades_in_screen:
            upgrade.update()
            upgrade.on_collision(ship)
    
    def _spawn(self, alien: Alien):
        if self.upgrade_frequency > self.last_upgrade_timer: # avoid too many upgrades
            # todo: Shop and shop.coin class
            return
        if random.random() > self.upgrade_odds: # rng, only 30% of chance of spawning
            # todo: Shop and shop.coin class
            self.upgrade_odds += 0.05 # bad luck protection
            return
        
        upgrade_type = random.choice(self.categories)

        if upgrade_type in self.last_upgrades: # reroll if you got same category too recently
            upgrade_type = random.choice(self.categories)
        
        # write that you got this upgrade recently
        if len(self.last_upgrades) >= 3:
            self.last_upgrades.pop(0)
        self.last_upgrades.append(upgrade_type)
        
        
        print("Upgrade!")
        # testing below, to be delete later
        """testing below, to be delete later"""



        common_all = self.common_upgrades[upgrade_type]
        if common_all == "weapon":
            print("no")
            return
        
        stat = random.choice(list(common_all.keys()))

        self.upgrades_in_screen.add(Upgrade(self.screen, self.settings, alien, "common", upgrade_type, stat))


