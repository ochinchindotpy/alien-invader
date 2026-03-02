import json
from assets import get_path

class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (120, 120, 210)
        self.enemies_have_dash = True # temp

        self.upgrade_frequency = 5 # in seconds 
        self.ship_speed = 3
        self.ship_speed_shift = 1.3

        file = get_path("settings_weapon.json")

        with open(file, "r") as f:
            self.weapon_data = json.load(f)


    def get_weapon_settings(self, weapon) -> dict:
        return self.weapon_data[weapon]
        