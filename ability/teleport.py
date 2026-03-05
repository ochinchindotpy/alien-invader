from ability.no_ability import Ability
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ship import Ship


class Teleport(Ability):
    def __init__(self, ship: "Ship"):
        self.ship = ship
        self.timer = 0

    def update(self, dt):
        self.timer += dt

    def _validate(self, *args, **kwargs):
        is_ready = self.timer > 10*1000
        is_moving = self.ship.moving != 0
        wont_leave_screen = self.ship.position_x + 200 * self.ship.moving > 0 and self.ship.screen_rect.right > self.ship.position_x + 200 * self.ship.moving
        return is_moving and wont_leave_screen and is_ready

    def _do(self, *args, **kwargs):
        self.ship.position_x += self.ship.moving * 200

    def _after(self, *args, **kwargs):
        self.timer = 0
