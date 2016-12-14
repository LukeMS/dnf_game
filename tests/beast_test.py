"""Test for specific_weapons.py."""
import os
import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import combat
import sprite


class TestBeast(unittest.TestCase):

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

        self._scene = Scene()


    def tearDown(self):
        pass

    def test_all_dragons(self):
        return
        d = {k: None for k in combat.bestiary.Bestiary.get_filtered(
            filter_list=[
                ("type", "dragon", "match", True)])}

        for template in d:
            d[template] = sprite.NPC(
                template=template, scene=self._scene, x=0, y=0).combat

        import tree_view

        tree_view.tree_view(d, expand=[combat.creatures.Beast])


if __name__ == '__main__':
    unittest.main(verbosity=2)
