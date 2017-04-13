"""
entity
~~~~~~


"""
from fatalerror.constants import MAX_R, MAX_C


class Entity(object):
    def __init__(self, name, title, position, symbol):
        self._name = name
        self._title = title
        self._symbol = symbol
        if not position:
            self._r, self._c = -1, -1
        else:
            self._r, self._c = position

    def _move_to(self, r=None, c=None):
        """ Move the Character instance to the specified grid after bounds
        check.

        """
        if isinstance(r, int):
            if 0 <= r < MAX_C:
                self._r = r
            elif r >= MAX_R:
                self._r = MAX_R - 1
            elif r <= 0:
                self._r = 0

        if isinstance(c, int):
            if 0 <= c < MAX_C:
                self._c = c
            elif c >= MAX_C:
                self._c = MAX_C - 1
            elif c <= 0:
                self._c = 0

    @property
    def title(self):
        return self._title

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if len(new_name) < 256:
            self._name = new_name

    @property
    def symbol(self):
        return self._symbol

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, new_r):
        self._move_to(r=new_r)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, new_c):
        self._move_to(c=new_c)

    @property
    def position(self):
        return (self.r, self.c)

    @position.setter
    def position(self, new_position):
        if isinstance(new_position, tuple):
            self.r, self.c = new_position
