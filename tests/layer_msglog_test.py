"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.scene_manager.layers import base_layers


class LayerMsgLogTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneLayerMsgLogTest, test=True).execute()


class SceneLayerMsgLogTest(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        msg_log = base_layers.MsgLog(parent=self)
        self.insert_layer(msg_log)
        msg_log.add("One")
        msg_log.add("Two")


if __name__ == '__main__':
    unittest.main(verbosity=2)
