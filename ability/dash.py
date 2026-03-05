from ability.no_ability import Ability
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ship import Ship

SPEED_BONUS = 4


class Dash(Ability):
    def __init__(self, ship: "Ship"):
        super().__init__(ship)
        self.dashing = False
        self.timer = 0
        self.dashing_timer = 0

    def update(self, dt):
        self.timer += dt
        self.dashing_timer += dt * self.dashing
        if self.dashing_timer > 1000:
            self.timer = 0
            self.dashing = False
            self.dashing_timer = 0
            self.ship.speed_default -= SPEED_BONUS


    def _validate(self):
        not_slow = not self.ship.slow_move
        is_ready = self.timer >= 5000
        not_dashing = not self.dashing
        return not_slow and is_ready and not_dashing

    def _before(self, *args, **kwargs):
        self.dashing = not self.dashing
        return super()._before(*args, **kwargs)
    
    def _do(self, *args, **kwargs):
        print(1)
        self.ship.speed_default += SPEED_BONUS

