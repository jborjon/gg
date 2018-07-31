# __init__.py
#
# This file initializes the GameGenerator (GG) package, which needs to
# be imported in order to create your very own Flak game.
#
# If you're interested in figuring out how this code works, go ahead:
# look through it, change it - even break it if you need to. You may run
# into stuff we didn't talk about in class, but don't let that stop you.
# Just Google around :)
#
# GameGenerator is free to use, modify, and redistribute for any purpose
# that is both educational and non-commercial, as long as this paragraph
# remains unmodified and in its entirety in a prominent place in all
# significant portions of the final code. No warranty, express or
# implied, is made regarding the merchantability, fitness for a
# particular purpose, or any other aspect of the software contained in
# this module.
#
# Okay, enough preamble. Enjoy!

"""GameGenerator - A simple 2D game engine for creating Flak games.

GG amounts to a small, simple game engine for making little Flak-style
2D games. Its intended clients are Mr. Borjon's awesome 6th-grade
students.

Flak, the style of game supported by GG, consists of a player on the
ground (the bottom of the screen) attempting to shoot down enemy planes
performing their bombing runs. The player and the ground structures the
player defends must survive, with the player reloading every few shots
when out of ammo (with unlimited reloads). It's fast-paced, challenging,
and exciting!
"""

__author__ = 'Mr. Joseph Borjon'
__email__ = 'work@josephborjon.com'
__license__ = 'Free with restrictions (see file headers)'
__version__ = '0.1.0'
__credits__ = ['Joseph Borjon']
__date__ = '2017-11-13'
__status__ = 'Development'

from gg.game import Game
from gg.player import Player
from gg.enemy import Enemy
from gg.ammo import Ammo
from gg.groundobject import GroundObject
from gg.thumbnail import Thumbnail
from gg.polardialogbox import PolarDialogBox
from gg.colors import *
