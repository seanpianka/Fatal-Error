"""
grid
~~~~


"""
from random import randint

from fatalerror.constants import MAX_R, MAX_C, _wall_symbol, maps
from fatalerror.entity import Entity
from fatalerror.character import Character
from fatalerror.item import Item
from fatalerror.space import Space
from fatalerror.terminal import s_print
from fatalerror import terminal


class Grid(object):
    def __init__(self, player, s_out, s_in):
        self._grid = [[Space() for spc in range(MAX_R)] for row in range(MAX_C)]
        self._generate_walls()

        self._player = player
        self.s_out = s_out
        self.s_in = s_in

    def _generate_walls(self):
        self._wall_space = Space(occupant=Entity(name="Wall",
                                                 title="Environment",
                                                 position=(-1, -1),
                                                 symbol=_wall_symbol))

        map_index = randint(0, len(maps) - 1)
        for i, line in enumerate(maps[map_index].split('\n')):
            for j, space in enumerate(list(line)):
                if space == 'A':
                    self._grid[i][j]._vacant = False
                    self._grid[i][j]._symbol = _wall_symbol
                    self._grid[i][j]._occupant = -1


    def display(self):
        terminal.clear_screen(self.s_out)
        terminal.go_to_terminal_coords(self.s_out, 0, 0)

        top_bot = _wall_symbol*(MAX_R*3+3) + _wall_symbol
        s_print(self.s_out, top_bot)
        for row in self._grid:
            s_print(self.s_out, _wall_symbol, end=' ')
            for space in row:
                s_print(self.s_out, ' {} '.format(space.symbol), end='')
            s_print(self.s_out, ' {}'.format(_wall_symbol))
        s_print(self.s_out, top_bot)

    def random_emplace_occupant(self, occupant):
        while True:
            r, c = randint(0, MAX_R - 1), randint(0, MAX_C - 1)
            occupant.position = (r, c)
            if self.emplace_occupant(occupant):
                break

    def move_occupant(self, occupant, position=None, offset=None):
        if not isinstance(occupant, Entity): return False

        # check if occupant doesn't already exist
        # if it doesn't attempt to emplace on grid
        grid_location = self._locate_occupant(occupant=occupant)
        if not grid_location and isinstance(position, tuple):
            occupant.position = position
            self.emplace_occupant(occupant=occupant)
        elif not grid_location and isinstance(position, tuple):
            self.emplace_occupant(occupant=occupant)

        # if occupant exists on grid, try to perform move
        if isinstance(position, tuple):
            if not self._is_in_bounds(position): return False
            if not self._is_vacant(position): return False
            self.displace_occupant(occupant=occupant)
            occupant.position = position
            self.emplace_occupant(occupant=occupant)
        elif isinstance(offset, tuple):
            if not self._is_in_bounds((occupant.r + offset[0],
                                       occupant.c + offset[1])): return False
            if not self._is_vacant((occupant.r + offset[0],
                                    occupant.c + offset[1])): return False
            self.displace_occupant(occupant=occupant)
            occupant.r += offset[0]
            occupant.c += offset[1]
            self.emplace_occupant(occupant=occupant)

        return True

    def emplace_occupant(self, occupant):
        if not isinstance(occupant, Entity): return False

        grid_coordinates = self._locate_occupant(occupant)
        if grid_coordinates is occupant.position or \
        not self._grid[occupant.r][occupant.c].vacant:
            return False

        self._grid[occupant.r][occupant.c].occupant = occupant
        return True

    def displace_occupant(self, position=None, occupant=None):
        if isinstance(position, tuple):
            grid_location = self._grid[position[0]][position[1]]
        elif occupant:
            position = self._locate_occupant(occupant)
            grid_location = self._grid[position[0]][position[1]]
            if not grid_location:
                return False

        # Don't remove an occupant if you didn't mean to do so
        if (isinstance(occupant,Entity) and grid_location.occupant is occupant)\
        or (not occupant and isinstance(position, tuple)):
            grid_location.occupant = None
            return True
        else:
            return False

    def surrounding_items(self, position=None, occupant=None):
        t_so = self.surrounding_occupants(position=position, occupant=occupant)
        return [x for x in t_so if isinstance(x[1].occupant, Item)]

    def surrounding_characters(self, position=None, occupant=None):
        t_so = self.surrounding_occupants(position=position, occupant=occupant)
        return [x for x in t_so if isinstance(x[1].occupant, Character)]

    def surrounding_occupants(self, position=None, occupant=None):
        if isinstance(occupant, Entity) and not position:
            position = self._locate_occupant(occupant)
        elif not position and not occupant:
            return False

        neighbors = lambda x, y: [(x2, y2) for x2 in range(x-1, x+2)
                                   for y2 in range(y-1, y+2)
                                   if (0 <= x < MAX_R and
                                   0 <= y < MAX_C and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 < MAX_R) and
                                   (0 <= y2 < MAX_C))]

        nl = []
        for location in neighbors(*position):
            if self._grid[location[0]][location[1]].occupant:
                nl.append((location, self._grid[location[0]][location[1]]))

        return nl

    def _is_in_bounds(self, position):
        return 0 <= position[0] < MAX_R and 0 <= position[1] < MAX_C

    def _is_vacant(self, position):
        return self._grid[position[0]][position[1]].vacant

    def _locate_occupant(self, occupant):
        """ Accepts an expected occupant argument, returns a tuple of its
        location.

        """
        try:
            return [(r, c) for r, row in enumerate(self._grid) \
                   for c, spc in enumerate(row) if spc.occupant is occupant][0]
        except IndexError:
            return None

    @property
    def grid(self):
        return self._grid
