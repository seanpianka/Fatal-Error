"""
constants
~~~~~~~~~


"""
import sys


MAX_R = MAX_C = 20
MAX_HELD_ITEMS = 16
GAME_ACTIVE = True

_green = '\033[92m'
_yellow = '\033[93m'
_teal = '\033[36m'
_blueback = '\x1b[44m'
_end = '\033[0m'
_wall_symbol = _blueback + _green + '|' + _end

MAPS_FNAME = "maps.txt"
MAP_DELIMITER = '\n\n'
DEFAULT_MAP = [r'''xxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxx
xxAxxxxxAxxxxxxxxxxx
xxAxxxxxAAAAAAxAAAAA
xxAxxxxxxxAxxxxxxxxx
xxxxxxxxxxxxxxxxxxxx
xxAxxxxxxxxAAAAAxxxx
xxAxxxxxxxxxxxxxxxxx
xxAxxxxxxAxxxxxxxxxx
xxAxxxxxAxxxxxxxxxxx
xxAxxxxxAxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxx
xxxAxxxxxxxxxxxxxxxx
xxxAxxxxxxxxAAAxxxxx
xxxAxxxxxxxAxxxxxxxx
xxxxAxxxxxAxxxxxxxxx
xxxxxxxxxAxxxxxxxxxx
xxxAAxxxAxxxxxxxxxxx
xxxAxxxxxxxxxxxxxxxx
xxxAxxxxxxxxxxxxxxxx''']


try:
    with open(MAPS_FNAME) as f:
        maps = f.read.split(MAP_DELIMITER)
except FileNotFoundError:
    e = sys.exc_info()[1].args[0] # this is the exception message
    maps = DEFAULT_MAP
