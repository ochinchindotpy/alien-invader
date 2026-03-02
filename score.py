import datetime
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameWorld 

class Score:
    def __init__(self, world: "GameWorld"):
        self.world = world
        self.scores = []
        #self.sort_score(file.readlines())
        self.this_score = 0

    def __str__(self):
        return str(self.this_score)

    def sort_score(self, previous_scores):
        all_scores = []

        for info in previous_scores:
            all_info = info.split("<>")
            score_int = int(all_info[2].strip())
            all_scores.append((score_int, all_info))
        
        all_scores.sort(key=lambda x: x[0], reverse=True)
        self.scores = all_scores

    def save_score(self, user):
        today = datetime.date.today()
        new_save = f"{today.year}-{today.month:02d}-{today.day:02d} <> {user} <> {self.this_score}"
        with open("scores.txt", "a") as file:
            file.write(new_save + "\n")
        
    def update(self, dead_aliens, multiplier, dt):
        if self.world.ship.moving == 0:
            return
        self.this_score += math.ceil((dt/100) ** multiplier)
        for alien in dead_aliens:
            self.this_score += math.ceil(1000 - alien.rect.y + 10*alien.speed**2)
