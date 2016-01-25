#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import ai
from . import bots
from . import models
from .client import *

TAVERN = 0
AIR = -1
WALL = -2

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

# command values
NORTH = 'North'
SOUTH = 'South'
WEST = 'West'
EAST = 'East'
STAY = 'Stay'

DIR_NORTH = (0, -1)
DIR_SOUTH = (0, 1)
DIR_WEST = (-1, 0)
DIR_EAST = (1, 0)
DIR_STAY = (0, 0)

AIM = {'North': DIR_NORTH,
       'East': DIR_EAST,
       'South': DIR_SOUTH,
       'West': DIR_WEST}
