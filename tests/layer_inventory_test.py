"""Test Scene for manager using pysdl2."""

import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scene_manager import Manager
from scene_manager.scenes import base_scenes
from scene_manager.windows import base_windows


class GradientWindowTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=LayerInventoryTest, test=True).execute()


class LayerInventoryTest(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        inventory = base_windows.Inventory(parent=self)
        self.insert_layer(inventory)


if __name__ == '__main__':
    unittest.main(verbosity=2)
