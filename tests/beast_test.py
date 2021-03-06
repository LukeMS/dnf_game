"""Test for specific_weapons.py."""

import unittest

from dnf_game.dnf_main.components import combat
from dnf_game.dnf_main.data_handler.bestiary import Bestiary
from dnf_game.dnf_main.map_entities import NPCreature
from dnf_game.util import tree_view
from dnf_game.util.ext.queries import where


class TestBeast(unittest.TestCase):
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
        self._scene = Scene()

    def tearDown(self):
        """..."""
        pass

    def test_all_dragons(self):
        """..."""
        b = Bestiary()
        l = (b.search(
            (where('type') == "dragon")
        ))

        d = {template["def_name"]: NPCreature(name=template["def_name"],
                                              scene=self._scene,
                                              pos=(0, 0)).combat
             for template in l}

        if __name__ == '__main__':
            tree_view.tree_view(d, expand=[combat.creatures.Beast])


if __name__ == '__main__':
    unittest.main(verbosity=2)
