"""Button example use."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.scene_manager.layers import gui_layer


class GuiButtonTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneGuiButtonTest, test=False).execute()


class SceneGuiButtonTest(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        gui = gui_layer.GUILayer(parent=self)
        gui.create_button(rect=(10, 10, 105, 25),
                          command=self.print_on_press,
                          text='Press Me',
                          clicked_font_color=(0, 0, 0),
                          hover_font_color=(205, 195, 100),
                          font_name="caladea-regular.ttf",
                          font_size=16,
                          font_color=(255, 255, 255),
                          border_color=(0, 0, 0))
        gui.active = True
        gui.visible = True
        self.insert_layer(gui)

    @staticmethod
    def print_on_press():
        """Sample callback function that prints a message to the screen."""
        print('button pressed')

if __name__ == '__main__':
    unittest.main(verbosity=2)
