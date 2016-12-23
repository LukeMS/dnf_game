"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes.base_scenes import SceneMultiLayer
from dnf_game.scene_manager.layers.base_layers import Inventory


class InventoryTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneInventoryTest, test=True).execute()


class SceneInventoryTest(SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        inventory = Inventory(parent=self)
        self.insert_layer(inventory)


if __name__ == '__main__':
    unittest.main(verbosity=2)
