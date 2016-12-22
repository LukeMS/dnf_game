"""Test for specific_weapons.py."""
import os
import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dnf_main.map_entities import PCreature, ItemEntity


class TestSpecificWeapon(unittest.TestCase):
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

            msg_log = Dummy()
            msg_log.add = print

            gfx.hp_bar = Dummy()
            gfx.hp_bar.set_value = dummy

        print("\n", "#" * 30, "\n%s" % __file__)
        self.scene = Scene()

    def tearDown(self):
        """..."""
        pass

    def test_bastards_sting(self):
        """..."""
        weapon_test = {}

        for _class in ["paladin", "antipaladin"]:
            try:
                player = PCreature(scene=self.scene,
                                   pos=(0, 0),
                                   _class=_class)
            except ValueError as e:
                player.combat._class = _class

            weapon = ItemEntity(name="bastard's sting",
                                pos=(0, 0), scene=self.scene)

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

        self.assertEqual(
            weapon_test['antipaladin']['magic'], 5)
        self.assertEqual(
            weapon_test['antipaladin']['on_hit_actions'], ['unholy'])
        self.assertEqual(
            weapon_test['antipaladin']['on_turn_actions'], ['unholy aurea'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
