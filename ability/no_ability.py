from ast import Raise
from pickletools import read_uint1

from action import Action
from alien_handler import *

class Ability(Action):
    def __init__(self):
        pass
    
    def validate(self, *args, **kwargs):
        return

    def before(self, *args, **kwargs):
        pass

    def on_press(self, *args, **kwargs):
        return super().action(*args, **kwargs)
    
    def _do(self, *args, **kwargs):
        print("nothing happened :(")
        print("at least it's working :)")


    def after(self, *args, **kwargs):
        pass
    