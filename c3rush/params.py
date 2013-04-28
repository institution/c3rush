# coding: utf-8


from engine import vec
from functools import partial



GAME_SIZE = vec(912, 688)
SIDEPANEL_SIZE = 112

MEDIUM_SIZE = vec(48,48)
SMALL_SIZE = vec(24,24)

FIELD_DIM = 24

TRUCK_MAX_VELOCITY = 10.0          # m/s
TRUCK_STORE_SPACE = 10.0
TRUCK_TANK_SIZE = 4.0

DAY_TIME = 30.0
NIGHT_TIME = 30.0

# standardowa jednostka węgla 1kg
COAL_UNIT_VOLUME = 1.0	#dm3   -jaka objetość zajmuje 1 kg
METAL_UNIT_VOLUME = 1.0	#dm3   -jaka objetość zajmuje 1 kg


MEDIUM_HEALTH= 80

MUTANT_HEALTH = 8
MGPOST_HEALTH = 50
TRUCK_HEALTH = 10
FACTORY_HEALTH = 100
RECYCLER_HEALTH = 100
MINE_HEALTH = 100
GENERATOR_HEALTH = 100
TRANSMITER_HEALTH = 10
CONTROLPOST_HEALTH = 100