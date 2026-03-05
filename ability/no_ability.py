from abc import abstractmethod
from action import Action
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ship import Ship

class Ability(Action):
    def __init__(self, ship: "Ship"):
        self.ship = ship
        pass
    
    @abstractmethod
    def update(self, dt):
        pass

    def _validate(self, *args, **kwargs):
        return False

    def _before(self, *args, **kwargs):
        pass

    def on_press(self, *args, **kwargs):
        return super().action(*args, **kwargs)
    
    def _do(self, *args, **kwargs):
        pass

    def after(self, *args, **kwargs):
        pass
    