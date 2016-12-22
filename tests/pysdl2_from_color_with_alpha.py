"""Test Scene for manager using pysdl2."""

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
        Manager(scene=SceneFromColorWithAlphaPySDL2, test=True).execute()


class SceneFromColorWithAlphaPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        from_color = self.manager.factory.from_color

        self.sprites = []
        self.sprites.append(from_color(rect=Rect(150, 150, 200, 200),
                                       color=(255, 255, 255, 127)))
        self.sprites.append(from_color(rect=Rect(0, 0, 200, 200),
                                       color=(255, 0, 0, 127)))
        self.sprites.append(from_color(rect=Rect(0, 150, 200, 200),
                                       color=(0, 255, 0, 127)))
        self.sprites.append(from_color(rect=Rect(150, 0, 200, 200),
                                       color=(0, 0, 255, 127)))

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprites)


if __name__ == '__main__':
    unittest.main(verbosity=2)
