"""..."""

import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scene_manager import Manager
from dnf_main.scenes.scene_descriptions import SceneDescriptions


class SceneDescriptionsTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneDescriptions, test=True).execute()

if __name__ == '__main__':
    unittest.main(verbosity=2)
