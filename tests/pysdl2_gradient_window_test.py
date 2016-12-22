"""Test Scene for manager using pysdl2."""

import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scene_manager import Manager
from scene_manager.scenes import base_scenes
from scene_manager.windows import base_windows


class GradientWindowTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneGradientWindowTestPySDL2, test=True).execute()


class GradientWindow(base_windows.Layer):
    """..."""

    def __init__(self, parent, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.create_gradient_surface()

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.surface)


class SceneGradientWindowTestPySDL2(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        gradient_window = GradientWindow(parent=self)
        self.insert_layer(gradient_window)


if __name__ == '__main__':
    unittest.main(verbosity=2)
