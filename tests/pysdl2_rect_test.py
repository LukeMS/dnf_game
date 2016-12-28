"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.util.ext.rect import Rect
from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes


class PySDL2RectTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=ScenePySDL2RectTest, test=True).execute()


class ScenePySDL2RectTest(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
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
