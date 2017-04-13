"""
function
~~~~~~~~

Object per the "Type-Object" pattern to describe the functionality of the Item
instance which includes a Function instance.

"""
class Function(object):
    def __init__(self, durability, inventory_size, title, symbol, **kwargs):
        self._durability = durability
        # if inventory_size is 0, then the Item cannot be equipped
        self._inventory_size = inventory_size
        self._title = title
        self._symbol = symbol

    @property
    def durability(self):
        return self._durability

    @property
    def inventory_size(self):
        return self._inventory_size

    @property
    def title(self):
        return self._title

    @property
    def symbol(self):
        return self._symbol

class Storage(Function):
    def __init__(self, **kwargs):
        super(Storage, self).__init__(**kwargs)
        self._capacity = kwargs['capacity']
        self._inventory = [] if not kwargs['inventory'] else kwargs['inventory']

class Weapon(Function):
    def __init__(self, **kwargs):
        super(Weapon, self).__init__(**kwargs)
        self._damage = kwargs['damage']

class Food(Function):
    def __init__(self, **kwargs):
        super(Food, self).__init__(**kwargs)
        self._health_restore = kwargs['health_restore']
