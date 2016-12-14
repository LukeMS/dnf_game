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
        fonts = self.manager.fonts
        font_name = "caladea-regular.ttf"
        text_color = (255, 31, 63)
        size = 16
        string = "Lorem Ipsum"

        self.text = fonts.render(string, font_name, size, text_color)
        pos = self.text.position
        self.text.position = pos[0] + 8, pos[1] + 8
        w, h = fonts.text_size(string, font_name, size)

        self.text2 = fonts.render(string, font_name, 24, text_color)
        pos = self.text2.position
        self.text.position = pos[0] + w * 2, pos[1] + h * 2

        bg_color = (63, 0, 127)
        bg_sprite = self.factory.from_color(color=bg_color,
                                            size=(w + 16, h + 16))
        self.bg_sprite = bg_sprite

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(
            sprites=[self.bg_sprite, self.text, self.text2])


if __name__ == '__main__':
    unittest.main(verbosity=2)
