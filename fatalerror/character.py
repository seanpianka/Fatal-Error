"""
character
~~~~~~~~~


"""
from fatalerror.entity import Entity
from fatalerror.item import Item
from fatalerror.constants import MAX_HELD_ITEMS


class Character(Entity):
    def __init__(self, name, role, inventory=[], equipped=None,
                 position=None, symbol=None):
        self._role = role
        self._strength = role.strength
        self._defense = role.defense
        self._health = role.health
        self._inventory = inventory
        self._equipped = equipped
        self._alive = True
        symbol = role.symbol if not symbol else symbol
        super(Character, self).__init__(name, role.title, position, symbol)

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, new_strength):
        if new_strength > 0:
            self._strength = new_strength

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, new_defense):
        if new_defense > 0:
            self._defense = new_defense

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        if new_health >= 0: self._health = new_health

    @property
    def role(self):
        return self._role

    @property
    def inventory(self):
        return self._inventory

    def pickup_item(self, item):
        if isinstance(item, Item) and len(self._inventory) < MAX_HELD_ITEMS:
            self._inventory.append(item)

    def drop_item(self, item):
        if isinstance(item, Item) and len(self._inventory) > 0:
            del self._inventory[self._inventory.index(item)]

    @property
    def equipped(self):
        return self._equipped

    @equipped.setter
    def equipped(self, new_equipped):
        if ininstance(new_equipped, Item) and new_eqipped.inventory_size:
            self._equipped = new_equipped

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, new_alive):
        if not self.health:
            self._alive = False
