"""Test for specific_weapons.py."""

import unittest

from dnf_game.dnf_main.components import combat
from dnf_game.dnf_main.map_entities import PCreature
from dnf_game.util.tree_view import tree_view


class TestCharacter(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
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

        print("\n", "#" * 30, "\n%s" % __file__)
        self.scene = Scene()

    def tearDown(self):
        """..."""
        pass

    def test_all(self):
        """..."""
        d = {}
        for _class in combat.char_roll.classes:
            for race in combat.char_roll.races:
                d["_".join((_class, race))] = PCreature(
                    scene=self.scene, pos=(0, 0),
                    _class=_class, race=race).combat

        if __name__ == '__main__':
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
