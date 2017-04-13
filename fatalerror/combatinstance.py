"""
combatinstance
~~~~~~~~

Defines a combat instance.

"""
import time
from random import randint

from fatalerror.terminal import s_print


class CombatInstance(object):
    def __init__(self, c1, c2, s_out, s_in):
        self.player = c1
        self.enemy = c2
        # initialize attacker and player
        self.attacker = self.player
        self.defender = self.enemy

        self.s_out, self.s_in = s_out, s_in

    def fight(self):
        while self.attacker.health > 0 and self.defender.health > 0:
            damage = CombatInstance.calculate_damage(self.attacker.strength,
                                                     self.defender.defense)
            if damage <= 0:
                evade_msg = "{} evades {}'s attack!"
                s_print(self.s_out, evade_msg.format(self.defender.name,
                                                     self.attacker.name),
                                                     print_border=True)
            else:
                self.defender.health -= damage
                damage_msg = "{} attacks {} for {} damage!"
                s_print(self.s_out, damage_msg.format(self.defender.name,
                                                      self.attacker.name,
                                                      damage), print_border=True)

            s_print(self.s_out, '\n', end='')
            # switch attacker and defender
            self.attacker, self.defender = self.defender, self.attacker
            time.sleep(.5)

        return [x for x in [self.player, self.enemy] if x.health <= 0][0]

    @staticmethod
    def calculate_damage(att_strength, def_defense):
        return randint(0, 6) + att_strength - def_defense
