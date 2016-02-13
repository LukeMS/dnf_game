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


class TestArmor(unittest.TestCase):

    def setUp(self):
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

        self.scene = Scene()
        self.player = sprite.Player(scene=self.scene, x=0, y=0,
                                    _class="fighter",
                                    race="human")


    def tearDown(self):
        pass

    def test_studded_leather_noproficiency_penalty(self):
        player = self.player

        armor = sprite.Item("studded leather",
                            x=0, y=0, scene=self.scene)

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
