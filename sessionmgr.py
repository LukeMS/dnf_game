import os
import pickle
from pickle import Pickler, Unpickler
from io import BytesIO
import shelve
import bz2

from constants import SCREEN_ROWS, MAP_ROWS, SCREEN_COLS, MAP_COLS
import sprite
import gamemap
import tile_fx


def clear_savedir():

    if os.path.isdir('save'):
        for root, path, files in os.walk('save'):
            for f in files:
                os.remove(os.path.join(root, f))
        os.removedirs('save')


def ensure_savedir():
    if not os.path.exists('save'):
        os.makedirs('save')

"""
    new_game
    new_level
    load_game
    save_game

Those are actual methods of the LevelScene class.
They should be properly splitted apart from it soon, possibly using an event
dispatcher.
For now, they're only phisically stored apart to keep things "organized".
"""


def new_game(self):
    clear_savedir()
    self.turn = 0

    self.levels = {}

    self.max_y = max(SCREEN_ROWS, MAP_ROWS)
    self.max_x = max(SCREEN_COLS, MAP_COLS)

    self.tile_fx = tile_fx.TileFx(scene=self)
    self.new_level()

    self.cursor = sprite.Cursor(scene=self)


def new_level(self, level=0):
    self.game_state = 'loading'

    # not the first level
    if len(self.levels) > 0:
        # clean up the current level
        self.rem_obj(self.player, 'creatures', self.player.pos)
        self.levels[self.current_level]['groups']['creatures'] = []
        self.levels[self.current_level]['groups']['objects'] = []
        self.levels[self.current_level]['player_pos'] = self.player.pos
        self.levels[self.current_level] = bz2.compress(pickle.dumps(
            self.levels[self.current_level]))

    # going back to a level, it already exists
    if level in self.levels:
        # set the level number, properties will follow it
        self.current_level = level
        self.levels[self.current_level] = pickle.loads(bz2.decompress(
            self.levels[self.current_level]))
        #

        self.set_groups()

        # recover player pos - should set it to stairs?
        self.player.pos = self.levels[level]['player_pos']
        self.add_obj(self.player, 'creatures', self.player.pos)

    else:
        import rnd_gen
        # going to a new level - or the first one
        # set the level number, properties will follow it
        self.current_level = level
        self.levels[level] = {}
        self.levels[level]['tile_fx'] = []
        self.levels[level]['grid'] = {}
        self.levels[level]['rooms'] = []
        self.levels[level]['halls'] = []

        self.grid = gamemap.Map(scene=self)
        map_mgr = getattr(self, "map_mgr", None)
        if map_mgr is None:
            self.map_mgr = gamemap.MapMgr(scene=self)

        grid, rooms, halls = rnd_gen.RndMap().make_map(width=MAP_COLS, height=MAP_ROWS)

        for pos, tile in grid.items():
            self.levels[level]['grid'][pos] = {
                "feature": tile,
                "objects": [],
                "creatures": [],
                "changed": False,
                "owner": None
            }

        self.levels[level]['groups'] = {
            'rooms': rooms,
            'halls': halls,
            'creatures': [],
            'objects': []
        }

        self.map_mgr.place_objects()
        self.map_mgr.set_tile_variation(
            check_func=self.gfx.tileset_mgr.get_tile_maximum_variation)
        self.map_mgr.set_tiling_index()
        self.add_obj(self.player, 'creatures', self.player.pos)

    self.map_mgr.set_fov()

    self.player.active = True
    self.game_state = 'playing'


def set_groups(self):
    level_dict = self.levels[self.current_level]

    for _type in ['creatures', 'objects']:
        for pos in level_dict['grid']:
            if _type in pos:
                for obj in level_dict['grid'][pos][_type]:
                    level_dict[_type].append(obj)


def load_game(self):
    with zshelf_open(os.path.join('save', 'savegame'), 'r') as shelf_file:
        self.levels = shelf_file['levels']

        for att, value in shelf_file['scene'].items():
            setattr(self, att, value)

        level_dict = self.levels[self.current_level]

        self.player = shelf_file['player']

        self.set_groups()
        self.player.pos = level_dict['player_pos']
        self.add_obj(self.player, 'creatures', self.player.pos)

        self.grid = gamemap.Map(scene=self)
        self.map_mgr = gamemap.MapMgr(scene=self)
        self.tile_fx = tile_fx.TileFx(scene=self)
        self.cursor = sprite.Cursor(scene=self)

        for creature in level_dict['groups']['creatures']:
            creature.scene = self

        for obj in level_dict['groups']['objects']:
            obj.scene = self

        self.map_mgr.set_fov()

        self.game_state = 'playing'


def save_game(self):
    self.game_state = 'saving'
    ensure_savedir()

    with zshelf_open(os.path.join('save', 'savegame'), 'n') as shelf_file:
        self.rem_obj(self.player, 'creatures', self.player.pos)
        self.levels[self.current_level]['player_pos'] = self.player.pos
        shelf_file['player'] = self.player

        scene = {}
        for att in ['current_level', 'turn', "max_y", "max_x", "offset"]:
            scene[att] = getattr(self, att)
        shelf_file['scene'] = scene

        self.levels[self.current_level]['groups']['creatures'] = []
        self.levels[self.current_level]['groups']['objects'] = []

        shelf_file['levels'] = self.levels


class ZShelf(shelve.Shelf):
    """
    A simple subclassing of shelve.Shelf to compress/uncompress the saved
    pickles with bz2, generating smaller saved game files.
    """
    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            f = BytesIO(
                bz2.decompress(self.dict[key.encode(self.keyencoding)]))
            value = Unpickler(f).load()
        return value

    def __setitem__(self, key, value):
        f = BytesIO()
        p = Pickler(f, self._protocol)
        p.dump(value)
        self.dict[key.encode(self.keyencoding)] = bz2.compress(f.getvalue())


class DbfilenameZShelf(ZShelf):
    def __init__(self, filename, flag='c'):
        import dbm
        super().__init__(dbm.open(filename, flag))


def zshelf_open(filename, flag='c'):
    return DbfilenameZShelf(filename, flag)
