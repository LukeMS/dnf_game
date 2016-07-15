"""Manage the session: load/save game, new/load/save level."""

import os

from constants import SCREEN_ROWS, MAP_ROWS, SCREEN_COLS, MAP_COLS
import sprite
import gamemap
import tile_fx
import rnd_gen
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


def new_game(session):
    """Start a new session."""
    clear_savedir()
    session.turn = 0

    session.levels = {}

    session.max_y = max(SCREEN_ROWS, MAP_ROWS)
    session.max_x = max(SCREEN_COLS, MAP_COLS)

    session.tile_fx = tile_fx.TileFx(scene=session)
    new_level(session)

    session.cursor = sprite.Cursor(scene=session)


def new_level(session, level=0):
    """Create a new map level for the session."""
    session.game_state = 'loading'

    # not the first level
    if len(session.levels) > 0:
        # clean up the current level
        session.rem_obj(session.player, 'creatures', session.player.pos)
        current_level = session.levels[session.current_level]
        current_level['groups']['creatures'] = []
        current_level['groups']['objects'] = []
        current_level['player_pos'] = session.player.pos
        current_level = packer.zshelf_pack(current_level)

    # going back to a level, it already exists
    if level in session.levels:
        # set the level number, properties will follow it
        session.current_level = level
        session.levels[level] = packer.zshelf_load(session.levels[level])
        #

        session.set_groups()

        # recover player pos - should set it to stairs?
        session.player.pos = session.levels[level]['player_pos']
        session.add_obj(session.player, 'creatures', session.player.pos)

    else:
        # going to a new level - or the first one
        # set the level number, properties will follow it
        session.current_level = level
        session.levels[level] = {}
        session.levels[level]['tile_fx'] = []
        session.levels[level]['grid'] = {}
        session.levels[level]['rooms'] = []
        session.levels[level]['halls'] = []

        session.grid = gamemap.Map(scene=session)
        map_mgr = getattr(session, "map_mgr", None)
        if map_mgr is None:
            session.map_mgr = gamemap.MapMgr(scene=session)

        grid, rooms, halls = rnd_gen.RndMap().make_map(
            width=MAP_COLS, height=MAP_ROWS)

        for pos, tile in grid.items():
            session.levels[level]['grid'][pos] = {
                "feature": tile,
                "objects": [],
                "creatures": [],
                "changed": False,
                "owner": None
            }

        session.levels[level]['groups'] = {
            'rooms': rooms,
            'halls': halls,
            'creatures': [],
            'objects': []
        }

        session.map_mgr.place_objects()
        session.map_mgr.set_tile_variation(
            check_func=session.gfx.tileset_mgr.get_tile_maximum_variation)
        session.map_mgr.set_tiling_index()
        session.add_obj(session.player, 'creatures', session.player.pos)

    # TODO export map templates
    # pygame.Image.save(mySurface, 'myimagefile.png')

    session.map_mgr.set_fov()

    session.player.active = True
    session.game_state = 'playing'


def set_groups(session):
    """..."""
    level_dict = session.levels[session.current_level]

    for _type in ['creatures', 'objects']:
        for pos in level_dict['grid']:
            if _type in pos:
                for obj in level_dict['grid'][pos][_type]:
                    level_dict[_type].append(obj)


def load_game(session):
    """..."""
    with packer.zshelf_open(
            os.path.join('save', 'savegame'), 'r') as shelf_file:
        session.levels = shelf_file['levels']

        for att, value in shelf_file['scene'].items():
            setattr(session, att, value)

        level_dict = session.levels[session.current_level]

        session.player = shelf_file['player']

        set_groups(session)
        session.player.pos = level_dict['player_pos']
        session.add_obj(session.player, 'creatures', session.player.pos)

        session.grid = gamemap.Map(scene=session)
        session.map_mgr = gamemap.MapMgr(scene=session)
        session.tile_fx = tile_fx.TileFx(scene=session)
        session.cursor = sprite.Cursor(scene=session)

        for creature in level_dict['groups']['creatures']:
            creature.scene = session

        for obj in level_dict['groups']['objects']:
            obj.scene = session

        session.map_mgr.set_fov()

        session.game_state = 'playing'


def save_game(session):
    """..."""
    session.game_state = 'saving'
    ensure_savedir()

    with packer.zshelf_open(
            os.path.join('save', 'savegame'), 'n') as shelf_file:

        current_level = session.levels[session.current_level]

        session.rem_obj(session.player, 'creatures', session.player.pos)
        current_level['player_pos'] = session.player.pos
        shelf_file['player'] = session.player

        scene = {}
        for att in ['current_level', 'turn', "max_y", "max_x", "offset"]:
            scene[att] = getattr(session, att)
        shelf_file['scene'] = scene

        current_level['groups']['creatures'] = []
        current_level['groups']['objects'] = []

        shelf_file['levels'] = session.levels
