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
        Manager(scene=SceneRectTestPySDL2, test=True).execute()


class SceneRectTestPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        from_color = self.manager.factory.from_color

        colors = [(255, 0, 0, 0), (0, 0, 255, 0), (0, 0, 255, 0)]

        rect_a = Rect(10, 10, 100, 100)
        rect_b = Rect(400, 400, 100, 100)
        rect_c = rect_a.gap(rect_b)

        self.sprites = {from_color(color=c, rect=r)
                        for c, r in zip(colors, [rect_a, rect_b, rect_c])}

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprites)


if __name__ == '__main__':
    unittest.main(verbosity=2)
