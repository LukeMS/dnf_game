"""Text box example use."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.scene_manager.layers import base_layers
from dnf_game.scene_manager.layers import gui_layer
from dnf_game.util.ext.rect import Rect


class LayerGuiTextboxTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneLayerGuiTextboxTest, test=False).execute()


class SceneLayerGuiTextboxTest(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        frame = base_layers.Layer(parent=self)
        frame.create_gradient_surface()
        gui = gui_layer.GUILayer(parent=self)
        rect = Rect(0, 0, 150, 30)
        rect.bottomright = (self.width, self.height)
        gui.create_textbox(rect=rect,
                           command=print_on_enter,
                           disable_on_execute=False)
        self.insert_layer(frame, gui)


def print_on_enter(id, final):
    """Sample callback function that prints a message to the screen."""
    locals()["manager"] = Manager()
    print('enter pressed, textbox contains "{}"'.format(final))
    eval(final)

if __name__ == '__main__':
    unittest.main(verbosity=2)
