"""Test Scene for manager using pysdl2."""

import random
import unittest

import sdl2

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes


class TilesTextPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(
            scene=SceneTilesTextPySDL2, test=False).execute()


class SceneTilesTextPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.ignore_regular_update = True
        manager = self.manager
        factory = manager.factory
        w, h = manager.width, manager.height

        tiles = set()
        tile_size = manager.tile_size
        possible_tiles = tile_shuffler(16, 42, tile_size)
        pos = tile_shuffler(w // tile_size, h // tile_size, tile_size)
        for x, y in pos:
            i, j = random.choice(possible_tiles)
            sprite = factory.from_tileset(area=(i, j, tile_size, tile_size))
            sprite.position = x, y
            tiles.add(sprite)
        self.tiles = tiles
        self.pos = pos
        self.on_update()

    def modify(self, sprite):
        """..."""
        color = [random.randrange(255) for i in range(3)]
        sprite.set_color_mod(color)

        alpha = random.randrange(127) * 2 + 1
        sprite.set_alpha_mod(alpha)

    def on_key_press(self, event, mod):
        """..."""
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()
        self.on_update()

    def on_update(self):
        """..."""
        def set_tile_position(tile, value):
            tile.position = value
            self.modify(tile)

        manager = self.manager
        manager.renderer.clear()
        tiles = self.tiles

        pos = list(self.pos)
        random.shuffle(pos)

        {set_tile_position(tile, p) for tile, p in zip(tiles, pos)}

        manager.spriterenderer.render(sprites=tiles)

        manager.present()


def tile_shuffler(w, h, tile_size):
    """Create the xy coordinates in the possible range and shuffle them.

    Args:
        w (int): width of the tileset
        h (int): height of the tileset

    Returns:
        list of tuples with coordinates (x, y)

    """
    l = [(x * tile_size, y * tile_size) for x in range(w) for y in range(h)]
    random.shuffle(l)
    return l

if __name__ == '__main__':
    unittest.main(verbosity=2)
