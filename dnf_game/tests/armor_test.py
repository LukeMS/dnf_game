"""Test for specific_weapons.py."""

import unittest

from dnf_game.dnf_main.map_entities import PCreature, ItemEntity


class TestArmor(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        def dummy(*args, **kwargs):
            pass

        class Dummy:
            add = print

        class Scene():
            def __init__(self, *args, **kwargs):
                self.msg_log = Dummy()
                self.add_obj = dummy
                self.rem_obj = dummy
                self.gfx = gfx = Dummy()
                gfx.hp_bar = Dummy()
                gfx.hp_bar.set_value = dummy
        print("\n", "#" * 30, "\n%s" % __file__)

        self.scene = Scene()
        self.player = PCreature(scene=self.scene, pos=(0, 0),
                                _class="fighter",
                                race="human")

    def tearDown(self):
        """..."""
        pass

    def test_studded_leather_noproficiency_penalty(self):
        """..."""
        player = self.player

        armor = ItemEntity(name="studded leather",
                           pos=(0, 0), scene=self.scene)

        self.assertEqual(armor.equipment.type, "light armor")

        feat = player.combat.feats.get('armor proficiency (light)')
        # feat.acquired = False

        armor.item.pick_up(player)
        armor.item.use(player)

        self.assertEqual(
            feat.bab,
            -armor.equipment.armor_check_penalty)

        armor.item.drop(player)
        return

        """

        self.assertEqual(weapon_test['paladin']['magic'], 2)
        self.assertEqual(weapon_test['paladin']['on_hit_actions'], [])
        self.assertEqual(weapon_test['paladin']['on_turn_actions'], [])

        self.assertEqual(weapon_test['antipaladin']['magic'],
                         5)
        self.assertEqual(weapon_test['antipaladin']['on_hit_actions'],
                         ['unholy'])
        self.assertEqual(weapon_test['antipaladin']['on_turn_actions'],
                         ['unholy aurea'])

        """

if __name__ == '__main__':
    """
    class Debug:
        __init__ = TestArmor.setUp
        test = TestArmor.test_studded_leather_noproficiency_penalty

        @staticmethod
        def assertEqual(v1, v2):
            print("assertEqual", v1 == v2)

    d = Debug()
    d.test()
    """

    unittest.main(verbosity=10)
