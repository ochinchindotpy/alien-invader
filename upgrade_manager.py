import pygame
import random
import settings as s
from typing import TYPE_CHECKING
from upgrades import Upgrade
from enemies import Alien

if TYPE_CHECKING:
    from game import GameWorld
    import alien_handler as ah
    from settings import Settings


class UpgradeManager:
    
    upgrades_in_screen = pygame.sprite.Group()
    
    def __init__(self, screen, settings: "Settings", enemy_handler, world: "GameWorld"):
        self.world = world
        self.more_upgrades = 0

        self.screen = screen
        self.settings: s.Settings = settings
        self.upgrade_odds = 0.3 # 30% for every alien that can drop upgrade
        self.handler: "ah.EnemyHandler" = enemy_handler
        
        self.last_upgrade_timer = 0 # is ms
        self.upgrade_frequency = settings.upgrade_frequency * 1000 # in ms --- settings.upgrade_frequency is in seconds 
        self.timer_increase_for_alien = 100

        self.last_upgrades = [] # for bad luck protection
        formatation = {
            "category": {"stat": "value", "text": "Text that  will appear on the screen"}
        }
        self.common_upgrades = {
            "weapon": {"nothing": "reroll"},

            "move_speed": {
                            "speed_default": {"value": 0.5, "target": "ship", "text": "Your ship is faster in normal speed!"},
                            "shift_speed_default": {"value": 0.3, "target": "ship", "text": "Your ship got faster in slow mode!"},
                            "speed_percentage": {"value": 0.1, "target": "ship", "text": r"Your ship got 10% faster!"},  # 10%
                            #"speed_temp": {"value": 3, "duration": 5, "target": "ship", "text": "Your ship moves really fast for 5 seconds!"}, 
                            "speed_both": {"value": 0.2, "target": "ship", "text": "Your entire ship got faster!"}
                            },

            "fire_speed": {
                            "bullet_delay": {"value": -5*60, "target": "ship.weapon", "text": "Your guns are recharging faster!"}, # DECREASES the delay between bullets, so it's negative
                            "max_bullets": {"value": 1, "target": "ship.weapon", "text": "More bullets!"},
                            "max_kills": {"value": 1, "target": "ship.weapon", "text": "Your bullets pierce!"}, # this will be pretty hard to implement, but ok
                            "bullet_speed": {"value": 1.5, "target": "ship.weapon", "text": "Faster bullets!"}
            },

            "ability": {
                            "extra_life": {"value": True, "target": "ship", "text": "Your ship's hull got more resistent!"},
                            "more_upgrades": {"value": 25, "target": "upgrade", "text": "Killing aliens get you more upgrades!"},
            }
        } # all upgrades will be common for now
        
        self.targets = {
            "ship": lambda: world.ship,
            "ship.weapon": lambda: world.ship.weapon,
            "upgrade": lambda: self
        }

        self.categories = ["move_speed", "fire_speed", "ability"] # todo: once implemented, add "weapon" here
        #self.categories = ["ability"]
    
    def upgrade(self, stat, change):
        setattr(self, stat, getattr(self, stat) + change)
    
    def update(self, dt, ship):
        self.last_upgrade_timer += dt

        alien_kill_bonus = 0
        for alien in self.handler.dead_aliens:
            self._spawn(alien)
            alien_kill_bonus += self.timer_increase_for_alien
            alien_kill_bonus += self.more_upgrades
        
        self.last_upgrade_timer += alien_kill_bonus  # killings aliens get you upgrades faster

        upgrade: Upgrade

        for upgrade in self.upgrades_in_screen:
            upgrade.update()
            upgrade.on_collision(ship)
    
    def _allow_spawn(self):
        # todo: Shop and shop.coin class
        is_ready = self.last_upgrade_timer >= self.upgrade_frequency # timer to avoid too many upgrades
        had_luck = self.upgrade_odds > random.random()

        if not had_luck:
            self.upgrade_odds += 0.05 # small bad luck protection

        return is_ready and had_luck

    def _choose_upgrade(self):
        """Choose an upgrade_category and reroll once if you got it recently, reducing the chances of getting the same upgrade every time
        Shouldn't garantee a new upgrade category every time, only reroll once"""
        upgrade_category = random.choice(self.categories)

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
        self.upgrade_odds = max(0.0, self.upgrade_odds - 0.4)

    def get_target(self, context):
        return self.targets[context["target"]]()

    def _spawn(self, alien: Alien):
        if not self._allow_spawn():
            return

        upgrade_category = self._choose_upgrade()
        self._register_recent(upgrade_category)
        self._reset_odds()

        common_all = self.common_upgrades[upgrade_category] # entire dict

        upgrade_key = random.choice(list(common_all.keys())) # category of the dict (i.e: "fire_speed")
        #upgrade_key = "extra_life"
        upgrade_item = common_all[upgrade_key] # {"value": 1, "text": "abc"}
        target = self.get_target(upgrade_item) # who it will apply to

        self.upgrades_in_screen.add(Upgrade(self.screen, self.settings, alien, target, "common", upgrade_category, upgrade_key, upgrade_item))
