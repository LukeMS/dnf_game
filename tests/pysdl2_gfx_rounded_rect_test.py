"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.util.ext import gfxdraw
from dnf_game.util.ext.rect import Rect


class TextTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneTextTestPySDL2, test=False).execute()


class SceneTextTestPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        w = 128
        h = 64
        rect = Rect(0, 0, w, h)
        sdlrenderer = self.manager.renderer.sdlrenderer
        factory = self.manager.factory
        #     def from_color(self, *, rect, color, bpp=32, masks=None):

        self.sprite = factory.from_new_texture(w, h)
        texture = self.sprite.texture

        with factory.new_render_target(texture):
            gfxdraw.rounded_box(sdlrenderer,
                                rect, 15, (255, 0, 0, 255))
            gfxdraw.pixel(sdlrenderer, 8, 8, (255, 255, 255, 255))
            gfxdraw.filled_polygon(sdlrenderer, color=(255, 255, 255, 255),
                                   points=(rect.midtop, rect.midright,
                                   rect.midbottom, rect.midleft))
            gfxdraw.bezier(sdlrenderer, color=(0, 0, 255, 255), steps=5,
                           points=(rect.midtop, rect.midright,
                                   rect.midbottom))

            gfxdraw.thick_line(sdlrenderer, *rect.bottomleft, *rect.topright,
                               5, (0, 255, 0, 127))

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprite)


if __name__ == '__main__':
    unittest.main(verbosity=2)
