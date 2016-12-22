"""Test for specific_weapons.py."""

import unittest

from dnf_game.dnf_main.map_entities import PCreature
from dnf_game.dnf_main.components import combat
from dnf_game.util.tree_view import tree_view


class TestFeats(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        def dummy(*args, **kwargs):
            pass

        class Dummy:
            pass

        class Scene():
            add_obj = dummy
            rem_obj = dummy

            gfx = Dummy()

            gfx.msg_log = Dummy()
            gfx.msg_log.add = print

            gfx.hp_bar = Dummy()
            gfx.hp_bar.set_value = dummy

        print("\n", "#" * 30, "\n%s" % __file__)
        self.scene = Scene()

        self.player = PCreature(scene=self.scene, pos=(0, 0),
                                _class="fighter", race="human")

    def tearDown(self):
        """..."""
        pass

    def test_human_fighter(self):
        """..."""
        player = self.player

        self.assertEqual(player.combat.race, "human")
        self.assertEqual(player.combat._class, "fighter")
        self.assertEqual(player.combat.feats.points, 3)

        player.combat.feats.on_equip()

        if __name__ == '__main__':
            tree_view(player.combat.feats, expand=[combat.feats.FeatNode])


if __name__ == '__main__':
    unittest.main(verbosity=10)
