"""Test for specific_weapons.py."""

import os
import sys
import unittest

try:
    import combat
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    import combat

import obj_components

# from specific_weapons import WEAPONS

import sprite

from common.tree_view import tree_view

class TestSpecificWeapon(unittest.TestCase):

    def setUp(self):
        def dummy(*args, **kwargs):
            pass

        class Dummy:
            pass

        class Cell:
            visible = True

        class Grid:
            def __getitem__(self, key):
                return Cell()

        class Scene():
            add_obj = dummy
            rem_obj = dummy

            grid = Grid()

            gfx = Dummy()

            gfx.msg_log = Dummy()
            gfx.msg_log.add = print

            gfx.hp_bar = Dummy()
            gfx.hp_bar.set_value = dummy

        self.scene = Scene()


    def tearDown(self):
        pass

    def test_bastards_sting(self):

        player = sprite.Player(scene=self.scene, x=0, y=0)

        weapon = sprite.Item("bastard's sting",
                             x=0, y=0, scene=self.scene)

        weapon.item.pick_up(player)
        weapon.item.use(player)

        tree_view(weapon, expand=[obj_components.Weapon])


if __name__ == '__main__':
    unittest.main(verbosity=2)
