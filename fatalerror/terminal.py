"""
terminal
~~~~~~~~


"""
from __future__ import print_function
import os
import select
import sys
import termios

from fatalerror.constants import _wall_symbol


class KeyPoller():
    def __init__(self):
        self.ready = False

    def _revert_terminal(self):
        self.ready = False
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def _convert_terminal(self):
        self.ready = True
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

    def __enter__(self):
        self._convert_terminal()
        return self

    def __exit__(self, type, value, traceback):
        self._revert_terminal()

    def poll(self):
        if self.ready:
            dr,dw,de = select.select([sys.stdin], [], [], 10000)
            if not dr == []:
                return sys.stdin.read(1)
        return None


def clear_screen(_os):
    # clear grid
    term_height = 50
    term_width = 63
    go_to_terminal_coords(_os, 0, 0)
    for i in range(term_height):
        go_to_terminal_coords(_os, i, 0)
        s_print(_os, str(_wall_symbol) + ' ' * (term_width - 1) + str(_wall_symbol), end="")


def s_print(_os, *args, **kwargs):
    if kwargs.get('print_border'):
        print("{} ".format(_wall_symbol), end="")
        kwargs.pop('print_border')
    print(*args, file=_os, **kwargs)
    _os.flush()


def s_input(_is):
    return _is.readline()


def get_terminal_dimensions():
    rows, columns = os.popen('stty size', 'r').read().split()
    return (int(rows), int(columns))


def go_to_terminal_coords(output, row, col):
    """ Terminal coordinates start at (1, 1), add 1 for zero indexed lists. """
    output.write("\033[{0};{1}f".format(row+1, col+1))


if __name__ == '__main__':
    with KeyPoller() as kp:
        while True:
            c = kp.poll()
            if c:
                if c == "c":
                    break
                print(ord(c))
