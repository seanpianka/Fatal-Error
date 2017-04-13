"""
item
~~~~


"""
from fatalerror.entity import Entity

class Item(Entity):
    def __init__(self, name, function, position=None, symbol=None):
        self._function = function
        # if inventory_size is 0, then the Item cannot be equipped
        self._inventory_size = function.inventory_size
        self._durability = function.durability
        # allows for custom symbol to be provided, override function's symbol
        symbol = function.symbol if not symbol else symbol
        super(Item, self).__init__(name, function.title,
                                   position, symbol)

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, new_durability):
        if 0 <= new_durability <= 100:
            self._durability = new_durability

    @property
    def inventory_size(self):
        return self._inventory_size

    @inventory_size.setter
    def inventory_size(self, new_inventory_size):
        if isinstance(new_inventory_size, int) and new_inventory_size >= 0:
            self._inventory_size = new_inventory_size

    @property
    def function(self):
        return self._function
