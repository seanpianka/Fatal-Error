"""
space
~~~~~

"""
from fatalerror.entity import Entity


class Space(object):
    _grid_symbol = '.'

    def __init__(self, occupant=None):
        self._occupant = None
        self.occupant = occupant
        self._vacant = not occupant
        self._symbol = Space._grid_symbol
        self.symbol = Space._grid_symbol if not occupant else occupant.symbol

    def __str__(self):
        return self._symbol

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, new_symbol):
        self._symbol = new_symbol

    @property
    def occupant(self):
        return self._occupant

    @occupant.setter
    def occupant(self, new_occupant):
        if isinstance(new_occupant, Entity) or not new_occupant:
            self._occupant = new_occupant
            try:
                self.symbol = self._occupant.symbol
                self.vacant = False
            except AttributeError:
                self.symbol = Space._grid_symbol
                self.vacant = True

    @property
    def vacant(self):
        return self._vacant

    @vacant.setter
    def vacant(self, vacancy_status):
        if isinstance(vacancy_status, bool):
            self._vacant = vacancy_status


