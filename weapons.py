class Weapon:
    # todo: ship should use a child of this class 
    # every time the ship shoots, it calls ship.weapon.attack()
    # weapon.attack() should return a respective Bullet class 


    def attack(self):
        pass

class Laser(Weapon):
    def attack(self):
        ...