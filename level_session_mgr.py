"""Manage creation, saving and loading of game sessions and levels."""

import os

import sprite
import gamemap
import tile_fx
from map_gen import rnd_gen, populate_level
from common import packer


def clear_savedir():
    """Clear a previous session."""
    if os.path.isdir('save'):
        for root, path, files in os.walk('save'):
            for f in files:
                os.remove(os.path.join(root, f))
        os.removedirs('save')


def ensure_savedir():
    """Create the save directory if not present."""
    if not os.path.exists('save'):
        os.makedirs('save')


class SessionMgr(object):
    """Handle session creation, saving and loading."""

    def __init__(self, level_scene):
        """Initialization.

        Parameters:
            level_scene: level scene instance;

        Returns:
            self: instance.
        """
        self.level_scene = level_scene
        self.parent = self.level_scene.parent

    def new_game(self):
        """Start a new session."""
        level_scene = self.level_scene
        parent = self.parent

        parent.transition("Creating a world of treasures and dangers...")
        clear_savedir()

        level_scene.turn = 0
        level_scene.levels = {}
        level_scene.tile_fx = tile_fx.TileFx(scene=level_scene)
        self.new_level()
        level_scene.cursor = sprite.Cursor(scene=level_scene)

    def new_level(self, level_n=0):
        """Create a new map level for the session."""
        level_scene = self.level_scene

        level_scene.game_state = 'loading'
        mode = level_scene.mode

        # not the first level
        if len(level_scene.levels) > 0:
            # clean up the current level
            level_scene.rem_obj(level_scene.player, 'creatures',
                                level_scene.player.pos)
            current_level = level_scene.levels[level_scene.current_level]
            current_level['groups']['creatures'] = []
            current_level['groups']['objects'] = []
            current_level['player_pos'] = level_scene.player.pos
            current_level = packer.zshelf_pack(current_level)

        # going back to a level that already exists
        if level_n in level_scene.levels:
            # set the level number so that dynamic @properties will use it
            level_scene.current_level = level_n
            level_scene.levels[level_n] = packer.zshelf_load(
                level_scene.levels[level_n])

            self.set_groups()

            # recover player pos - should set it to stairs?
            level_scene.player.pos = level_scene.levels[level_n]['player_pos']
            level_scene.add_obj(level_scene.player, 'creatures',
                                level_scene.player.pos)

        else:
            # going to a new level - or the first one
            # set the level number so that dynamic @properties will use it
            level_scene.current_level = level_n
            level_scene.levels[level_n] = {}
            level_scene.levels[level_n]['tile_fx'] = []
            level_scene.levels[level_n]['grid'] = {}
            level_scene.levels[level_n]['rooms'] = []
            level_scene.levels[level_n]['halls'] = []

            level_scene.grid = gamemap.Map(scene=level_scene)
            map_mgr = getattr(level_scene, "map_mgr", None)
            if map_mgr is None:
                level_scene.map_mgr = gamemap.MapMgr(scene=level_scene)

            if mode != 'default':
                if mode == 'pit':
                    grid, rooms, halls, w, h = rnd_gen.Pit().make_map()
            else:
                grid, rooms, halls, w, h = rnd_gen.RndMap().make_map()

            for pos, tile in grid.items():
                level_scene.levels[level_n]['grid'][pos] = {
                    "feature": tile,
                    "objects": [],
                    "creatures": [],
                    "changed": False,
                    "owner": None
                }

            level_scene.levels[level_n]['width'] = w
            level_scene.levels[level_n]['height'] = h

            level_scene.levels[level_n]['groups'] = {
                'rooms': rooms,
                'halls': halls,
                'creatures': [],
                'objects': []
            }

            populate_level.populate(level_n, level_scene, grid, rooms)

            check_func = level_scene.gfx.tileset_mgr.get_tile_maximum_variation
            level_scene.map_mgr.set_tile_variation(check_func=check_func)
            level_scene.map_mgr.set_tiling_index()

            level_scene.add_obj(level_scene.player, 'creatures',
                                level_scene.player.pos)

        level_scene.map_mgr.set_fov()

        level_scene.player.active = True
        level_scene.game_state = 'playing'

    def set_groups(self):
        """Set groups per object type to facilitate referencing."""
        level_scene = self.level_scene

        level_dict = level_scene.levels[level_scene.current_level]

        for _type in ['creatures', 'objects']:
            for pos in level_dict['grid']:
                if _type in pos:
                    for obj in level_dict['grid'][pos][_type]:
                        level_dict[_type].append(obj)

    def load_game(self):
        """Load a game session."""
        level_scene = self.level_scene

        with packer.zshelf_open(
                os.path.join('save', 'savegame'), 'r') as shelf_file:
            level_scene.levels = shelf_file['levels']

            for att, value in shelf_file['scene'].items():
                setattr(level_scene, att, value)

            level_dict = level_scene.levels[level_scene.current_level]

            level_scene.player = shelf_file['player']

            self.set_groups()
            level_scene.player.pos = level_dict['player_pos']
            level_scene.add_obj(level_scene.player, 'creatures',
                                level_scene.player.pos)

            level_scene.grid = gamemap.Map(scene=level_scene)
            level_scene.map_mgr = gamemap.MapMgr(scene=level_scene)
            level_scene.tile_fx = tile_fx.TileFx(scene=level_scene)
            level_scene.cursor = sprite.Cursor(scene=level_scene)

            for creature in level_dict['groups']['creatures']:
                creature.scene = level_scene

            for obj in level_dict['groups']['objects']:
                obj.scene = level_scene

            level_scene.map_mgr.set_fov()

            level_scene.game_state = 'playing'

    def save_game(self):
        """Save the game session."""
        level_scene = self.level_scene
        parent = self.parent

        parent.transition(
            "Fear not, for your deeds shall not be forgotten...")
        level_scene.game_state = 'saving'
        ensure_savedir()

        with packer.zshelf_open(
                os.path.join('save', 'savegame'), 'n') as shelf_file:

            current_level = level_scene.levels[level_scene.current_level]

            level_scene.rem_obj(level_scene.player, 'creatures',
                                level_scene.player.pos)
            current_level['player_pos'] = level_scene.player.pos
            shelf_file['player'] = level_scene.player

            scene = {att: getattr(level_scene, att)
                     for att in ['current_level', 'turn', "offset"]}

            shelf_file['scene'] = scene

            current_level['groups']['creatures'] = []
            current_level['groups']['objects'] = []

            shelf_file['levels'] = level_scene.levels
