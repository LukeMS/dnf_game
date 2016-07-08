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

class TestSpecificWeapon(unittest.TestCase):

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


    def tearDown(self):
        pass

    def test_bastards_sting(self):
        weapon_test = {}

        for _class in ["paladin", "antipaladin"]:
            player = sprite.Player(scene=self.scene,
                                   x=0, y=0,
                                   _class=_class)

            weapon = sprite.Item("bastard's sting",
                                 x=0, y=0, scene=self.scene)

            weapon.item.pick_up(player)
            weapon.item.use(player)

            weapon_test[_class] = {
                "magic": int(weapon.equipment.magic),
                "on_hit_actions": list(weapon.equipment.on_hit_actions),
                "on_turn_actions": list(weapon.equipment.on_turn_actions),
            }

            weapon.item.drop(player)

        self.assertEqual(weapon_test['paladin']['magic'], 2)
        self.assertEqual(weapon_test['paladin']['on_hit_actions'], [])
        self.assertEqual(weapon_test['paladin']['on_turn_actions'], [])

        self.assertEqual(weapon_test['antipaladin']['magic'],
                         5)
        self.assertEqual(weapon_test['antipaladin']['on_hit_actions'],
                         ['unholy'])
        self.assertEqual(weapon_test['antipaladin']['on_turn_actions'],
                         ['unholy aurea'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
