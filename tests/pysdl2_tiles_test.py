"""Test Scene for manager using pysdl2."""

import random
import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from constants import TILE_W, TILE_H
from manager import Manager
from manager.scenes import base_scenes


class TestSceneTiles(unittest.TestCase):
    """..."""

    def test_scene(self):
        """..."""
        Manager(scene=SceneTiles).execute()


class SceneTiles(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        manager = self.manager
        factory = manager.factory
        tileset = manager.tileset
        w, h = manager.width, manager.height

        tiles = set()
        possible_tiles = tile_shuffler(16, 42)
        pos = tile_shuffler(w // TILE_W, h // TILE_H)
        for x, y in pos:
            i, j = random.choice(possible_tiles)
            sprite = factory.from_tileset(
                tileset, (i, j, TILE_W, TILE_H))
            sprite.position = x, y
            tiles.add(sprite)
        self.tiles = tiles
        self.pos = pos

    def on_update(self):
        """..."""
        def set_tile_position(tile, value):
            tile.position = value

        manager = self.manager
        tiles = self.tiles

        pos = list(self.pos)
        random.shuffle(pos)

        {set_tile_position(tile, p) for tile, p in zip(tiles, pos)}

        manager.spriterenderer.render(sprites=tiles)


def tile_shuffler(w, h):
    """Create the xy coordinates in the possible range and shuffle them.

    Args:
        w (int): width of the tileset
        h (int): height of the tileset

    Returns:
        list of tuples with coordinates (x, y)

    """
    l = [(x * TILE_W, y * TILE_H) for x in range(w) for y in range(h)]
    random.shuffle(l)
    return l

if __name__ == '__main__':
    unittest.main(verbosity=2)
