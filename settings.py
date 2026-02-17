
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        # todo: check if there are more variables that could be move to this class
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (120, 120, 210)
        

        self.fire_speed = 1000 # in ms
        self.upgrade_frequency = 5 # in seconds 
        self.ship_speed = 3
        self.ship_speed_shift = 1.3
