"""Test Scene for manager using pysdl2."""

import unittest


from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.dnf_main import data_handler


class PySDL2Tiles2Test(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(
            scene=ScenePySDL2Tiles2Test, test=False).execute()


class ScenePySDL2Tiles2Test(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        # manager = self.manager
        factory = self.factory
        # tile_size = manager.tile_size
        tile = "floor"
        data = data_handler.get_tile_data(tile)
        self.sprite = factory.from_tileset(tile=tile, var=0, pos=0)

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprite)

if __name__ == '__main__':
    unittest.main(verbosity=2)
