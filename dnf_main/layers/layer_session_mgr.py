"""Manage creation, saving and loading of game sessions and levels."""

import os
import sys
WP = os.path.join(os.path.dirname(__file__), '..', '..')
if __name__ == '__main__':
    sys.path.insert(0, WP)

from dnf_main.map_entities import PCreature, Cursor
from dnf_main.map_gen import rnd_gen, populate_level
from dnf_main.map_containers import MapContainer, MapHeader
from scene_manager.layers.base_layers import LogicLayer
from util import tile_fx, packer


def clear_savedir():
    """Clear a previous session."""
    if os.path.isdir('save'):
        for root, path, files in os.walk('save'):
            for f in files:
                os.remove(os.path.join(root, f))
        os.removedirs('save')


def ensure_savedir():
    """Create the save directory if not present."""
    path = os.path.join(WP, 'save')
    if not os.path.exists(path):
        os.makedirs(path)


class SessionMgr(LogicLayer):
    """Handle session creation, saving and loading.

    Parent scene's map related procedures (creating ccontainers, creating,
    storing and retrieving maps) is done here.
    """

    def __init__(self, character, new, **kwargs):
        """Initialization.

        Args:
            character (PCreature): the character
            created by the player, if coming from a new game
            new (bool): True for a new game, False otherwise

        Kwargs:
            parent (SceneMap): The parent scene (implicity required by super)
        """
        super().__init__(**kwargs)

        if new:
            self.new_game(character)
        else:
            self.load_game()

    def new_game(self, character):
        """Start a new session."""
        clear_savedir()
        scene = self.parent

        scene.turn = 0
        scene.maps = MapContainer()
        scene.tile_fx = tile_fx.TileFx(scene=scene)
        map_header = MapHeader(name="dungeon0", level=1, split=0, cr=0,
                               mode=scene.mode)
        self.new_level(map_header, character)

        scene.cursor = Cursor(scene=scene)

    def new_level(self, header, character):
        """Create a new map level for the session."""
        scene = self.parent

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
            current_level.set_tile_variation()
            current_level.set_tiling_index()
            for tile in current_level.tiles:
                tile.scene = scene

        scene.player = PCreature(scene=scene, pos=(0, 0),
                                 combat=character)
        scene.player.set_starting_position(pos=scene.current_level._start,
                                           header=scene.current_level.header)

        scene.player.active = True
        scene.state = 'playing'

    def load_game(self):
        """Load a game session."""
        scene = self.parent

        with packer.zshelf_open(
                os.path.join(WP, 'save', 'savegame'), 'r') as shelf_file:
            scene.maps = shelf_file['maps']

            for att, value in shelf_file['scene'].items():
                setattr(scene, att, value)

            current_level = scene.current_level

            scene.player = shelf_file['player']

            scene.add_obj(scene.player, scene.player.pos)

            scene.tile_fx = tile_fx.TileFx(scene=scene)
            scene.cursor = Cursor(scene=scene)

            [setattr(entity, 'scene', scene)
             for entity in current_level.entities]

            scene.state = 'playing'

    def save_game(self):
        """Save the game session."""
        scene = self.parent

        scene.state = 'saving'
        ensure_savedir()

        with packer.zshelf_open(
                os.path.join(WP, 'save', 'savegame'), 'n') as shelf_file:

            scene.rem_obj(scene.player, scene.player.pos)
            shelf_file['player'] = scene.player
            shelf_file['scene'] = {att: getattr(scene, att)
                                   for att in ['turn']}
            shelf_file['maps'] = scene.maps
