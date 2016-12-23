"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes


class MouseTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneMouseTestPySDL2, test=True).execute()


class SceneMouseTestPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.sprites = {}

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(
            sprites=self.sprites.values())

    def on_mouse_drag(self, x, y, dx, dy, button):
        """Called when mouse buttons are pressed and the mouse is dragged."""
        sprite = self.manager.fonts.render(
            "on_mouse_drag", "caladea-regular.ttf", 12, (255, 255, 255))
        sprite.position = x, y
        self.sprites["on_mouse_drag"] = sprite

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved."""
        sprite = self.manager.fonts.render(
            "on_mouse_motion", "caladea-regular.ttf", 12, (255, 0, 255))
        sprite.position = x, y
        self.sprites["on_mouse_motion"] = sprite

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons pressed."""
        if button == "LEFT" and not double:
            string = "simple left button"
            color = (255, 0, 0)
        elif button == "LEFT" and double:
            string = "double left button"
            color = (0, 255, 0)
        elif button == "RIGHT" and not double:
            string = "simple right button"
            color = (0, 0, 255)
        elif button == "RIGHT" and double:
            string = "double right button"
            color = (0, 255, 255)
        sprite = self.manager.fonts.render(
            string, "caladea-regular.ttf", 12, color)
        sprite.position = x, y
        self.sprites[string] = sprite

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        for sprite in self.sprites.values():
            sprite.position = (sprite.position[0],
                               max(sprite.position[1] + offset_y, 0))

if __name__ == '__main__':
    unittest.main(verbosity=2)
