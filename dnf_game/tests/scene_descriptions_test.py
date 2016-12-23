"""..."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.dnf_main.scenes.scene_descriptions import SceneDescriptions


class SceneDescriptionsTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneDescriptions, test=False).execute()

if __name__ == '__main__':
    unittest.main(verbosity=2)
