# Fatal Error

The name of our game is Fatal Error, a networked text-based RPG – an old-style dungeon crawler.

## Description

There is a single level which is composed of a large world map/grid. As shown below, the player is initially positioned on the leftmost center square. The grid should be randomly initialized with 2 elements: a backpack (the objective) and evil robot army minions (which you can engage in combat with). You start off with 30 health, and must safely make your way to the objective through the evil robot horde!

<img src="https://puu.sh/vii8Q/2eb19034f8.png">

The game _should_ be compatiable with both Python 2 and Python 3, however I am willing to bet there are maybe one or two incompatibilities that I missed.

## In-game Commands

| Command | Action |
| ------- | ------ |
| go [N, S, E, W] | Move one space in a cardinal direction. |
| pickup | Pickup an item in an adjacent square. |
| attack | Attack an enemy in an adjacent square. |
| health | Display current health. |
| inventory | Display all items in inventory. |
| clear | Clear the command output. |
| help | Print this help message. |
| quit | Exit the game. |

_*Pressing enter will repeat the previous command._

## Installation

```
$ git clone https://github.com/seanpianka/Fatal-Error.git && cd Fatal-Error
```

## Playing

To run the game locally: 

    `python game.py`

To run the game server:
    
    `python server.py`

To connect to a running gameserver:

    `telnet 127.0.0.1 9000`

## Technical Details

The game was originally supposed to be a small, text-based game for my Python class' midterm, however I enjoyed working on the project and went a little beyond the requirements of the assignment before turning in my work.

### Class Design

