"""..."""

import unittest

from dnf_game.scene_manager.manager import Manager
from dnf_game.dnf_main.scenes.scene_creation import SceneCreation


class SceneCreationTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneCreation, test=True).execute()

if __name__ == '__main__':
    unittest.main(verbosity=2)
