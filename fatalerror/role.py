"""
role
~~~~


"""
class Role(object):
    def __init__(self, health, strength, defense, title, symbol):
        self._health = health
        self._strength = strength
        self._defense = defense
        self._title = title
        self._symbol = symbol

    @property
    def health(self):
        return self._health

    @property
    def strength(self):
        return self._strength

    @property
    def defense(self):
        return self._defense

    @property
    def attack(self):
        return self._attack

    @property
    def title(self):
        return self._title

    @property
    def symbol(self):
        return self._symbol

class Enemy(Role):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)

class Player(Role):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
