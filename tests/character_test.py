"""Test for specific_weapons.py."""
import os
import sys
import unittest

try:
    import combat
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    import combat

import sprite

from common.tree_view import tree_view

class TestCharacter(unittest.TestCase):

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

    def test_all(self):
        d = {}
        for _class in combat.char_roll.classes:
            for race in combat.char_roll.races:
                d["_".join((_class, race))] = sprite.Player(
                    scene=self.scene, x=0, y=0,
                    _class=_class, race=race).combat

        for character in d.keys():
            feats = d[character].__dict__.pop('feats')
            skills = d[character].__dict__.pop('skills')
            d[character] = tree_view(d[character])
            d[character]['feats'] = tree_view(
                feats, expand=[combat.feats.FeatNode])
            d[character]['skills'] = tree_view(
                skills, expand=[combat.skills.SkillNode])


        tree_view(d)


if __name__ == '__main__':
    unittest.main(verbosity=2)
