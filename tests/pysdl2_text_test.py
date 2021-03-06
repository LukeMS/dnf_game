"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes


class PySDL2TextTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=ScenePySDL2TextTest, test=False).execute()


class ScenePySDL2TextTest(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.text = self.manager.fonts.render(
            "Lorem Ipsum", "caladea-regular.ttf", 16, (255, 127, 255))
        print(type(self.text))
        self.window = self.manager._window

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
