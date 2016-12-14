"""Test for specific_weapons.py."""

import os
import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import obj_components

# from specific_weapons import WEAPONS

import sprite

from common.tree_view import tree_view


class TestSpecificWeapon(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        def dummy(*args, **kwargs):
            pass

        def dummy_true(self):
            return True

        class Dummy:
            add = print

        class Cell:
            visible = True

        class Grid:
            def __getitem__(self, key):
                return Cell()

        class Scene():
            def __init__(self, *args, **kwargs):
                self.msg_log = Dummy()
                self.add_obj = dummy
                self.rem_obj = dummy
                self.gfx = gfx = Dummy()
                gfx.hp_bar = Dummy()
                gfx.hp_bar.set_value = dummy

        sprite.GameObject.current_level = dummy
        sprite.GameObject.next_to_vis = dummy_true
        sprite.GameObject.visible = dummy_true
        self.scene = Scene()

    def tearDown(self):
        """..."""
        pass

    def test_bastards_sting(self):
        """..."""
        scene = self.scene
        player = sprite.Player(scene=scene, x=0, y=0)
        scene.player = player

        weapon = sprite.Item("bastard's sting", x=0, y=0, scene=scene)

        weapon.item.pick_up(player)
        weapon.item.use(player)

        tree_view(weapon, expand=[obj_components.Weapon])


if __name__ == '__main__':
    unittest.main(verbosity=2)
