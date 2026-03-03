from logging import BufferingFormatter
import random

class DifficultManager:
    def __init__(self, settings):
        self.settings = settings

        # getting harder over time
        self._next_increase = random.randint(30, 60) * 1000 # in ms
        self.timer = 0 # in ms
        self.difficult = 1

        # speed info
        self.speed_info = {
            "min_roll": 0, 
            "max_roll": 2,
            "rolls_quantity": 5,
            "constant": 1
        }
        self._speed_keys = list(self.speed_info.keys())
        # spawn info
        self.spawn_info = { 
            "spawner_min": {"value": 1, "increase_rate": 1},
            "spawner_max": {"value": 3, "increase_rate": 1},
            "base_delay": {"value": 1500, "increase_rate": -250},
            "delay_offset_p": {"value": 500, "increase_rate": -50},
            "delay_offset_n": {"value": 500, "increase_rate": -50},
        }
        self._spawn_keys = list(self.spawn_info.keys())

        self.categories = {
            "spawning": self._increase_spawn,
        #    "speed": self._increase_speed,
        #    "special": self._unlock_special
        }
        self.category_caller = list(self.categories.keys())

        self._specials = {
            "dash": self._allow_dash,
            "shield": self._allow_shield
        }
        self._specials_caller = list(self._specials.keys())
        
    def get_spawn_info(self, data):
        """spawner_min - spawner_max - base_delay - delay_offset_p -delay_offset_n"""
        return self.spawn_info[data]["value"]

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
        self._next_increase = self.timer + random.randint(30, 60) * 1000 # in ms
        self.categories[buffed]()
        self.difficult += 0.1

    def _increase_spawn(self): # category
        buffed = random.choice(self._spawn_keys)
        print("spawn")
        print(buffed)
        self.spawn_info[buffed]
        print("-"*10)
        self.spawn_info[buffed]["value"] = self.spawn_info[buffed]["value"] + self.spawn_info[buffed]["increase_rate"]


    def _increase_speed(self): # category
        if self.speed_info["min_roll"] == self.speed_info["max_roll"]:
            self.speed_info["max_roll"] = self.speed_info["max_roll"] + 1
            return
        buffed = random.choice(self._speed_keys)
        print(buffed)

        self.speed_info[buffed] = self.speed_info[buffed] + 1

    def _unlock_special(self): # category
        self._specials[random.choice(self._specials_caller)]()

    def _allow_dash(self): # todo: add dash
        ...

    def _allow_shield(self): #todo: add shield
        ...


if __name__ == "__main__": # debugging
    from settings import Settings
    dm = DifficultManager(Settings())
    d = {}
    for i in range (1000000):
        speed = dm.get_speed_info("constant") + sum(random.randint(dm.get_speed_info("min_roll"), dm.get_speed_info("max_roll")) for _ in range(dm.get_speed_info("rolls_quantity"))) # difficult related
        
        if speed in list(d.keys()):
            d[speed] += 1
        else:
            d[speed] = 1
    
    d_sort = list(d.keys())
    d_sort.sort()
    for key in d_sort:
        print(f"{key}: {d[key]}   |   {d[key]/1000000}")
