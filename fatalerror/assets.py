"""
assets
~~~~~~

"""
from fatalerror.character import Character
from fatalerror.item import Item
from fatalerror.role import Role, Enemy, Player
from fatalerror.function import Function, Storage, Weapon, Food

# r_name specifies a list of Roles instantiated from same Role subclass
r_player = {}
r_player['h4x0r']        = Player(health=30, strength=8, defense=10,
                                  title="H4X0R", symbol='P')
r_player['code_warrior'] = Player(health=30, strength=10, defense=8,
                                  title="CodeWarrior", symbol='P')

r_enemy = {}
r_enemy['EvilRobot'] = Enemy(health=15, strength=9, defense=7,
                             title="EvilRobot", symbol='E')

# f_name specifies a list of Functions instantiated from same Function subclass
f_storage = {}
f_storage['Backpack'] = Storage(durability=100, inventory_size = 0,
                                title="Backpack", symbol='B',
                                capacity='16', inventory=[])

f_weapon = {}

f_food = {}
