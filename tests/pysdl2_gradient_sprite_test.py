"""Test Scene for manager using pysdl2."""

import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scene_manager import Manager
from scene_manager.scenes import base_scenes
from util import Rect


class GradientSpriteTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneGradientSpriteTestPySDL2, test=True).execute()


class SceneGradientSpriteTestPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        from_gradient = self.manager.factory.from_gradient
        self.sprite = from_gradient(color_start=(10, 36, 106, 0),
                                    color_end=(166, 202, 240, 0),
                                    rect=Rect(0, 0, 320, 240),
                                    mode="v")

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprite)


if __name__ == '__main__':
    unittest.main(verbosity=2)
