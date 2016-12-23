"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes.base_scenes import SceneMultiLayer
from dnf_game.scene_manager.layers.base_layers import Layer


class GradientWindowTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneGradientWindowTestPySDL2, test=True).execute()


class GradientWindow(Layer):
    """..."""

    def __init__(self, parent, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.create_gradient_surface()

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.surface)


class SceneGradientWindowTestPySDL2(SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        gradient_window = GradientWindow(parent=self)
        self.insert_layer(gradient_window)


if __name__ == '__main__':
    unittest.main(verbosity=2)
