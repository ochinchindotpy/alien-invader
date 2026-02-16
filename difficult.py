import random

class DifficultManager:
    #todo: make the game harder as the player stays alive
    # maybe every 30~60 seconds, a random attribute increases, like alien speed or number of alien spawning
    # EnemyHandler should read info from this class and act on it
    
    def __init__(self, settings):
        self.settings = settings

        # getting harder over time
        self._next_increase = random.randint(30, 60) * 1000 # in ms
        self.timer = 0 # in ms
        self.difficult = 1

        # speed info
        self.speed_info = {
            "min_roll": 1, 
            "max_roll": 3,
            "rolls_quantity": 5,
            "constant": 1
        }
        self._speed_keys = list(self.speed_info.keys())
        # spawn info
        self.spawn_info = { 
            "spawner_min": 1,
            "spawner_max": 3,
            "base_delay": 90,
            "delay_offset_p": 30,
            "delay_offset_n": 30,
        }
        self._spawn_keys = list(self.spawn_info.keys())

        self.categories = {
            "spawning": self._increase_spawn,
            "speed": self._increase_speed,
            "special": self._unlock_special
        }
        self.category_caller = list(self.categories.keys())

        self._specials = {
            "dash": self._allow_dash,
            "shield": self._allow_shield
        }
        self._specials_caller = list(self._specials.keys())
        
    def get_spawn_info(self, data):
        """spawner_min - spawner_max - base_delay - delay_offset_p -delay_offset_n"""
        return self.spawn_info[data]

    def get_speed_info(self, data):
        """min_roll - max_roll - rolls_quantity - constant"""
        return self.speed_info[data]

    def update(self, delta):
        self.timer += delta
        self.increase_difficult()

    def increase_difficult(self):
        """Chooses a random category to upgrade. The category-functions calls another random attribute to upgrade"""
        if self._next_increase > self.timer:
            return
        buffed = random.choice(self.category_caller)
        print(f"Changing: {buffed}")
        self._next_increase = self.timer + random.randint(30, 60) * 1000 # in ms
        self.categories[buffed]()

    def _increase_spawn(self): # category
        buffed = random.choice(self._spawn_keys)
        self.spawn_info[buffed] = self.spawn_info[buffed] + 1


    def _increase_speed(self): # category
        if self.speed_info["min_roll"] == self.speed_info["max_roll"]:
            self.speed_info["max_roll"] = self.speed_info["max_roll"] + 1
            return
        buffed = random.choice(self._speed_keys)

        self.speed_info[buffed] = self.speed_info[buffed] + 1

    def _unlock_special(self):
        self._specials[random.choice(self._specials_caller)]()

    def _allow_dash(self): # todo: add dash
        ...

    def _allow_shield(self): #todo: add shield
        ...