from operator import not_

from ability.teleport import Teleport
from ability.no_ability import Ability
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ship import Ship

_COOLDOWN = 7_000
_TIME_IN = 2_500
_TELEPORT_RANGE = 250


class InOut(Ability):
    def __init__(self, ship: "Ship"):
        super().__init__(ship)
        self.cooldown_timer = 0
        self.return_timer = 0
        self._used_ability: bool = False
        self.return_place = None

    def update(self, dt):
        self.cooldown_timer += dt
        if not self._used_ability:
            return
        self.return_timer += dt
        will_return = self.return_timer > _TIME_IN
        if will_return:
            self.out()

    def _validate(self, *args, **kwargs):
        not_active = not self._used_ability
        is_ready = self.cooldown_timer > _COOLDOWN
        is_moving = self.ship.moving != 0
        wont_leave_screen = self.ship.position_x + _TELEPORT_RANGE * self.ship.moving > 0 and\
              self.ship.screen_rect.right > self.ship.position_x + _TELEPORT_RANGE * self.ship.moving
        return is_moving and wont_leave_screen and is_ready and not_active

    def _before(self, *args, **kwargs):
        self.return_place = self.ship.position_x 

    def _do(self, *args, **kwargs):
        self.ship.position_x += self.ship.moving * _TELEPORT_RANGE
        
    def _after(self, *args, **kwargs):
        self.return_timer = 0
        self.cooldown_timer = 0
        self._used_ability = True
        self.ship.speed_debuff = max(1, abs(self.ship.speed)/2)

    def out(self):
        self.ship.speed_debuff = 0
        self.ship.position_x = self.return_place
        self.return_place = None
        self._used_ability = False
        self.return_timer = 0
