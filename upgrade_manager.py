import pygame
import random
import alien_handler as ah
import settings as s
from upgrades import Upgrade
from enemies import Alien

class UpgradeManager:
    
    upgrades_in_screen = pygame.sprite.Group()
    
    def __init__(self, screen, settings, enemy_handler):
        self.screen = screen
        self.settings: s.Settings = settings
        self.upgrade_odds = 0.3 # 30% for every alien that can drop upgrade
        self.handler: ah.EnemyHandler = enemy_handler

        self.last_upgrade_timer = 0 # is ms
        self.upgrade_frequency = settings.upgrade_frequency * 1000 # in ms --- settings.upgrade_frequency is in seconds 
        self.timer_increase_for_alien = 100

        self.last_upgrades = [] # for bad luck protection
        formatation = {
            "category": {"stat": "value", "text": "Text that  will appear on the screen"}
        }
        self.common_upgrades = { # todo: add "target" key to stat dict, example "target": "ship". This could allow better upgrades 
            "weapon": {"nothing": "reroll"},

            "move_speed": {
                            "speed_default": {"value": 0.5, "text": "Your ship is faster in normal speed!"},
                            "shift_speed_default": {"value": 0.3, "text": "Your ship got faster in slow mode!"},
                            "speed_percentage": {"value": 0.1, "text": r"Your ship got 10% faster!"},  # 10%
                            #"speed_temp": {"value": 3, "duration": 5, "text": "Your ship moves really fast for 5 seconds!"}, 
                            "speed_both": {"value": 0.2, "text": "Your entire ship got faster!"}
                            },

            "fire_speed": {
                            "bullet_delay": {"value": -5*60, "text": "Your guns are recharging faster!"}, # DECREASES the delay between bullets, so it's negative
                            "max_bullets": {"value": 1, "text": "More bullets!"},
                            #"max_kills": {}, # this will be pretty hard to implement, but ok
                            "bullet_speed": {"value": 1.5, "text": "Faster bullets!"}
            },

            "ability": {
                            "extra_life": {"value": True, "text": "Your ship's hull got more resistent!"},
                            "more_upgrades": {"value": 25, "text": "Killing aliens get you more upgrades!"},
            }
        } # all upgrades will be common for now
        self.categories = ["move_speed", "fire_speed", "ability"] # todo: once implemented, add "weapon" here
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
    
    def _deny_spawn(self):
        if self.upgrade_frequency > self.last_upgrade_timer: # avoid too many upgrades
            # todo: Shop class with shop.coin
            return True
        if random.random() > self.upgrade_odds and self.upgrade_odds > 0: # rng, only 30% of chance of spawning
            # todo: Shop and shop.coin class
            self.upgrade_odds += 0.05 # small bad luck protection
            return True
        return False    

    def _choose_upgrade(self):
        """Choose an upgrade_category and reroll once if you got it recently, reducing the chances of getting the same upgrade every time
        Shouldn't garantee a new upgrade category every time, only reroll once"""
        upgrade_category = random.choice(self.categories)
        self.once = False

        if upgrade_category in self.last_upgrades: # reroll if you got same category too recently
            upgrade_category = random.choice(self.categories)
        

        return upgrade_category

    def _register_recent(self, upgrade_category):
        """Saves the upgrades you got recently, for self._choose_upgrade"""
        if len(self.last_upgrades) >= 3:
            self.last_upgrades.pop(0)
        self.last_upgrades.append(upgrade_category)
        
    def _reset_odds(self):
        """Resets odds"""
        self.last_upgrade_timer -= self.upgrade_frequency # todo: this could be better
        self.upgrade_odds -= 0.4


    def _spawn(self, alien: Alien):
        if self._deny_spawn():
            return

        upgrade_category = self._choose_upgrade()
        self._register_recent(upgrade_category)
        self._reset_odds()
        
        print("Upgrade!")

        # testing below, to be deleted later
        """testing below, to be deleted later"""

        common_all = self.common_upgrades[upgrade_category]


        upgrade_key = random.choice(list(common_all.keys()))

        upgrade_item = common_all[upgrade_key]

        self.upgrades_in_screen.add(Upgrade(self.screen, self.settings, alien, "common", upgrade_category, upgrade_key, upgrade_item))


