"""Test Scene for manager using pysdl2."""

import random
import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from util import Rect
from scene_manager import Manager
from scene_manager.scenes import base_scenes


class RectTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneFromGradientWithAlphaPySDL2, test=False).execute()


class SceneFromGradientWithAlphaPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        from_g = self.manager.factory.from_gradient
        from_c = self.manager.factory.from_color

        self.sprites = [
            from_g(
                rect=Rect(64, 64, 200, 200), mode="h",
                color_end=(255, 0, 0, 31), color_start=(255, 255, 255, 127)
            ),
            from_g(
                rect=Rect(214, 64, 200, 200), mode="v",
                color_end=(0, 255, 0, 31), color_start=(255, 255, 255, 127)
            ),
            from_g(
                rect=Rect(214, 214, 200, 200), mode="h",
                color_end=(255, 255, 255, 127), color_start=(0, 0, 255, 31)
            ),
            from_g(
                rect=Rect(64, 214, 200, 200), mode="v",
                color_end=(255, 255, 255, 127), color_start=(255, 255, 0, 31)
            ),
            from_c(rect=Rect(0, 0, 128, 128), color=(0, 0, 127, 127)),
            from_c(rect=Rect(350, 0, 128, 128), color=(127, 127, 0, 127)),
            from_c(rect=Rect(350, 350, 128, 128), color=(127, 0, 0, 127)),
            from_c(rect=Rect(0, 350, 128, 128), color=(0, 127, 0, 127))
        ]

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=reversed(self.sprites))


if __name__ == '__main__':
    unittest.main(verbosity=2)
