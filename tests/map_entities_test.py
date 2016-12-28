"""..."""

import unittest

from dnf_game.dnf_main.map_entities import (
    TileEntity, FeatureEntity, ItemEntity, PCreature, NPCreature)
from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes


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

    def add_obj(self, obj, pos):
        """..."""
        _type = obj.__class__
        print("adding to scene: %s, type %s, at %s" % (obj.name, _type, pos))

if __name__ == '__main__':
    unittest.main(verbosity=2)
