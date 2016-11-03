"""Manage creation, saving and loading of game sessions and levels."""

import os

import sprite
import tile_fx
from map_gen import rnd_gen, populate_level
from game_types import MapContainer, MapHeader
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

    def __init__(self, scene, character):
        """Initialization.

        Parameters:
            scene: level scene instance;

        Returns:
            self: instance.
        """
        self.scene = scene
        self.game = scene.game
        scene.player = sprite.Player(scene=scene, x=0, y=0,
                                     combat=character)
        print(scene.player.combat)

    def new_game(self):
        """Start a new session."""
        clear_savedir()

        self.scene.turn = 0
        self.scene.maps = MapContainer()
        self.scene.tile_fx = tile_fx.TileFx(scene=self.scene)
        map_header = MapHeader(name="dungeon0", level=1, split=0, cr=0,
                               mode='RndMap2')
        self.new_level(map_header)
        self.scene.cursor = sprite.Cursor(scene=self.scene)

    def new_level(self, header):
        """Create a new map level for the session."""
        scene = self.scene

        scene.state = 'loading'

        # TODO use try/except to handle first level (no record of player)
        if scene.current_level:
            try:
                scene.rem_obj(scene.player, "creatures", scene.player.pos)
            except AttributeError:
                pass

        # going back to a level that already exists
        if header in scene.maps:
            # set the level number so that dynamic @properties will use it
            scene.maps.set_current(header)
        else:
            # going to a new level - or the first one
            # set the level number so that dynamic @properties will use it

            scene.maps.add(rnd_gen.create_map(header=header))
            scene.maps.set_current(header)
            current_level = scene.current_level
            populate_level.populate(scene=scene, _map=current_level)
            check_func = self.game.tilesets.get_tile_maximum_variation
            current_level.set_tile_variation(check_func=check_func)
            current_level.set_tiling_index()

        scene.player.set_starting_position(pos=scene.current_level._start,
                                           header=scene.current_level.header)

        scene.set_fov()

        scene.player.active = True
        scene.state = 'playing'

    def load_game(self):
        """Load a game session."""
        scene = self.scene

        with packer.zshelf_open(
                os.path.join('save', 'savegame'), 'r') as shelf_file:
            scene.maps = shelf_file['maps']

            for att, value in shelf_file['scene'].items():
                setattr(scene, att, value)

            current_level = scene.current_level

            scene.player = shelf_file['player']

            scene.add_obj(scene.player, 'creatures', scene.player.pos)

            scene.tile_fx = tile_fx.TileFx(scene=scene)
            scene.cursor = sprite.Cursor(scene=scene)

            for creature in current_level.creatures:
                creature.scene = scene

            for obj in current_level.objects:
                obj.scene = scene

            scene.current_level.set_fov()

            scene.state = 'playing'

    def save_game(self):
        """Save the game session."""
        scene = self.scene

        scene.state = 'saving'
        scene.msg.text = "Fear not, for your deeds shall not be forgotten..."
        ensure_savedir()

        with packer.zshelf_open(
                os.path.join('save', 'savegame'), 'n') as shelf_file:

            current_level = scene.current_level

            scene.rem_obj(scene.player, 'creatures', scene.player.pos)
            current_level['player_pos'] = scene.player.pos
            shelf_file['player'] = scene.player

            scene = {att: getattr(scene, att)
                     for att in ['current_level', 'turn', "offset"]}

            shelf_file['scene'] = scene

            shelf_file['maps'] = scene.maps
