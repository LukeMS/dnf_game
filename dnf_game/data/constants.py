"""Some constant values used by the game."""

TILE_W = TILE_H = 32
BASE_TILESET = "DejaVuSansMono-Bold{}.png".format(TILE_W)

# Screen width
SCR_W = 1024
# Number of screen columns (each with tile width)
SCR_COLS = SCR_W // TILE_W

# Screen height
SCR_H = 768
# Number of screen rows (each with tile height)
SCR_ROWS = SCR_H // TILE_H

MAP_COLS = 40 * 2
MAP_ROWS = 24 * 2

FPS = 30

DEBUG = False

FOV_RADIUS = 6
EXPLORE_RADIUS = 3

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 5
MAX_ROOMS = 30

MAX_ROOM_MONSTERS = 3


HEAL_AMOUNT = 4

LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5

FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8

# experience and level-ups
LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150
