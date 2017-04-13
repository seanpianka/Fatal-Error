from __future__ import print_function
import time
import sys
import socket

import fatalerror.grid
import fatalerror.terminal
from fatalerror.constants import _wall_symbol
from fatalerror.terminal import s_print
from fatalerror.combatinstance import CombatInstance
from fatalerror.constants import MAX_R, MAX_C, MAX_HELD_ITEMS
from fatalerror.assets import (Character,  r_player, r_enemy,
                                Item,       f_storage, f_weapon, f_food)


class FatalError:
    def __init__(self, s_out=sys.stdout, s_in=sys.stdin):
        self.s_out = s_out
        self.s_in = s_in
        self._create_player()
        self._map = grid.Grid(self._player, self.s_out, self.s_in)
        self._spawn_all_entities()
        self.win_condition = lambda player, item: item in player.inventory

        s_print(self.s_out, "\n3")
        time.sleep(1)
        s_print(self.s_out, "2")
        time.sleep(1)
        s_print(self.s_out, "1")
        time.sleep(1)
        s_print(self.s_out, "Begin!")
        time.sleep(1)

    def _create_player(self):
        game_title = "0xF97C~~FATAL_ERROR~~0x19FA"
        s_print(self.s_out, game_title)

        # Determine user's name
        name_title = "Challenger! Tell me your name!\n> "
        s_print(self.s_out, name_title, end='')
        while True:
            name_choice = self.s_in.readline().rstrip()
            if name_choice.islower():
                name_choice = name_choice.capitalize()

            if len(name_choice) < 256:
                greeting = "Welcome to the arena, {}!"
                s_print(self.s_out, greeting.format(name_choice))
                break
            else:
                incorrect_name = "Your name is not that long. Try again!\n> "
                s_print(self.s_out, incorrect_name, end='')

        # Determine user's preferred role
        role_title = "\nAre you a h4x0r or a Code Warrior?\n" + \
                      "1) h4x0r (h)\n2) Code Warrior (c||w)\n\n> "
        s_print(self.s_out, role_title, end='')
        while True:
            role_choice = self.s_in.readline().replace(" ", "").rstrip()
            if role_choice.lower() in ['h', 'h4x0r']:
                role_choice = 'h4x0r'
                break
            elif role_choice.lower() in ['c', 'w' 'codewarrior', 'code_warrior']:
                role_choice = 'code_warrior'
                break
            else:
                incorrect_role = "That was not one of the options! Choose again!\n> "
                s_print(self.s_out, incorrect_role, end='')

        self._player = Character(name=name_choice,
                                 role=r_player[role_choice],
                                 position=(0, 0))

    def _spawn_all_entities(self):
        self._goal = Item("Goal Backpack", f_storage['Backpack'],
                          position=(2, 4), symbol='G')
        self._misc = Item("Backpack", f_storage['Backpack'],
                          position=(1, 5))
        self._robot_army = [Character(name="robot_{}".format(i), \
                            role=r_enemy['EvilRobot']) \
                            for i in range(5)]

        self._map.random_emplace_occupant(self._player)
        self._map.random_emplace_occupant(self._goal)
        self._map.random_emplace_occupant(self._misc)
        for robot in self._robot_army:
            self._map.random_emplace_occupant(robot)

    def _new_combat_instance(self, combatant):
        dead = CombatInstance(self._player, combatant, self.s_out, self.s_in).fight()
        self._map.displace_occupant(occupant=dead)
        self._map.display()

    def _cmd_help(self):
        help_all_cmds = "AVAILABLE COMMANDS: Help, Quit, Health, Attack, Pickup\n"
        s_print(self.s_out, help_all_cmds, print_border=True)
        help_goal = "Your goal, using the `attack` command, is to defeat enemies\n" \
                    "and successfully recover the goal backpack labeled `G` " \
                    "using\n`pickup` command while next to it. Move around the" \
                    "map using \nthe `go {N|S|E|W}` command."
        s_print(self.s_out, help_goal, print_border=True)

    def _cmd_quit(self):
        if self.s_out == sys.stdout: sys.exit(0)
        else: raise socket.error

    def _cmd_go(self, direction):
        err_msg = 'Invalid use of `go` command.'
        if not direction[0]: raise UserWarning(err_msg)
        offs = {
            'N': (-1, 0),
            'S': (1, 0),
            'W': (0, -1),
            'E': (0, 1)
        }
        old_position = new_position = 0
        try:
            offset = offs[direction[0].upper()]

            if not self._map.move_occupant(self._player, offset=offset):
                s_print(self.s_out, "Your path is blocked.", print_border=True)
            else:
                self._map.display()
        except KeyError:
            raise UserWarning(err_msg)

    def _cmd_health(self):
        s_print(self.s_out, "Health: {}".format(self._player.health), print_border=True)

    def _cmd_inventory(self):
        s_print(self.s_out, "Inventory [{}/{}]:".format(len(self._player.inventory),
                                                        MAX_HELD_ITEMS), print_border=True)
        for i, item in enumerate(self._player.inventory):
            s_print(self.s_out, "{}: {}".format(i+1, item.name), print_border=True)

    def _cmd_pickup(self):
        nl = self._map.surrounding_items(position=self._player.position)

        if not nl:
            s_print(self.s_out, "No nearby items to pick up.", print_border=True)
            self._map.display()
            return
        elif len(nl) is 1:
            self._player.pickup_item(nl[0][1].occupant)
            self._map.displace_occupant(nl[0][0])
            self._map.display()
            return

        # else, multiple nearby items
        s_print(self.s_out, "Which item do you wish to pick up?\n", print_border=True)
        for i, item in enumerate(nl):
            s_print(self.s_out, "{}) {}".format(i+1, item[1].occupant.name), print_border=True)

        s_print(self.s_out, "> ", end='', print_border=True)

        num = int(self.s_in.readline().rstrip())

        if num in range(1, len(nl) + 1):
            self._player.pickup_item(nl[num - 1][1].occupant)
            self._map.displace_occupant(nl[num - 1][0]) # contains position tuple
        else:
            s_print(self.s_out, "Invalid item number.", print_border=True)
        self._map.display()

    def _cmd_drop(self):
        self._map.display()

    def _cmd_clear(self):
        self._map.display()

    def _cmd_attack(self):
        nl = self._map.surrounding_characters(position=self._player.position)

        if not nl:
            s_print(self.s_out, "No nearby combatants to attack.", print_border=True)
            return
        elif len(nl) is 1:
            combatant = self._map._grid[nl[0][0][0]][nl[0][0][1]].occupant
            self._new_combat_instance(combatant)
            return

        # else, multiple nearby combatants
        s_print(self.s_out, "Which combatant do you choose to engage in combat?\n", print_border=True)
        for i, combatant in enumerate(nl):
            s_print(self.s_out, "{}) {}".format(i+1, combatant[1].occupant.name))

        s_print(self.s_out, "> ", end='')
        num = int(self.s_in.readline().rstrip())

        if num in range(1, len(nl) + 1):
            combatant = self._map._grid[nl[num-1][0][0]][nl[num-1][0][1]].occupant
            self._new_combat_instance(combatant) # contains position tuple
        else:
            s_print(self.s_out, "Invalid combatant number.", print_border=True)

    def play(self):
        all_cmds = {
            'GO': lambda direction: self._cmd_go(direction),
            'ATTACK': lambda ignore: self._cmd_attack(),
            'HEALTH': lambda ignore: self._cmd_health(),
            'INVENTORY': lambda ignore: self._cmd_inventory(),
            'QUIT': lambda ignore: self._cmd_quit(),
            'EXIT': lambda ignore: self._cmd_quit(),
            'HELP': lambda ignore: self._cmd_help(),
            'PICKUP': lambda ignore: self._cmd_pickup(),
            'DROP': lambda ignore: self._cmd_drop(),
            'CLEAR': lambda ignore: self._cmd_clear()
        }
        last_cmd = None
        self._map.display()

        try:
            while True:
                if self.win_condition(self._player, self._goal):
                    s_print(self.s_out, "You've won!", print_border=True)
                    break

                s_print(self.s_out, "> ", end='', print_border=True)
                cmd = self.s_in.readline().rstrip().split()
                cmd = (cmd[0], None) if len(cmd) is 1 else cmd
                try:
                    if cmd[0].upper() in all_cmds.keys():
                        last_cmd = cmd
                        all_cmds[cmd[0].upper()](list(cmd[1:]))
                    else:
                        s_print(self.s_out, "ERROR: Invalid command.", print_border=True)
                except UserWarning:
                    e = sys.exc_info()[1].args[0] # this is the exception message
                    s_print(self.s_out, "ERROR: {}".format(e), print_border=True)
                except IndexError:
                    try:
                        all_cmds[last_cmd[0].upper()](list(last_cmd[1:]))
                    except (IndexError, TypeError):
                        s_print(self.s_out)
                        continue
        except (EOFError, KeyboardInterrupt):
            s_print(self.s_out, "Exiting Fatal Error. Goodbye.", print_border=True)
            self._cmd_quit()

