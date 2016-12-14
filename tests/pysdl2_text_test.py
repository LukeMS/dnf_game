"""Test Scene for manager using pysdl2."""

import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from manager import Manager
from manager.scenes import base_scenes


class TestSceneTiles(unittest.TestCase):
    """..."""

    def test_scene(self):
        """..."""
        Manager(scene=SceneText).execute()


class SceneText(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        self.text = self.manager.fonts.render(
            "Lorem Ipsum", "caladea-regular.ttf", 16, (255, 127, 255))
        print(type(self.text))

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
