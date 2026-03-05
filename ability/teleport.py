from ability.no_ability import Ability
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ship import Ship

_TELEPORT_RANGE = 200
_COOLDOWN = 10_000

class Teleport(Ability):
    def __init__(self, ship: "Ship"):
        self.ship = ship
        self.timer = 0

    def update(self, dt):
        self.timer += dt

    def _validate(self, *args, **kwargs):
        is_ready = self.timer > _COOLDOWN
        is_moving = self.ship.moving != 0
        wont_leave_screen = self.ship.position_x + _TELEPORT_RANGE * self.ship.moving > 0 and\
              self.ship.screen_rect.right > self.ship.position_x + _TELEPORT_RANGE * self.ship.moving
        return is_moving and wont_leave_screen and is_ready

    def _do(self, *args, **kwargs):
        self.ship.position_x += self.ship.moving * _TELEPORT_RANGE

    def _after(self, *args, **kwargs):
        self.timer = 0
