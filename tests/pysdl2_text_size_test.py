"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.util.ext.rect import Rect


class PySDL2TextSizeText(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=ScenePySDL2TextSizeText, test=True).execute()


class ScenePySDL2TextSizeText(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
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
                                            rect=Rect(0, 0, w + 16, h + 16))
        self.bg_sprite = bg_sprite

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(
            sprites=[self.bg_sprite, self.text, self.text2])


if __name__ == '__main__':
    unittest.main(verbosity=2)
