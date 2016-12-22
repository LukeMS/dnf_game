"""..."""

import unittest

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scene_manager import Manager, base_scenes
from dnf_main.map_entities import (TileEntity, FeatureEntity, ItemEntity,
                                   PCreature, NPCreature, Cursor)


class MapEntitiesTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneMapEntitiesTest, test=True).execute()


class SceneMapEntitiesTest(base_scenes.SceneBase):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)
        self.tile = TileEntity(name="floor", scene=self, pos=(0, 0))
        self.feature = FeatureEntity(name="stair_up", scene=self, pos=(0, 0))
        self.item = ItemEntity(name='healing potion', scene=self, pos=(0, 0))
        self.player = PCreature(scene=self, pos=(0, 0))
        self.beast = NPCreature(name="orc", scene=self, pos=(0, 0))

    def add_obj(self, obj, _type, pos):
        """..."""
        print("adding to scene: %s, type %s, at %s" % (obj.name, _type, pos))

if __name__ == '__main__':
    unittest.main(verbosity=2)