The design of the classes in this project is heavily inspired by the ["Type Object"](http://gameprogrammingpatterns.com/type-object.html) design pattern, which:

#### Type Object

> Allow the flexible creation of new “classes” by creating a single class, each instance of which represents a different type of object.

Essentially, I can create a hollow `Enemy` or `Hero` class, and provide it an object which contains the attributes that the specific instance of the `Enemy`, `Hero`, `Weapon` (etc.) class(es) will take on. You can think of this pattern as similar to dependency injection.

#### Entity

All objects which are seen in the world exist as instances of some `Entity`-derived class (Entity can be thought of as an `abstract` class in this context). The `Entity` model handles universal attributes such as the object's name, visual symbol, and current row/column position within the world map, as shown below:

```python
class Entity(object):
    def __init__(self, name, title, position, symbol):
        self._name = name
        self._title = title
        self._symbol = symbol
        if not position: self._r, self._c = -1, -1
        else:            self._r, self._c = position

        ...
```

Note, `(-1, -1)` is used to denote that the `Entity` instance is not visible on the world map and should be prevented from being displayed.

##### Character

Examining the `Character` class, we can see it's derived from `Entity`, inherting all of the aforementioned attributes, along with the attributes which are designated by the provided `Role` object/instance. The `Role` object instance defines the health, strength, defense, attack, title, and symbol for related objects. 

```python
class Character(Entity):
    def __init__(self, name, role, inventory=[], equipped=None,
                 position=None, symbol=None):
        self._role = role
        self._strength = role.strength
        self._defense = role.defense
        self._health = role.health
        self._inventory = inventory
        self._equipped = equipped
        self._alive = True
        symbol = role.symbol if not symbol else symbol
        super(Character, self).__init__(name, role.title, position, symbol)

    ...
```

However, `Role` and `Entity` are similar in that they both can be considered `abstract`, so additional classes are defined (`Enemy` and `Player`) to denote the difference types of `Role`s that a `Character` instance may assume. In doing so, we allow each `Character` instance to take on the attributes of said `Role`, and behave differently (all of the previously mentioned "evil robots" are `Character` instances who assumed an instance of the `Enemy` role named `r_enemy`, defined to be:

```python
# fatalerror/assets.py

r_player['h4x0r']        = Player(health=30, strength=8, defense=10,
                                  title="H4X0R", symbol='P')
r_player['code_warrior'] = Player(health=30, strength=10, defense=8,
                                  title="CodeWarrior", symbol='P')

r_enemy['EvilRobot'] = Enemy(health=15, strength=9, defense=7, 
                             title="EvilRobot", symbol='E')

f_storage['Backpack'] = Storage(durability=100, inventory_size = 0,
                                title="Backpack", symbol='B',
                                capacity='16', inventory=[])
```

There are unlimited possibilities here with a system like this, as the amount of unique attributes that an `Enemy` role can possess is limited by the creativity of the game designers, and adds to the ease of differentiating the `Player` and `Enemy` roles (and whatever additional roles spawn in the design process).

##### Item

Additionally, the `Item` model was derived from `Entity`, given that just as `Character` instances may exist on the world map, have both unique and common attributes, and maintain fundamental data about their position, name, etc., so too do items require this information.

Similarly defined, the `Item` class requires that an pseudo-`Role`, confusingly named `Function`, instance be provided with the instatiation of the object. The `Function` class provides an extremely similar role to `Role` in that it provides the functionality for the hollow `Item` shell that is created -- attributes such as its `title`, `symbol,` and `inventory_size` (the amount of space it occupies in one's inventory). It is also a de-facto `abstract` class, so there are derived "Functions" for which are actually used in instantiation; these include `Storage`, `Weapon`, and `Food` (although not all of these are present at the moment, the ability to create such `Item`s exists).


#### Combat

An instance of combat, aptly identified as `CombatInstance`, which acts as a [`Mediator`](https://en.wikipedia.org/wiki/Mediator_pattern) between the two active `Character` instances engaged in combat.

```python
class CombatInstance(object):
    def __init__(self, c1, c2, s_out, s_in):
        self.attacker = c1
        self.defender = c2
```


Combat is one of the most limited aspects of the game, as it is essentially a randomized chance where either player deals damage or not, as can be shown by the damage algorithm below:

```python
    @staticmethod
    def calculate_damage(att_strength, def_defense):
        return randint(0, 6) + att_strength - def_defense

    def fight(self):
        while self.attacker.health > 0 and self.defender.health > 0:
            damage = CombatInstance.calculate_damage(self.attacker.strength,
                                                     self.defender.defense)
            if damage <= 0:
                evade_msg = "{} evades {}'s attack!"
                ...
            else:
                self.defender.health -= damage
                ...

            ...
            self.attacker, self.defender = self.defender, self.attacker
            ...

        return [x for x in [self.player, self.enemy] if x.health <= 0][0]
```

Note: I've left `calculate_damage` as a static method as I foresaw possible times where calculating damage outside of an active `CombatInstance` would be useful (for instance, within a shop:the average damage a player could deal with a certain item could be calculated).

It's now apparent where the utility of the `Role` comes in for a `Character`, given that its ability to attack and defend during combats is almost solely determined by their starting abilities (I do not believe this is good game design, but this is the nature of `Fatal Error` at the moment):

Damage is calculated as a very simple arithmetic equation involving a random integer, along with the attacker's strength level minus the defender's defense level. The attacker and defender are swapped each turn in a combat instance, so there is no need to customize the logic to the nature of their being two separate `Character` instances engaged in combat (however, it is limited to only one-vs-one combat).


#### World Map

The world map, identified as the `Grid` class, is essentially a `composition` of `Space` instances:

```python
class Grid:
    def __init__(self, ...):
        self._grid = [[Space() for spc in range(MAX_R)] for row in range(MAX_C)]

    ...
```

where each `Space` is defined as:

```python
class Space(object):
    _grid_symbol = '.'
    def __init__(self, occupant=None):
        self._occupant = None
        self.occupant = occupant
        self._vacant = not occupant
        self._symbol = Space._grid_symbol
        self.symbol = Space._grid_symbol if not occupant else occupant.symbol

    ...
```

These two classes are the way in which `Entity` instances are correctly displayed on the world map. `Grid` comes packed with utility methods purely for this purpose, such as:

* `_generate_walls` - Parse the maps (read in from `maps.txt`), generate the wall boundaries (and mark the spaces as occupied) so that they act as unmovable object which blocks the player's path (no matter how much they believe they're unstoppable forces!).
* `display` - Update the screen, refresh the command window, and re-draw any movement of characters (No A.I. at the moment, so it's only the player's movement).
* `random_emplace_occupant` - Randomly put a provided `Entity` instance onto the map at both a valid row/column position and in a `Space` which is does not have its `vacant` flag enabled.
* `move_occupant` - Move an existing `Grid` occupant to another space; if that `Entity` is not present on the map, emplace them randomly or at a provided position).
* `emplace_occupant` - Emplace an `Entity` instance at a row/column set of coordinates, checks for vacanies.
* `displace_occupant` - Remove an `Entity` instance at a row/column set of coordinates.
* `surrounding_items` - Return a list of `Item` instances located in surrounding squares.
* `surrounding_characters` - Return a list of `Character` instances located in surrounding squares.
* `surrounding_occupants` - Return a list of `Entity` instances located in surrounding squares.
* `_is_in_bounds` - Check if a pair of row/column coordinates is valid.
* `_is_vacant` - Check if a `Space` found at a row/column set of coordinates is vacant.
* `_locate_occupant` - Locate an `Entity` occupying a `Space`, returns `False` if not found.

(for which all definitions are available in `fatalerror/grid.py`).


#### Networking

The networking component to `Fatal Error` is very simple -- it's a homegrown, TCP socket server which allows 10 remote connections to the game server at any one time:

```python
class FatalErrorServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
    ...

    def listen(self):
            ...
            self.sock.listen(10)
            ...
```

Not very fancy, but enough to do the job and allow someone to use `netcat` or `telnet` and remotely play `Fatal Error`! 

##### New Connection

When a new connection is received or dropped, the basic logging will notify any administrator watching the logs that a new player has connected from {address}:{port} (or conversely, has disconnected from the game). 


```python
def client_game_instance(self, client, addr):
    new_conn = "[+] New game client connection from {}:{}".format(addr[0],
                                                                  addr[1])
    print(new_conn, end='')

    ...

    lost_conn = "[-] Lose connection from {}:{}".format(addr[0], addr[1])
    print(lost_conn)

    client.close()
```


Then, a new file descriptor is created for that visitor in order to sent all of the print statements to the user over the connection, while also allowing for user input from the remote client to reach the server.

```python
    try:
        s_out = client.makefile('w', 0)
        s_in = client.makefile('r', 0)
        FatalError(s_out, s_in).play()
    except (socket.error, Exception) as e:
        print(e)
```

This is what all that business about with `s_print`, defined here:

```python
def s_print(_os, *args, **kwargs):
    ...
    print(*args, file=_os, **kwargs)
    _os.flush()

def s_input(_is):
    return _is.readline()

```

Where `_os` and `_is` are output and input streams respectively that the client will read or write data from/to (this is the reason for the original creation of the file descriptors, they are attached to by the client and subsequently used to transmit data to and from the client).

Having a networked game client was one of the requirements of the original project, and I'm happy it was as it lead me down an interesting road which I hadn't explored before. 

I am, however, interested in exploring my advanced options for networked clients and gaming, as I believe the capabilities of a system I've created far exceed what I've managed to achieve here with it.

#### Terminal Modification

I cannot speak much as to the original creation of this class, as it is an amalgam from numerous StackOverflow and Reddit posts, but it (almost) allows me to simulate the switching of frame-buffers that programs like `man`:

```python
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

    ...
```

The `KeyPoller` classes allows me to save and restore the original settings that were set by the user of the terminal, which gives me the freedom to modify the settings however I need in order to display the world map how I desire.

In addition, Python's `__enter__` and `__exit__` constructs allow me to perform very neat tricks like:

```python
with KeyPoller() as kp:
    # perform non-blocking key polling, allows for W, A, S, D as movement keys
    ...
```

Which will automatically convert the terminal to allow for non-blocking key polling, allowing for more smooth movement. However, I originally wasn't able to concoct a solution for this problem (now, with all my experience with `vim`, using `:` as the leader for a command (or "delimiter" is the more proper term, I suppose) would have been the best, most innovative idea).


#### Closing Notes

This was my first foray into any sort of "graphics" programming (if you can really call it that... maybe 2D graphics?), and creating a system of spaces, within what essentially amounts to a table, is the best way I had come up. This was a more-beginner-me who was having difficulties understanding all the idiosyncrasies of the Unix terminal, and a future implementation would likely make more use of a lower level graphics API such as `SFML` or an `OpenGL` library.
