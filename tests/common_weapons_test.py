"""Test for specific_weapons.py."""

import unittest

from dnf_game.dnf_main.components import WeaponComponent
from dnf_game.dnf_main.map_entities import (
    CreatureEntityAbstract, PCreature, ItemEntity, MapEntityAbstract)
from dnf_game.util.tree_view import tree_view


class TestCommonWeapons(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        def dummy(*args, **kwargs):
            pass

        def dummy_iter(*args, **kwargs):
            return []

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
                self.current_level = Dummy()
                self.current_level.get_neighbors = dummy_iter

        print("\n", "#" * 30, "\n%s" % __file__)
        CreatureEntityAbstract.current_level = Grid()
        CreatureEntityAbstract.next_to_vis = dummy_true
        MapEntityAbstract.visible = Dummy()
        MapEntityAbstract.sprite = Dummy()
        self.scene = Scene()

    def tearDown(self):
        """..."""
        pass

    def test_bastards_sting(self):
        """..."""
        scene = self.scene
        player = PCreature(scene=scene, pos=(0, 0))
        scene.player = player

        weapon = ItemEntity(name="bastard's sting", pos=(0, 0), scene=scene)

        weapon.item.pick_up(player)
        weapon.item.use(player)

        if __name__ == '__main__':
            tree_view(weapon, expand=[WeaponComponent])


if __name__ == '__main__':
    unittest.main(verbosity=2)
