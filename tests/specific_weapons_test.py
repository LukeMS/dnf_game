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


class Player(sprite.Player):
    pass


class _Player:
    """Represents the player character."""

    inventory = []

    def __init__(self, char_class):
        """For this example, we just store the class on the instance."""
        self.char_class = char_class

    def pick_up(self, item):
        """Pick an object, put in inventory, set its owner."""
        self.inventory.append(item)
        item.owner = self


class Weapon(obj_components.Weapon):
    pass


class _Weapon:
    """An type of item that can be equipped/used to attack."""

    equipped = False
    action_lists = {
        "on_hit": "on_hit_actions",
        "on_turn": "on_turn_actions",
    }

    def __init__(self, template):
        """Set the parameters based on a template."""
        self.__dict__.update(WEAPONS[template])

    def toggle_equip(self):
        """Set item status and call its equip/unequip functions."""
        if self.equipped:
            self.equipped = False
            actions = self.on_unequip
        else:
            self.equipped = True
            actions = self.on_equip

        for action in actions:
            if action['type'] == "check":
                self.check(action)
            elif action['type'] == "action":
                self.action(action)

    def check(self, dic):
        """Check a condition and call an action according to it."""
        obj = getattr(self, dic['condition']['object'])
        compared_att = getattr(obj, dic['condition']['attribute'])
        value = dic['condition']['value']
        result = compared_att == value

        self.action(*dic[result])

    def action(self, *dicts):
        """Perform action with args, both specified on dicts."""
        for dic in dicts:
            act = getattr(self, dic['action'])
            args = dic['args']
            if isinstance(args, list):
                act(*args)
            elif isinstance(args, dict):
                act(**args)

    def set_attribute(self, field, value):
        """Set the specified field with the given value."""
        setattr(self, field, value)

    def add_to(self, category, actions):
        """Add one or more actions to the category's list."""
        action_list = getattr(self, self.action_lists[category])

        for action in actions:
            if action not in action_list:
                action_list.append(action)

    def remove_from(self, category, actions):
        """Remove one or more actions from the category's list."""
        action_list = self.action_lists[category]

        for action in actions:
            if action in action_list:
                action_list.remove(action)


class TestWeapon(unittest.TestCase):

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
        self.player = Player(scene=self.scene, x=0, y=0)


    def tearDown(self):
        pass

    def test_bastards_sting(self):
        weapon_test = {}
        player = self.player

        for _class in ["paladin", "antipaladin"]:
            player.combat._class = _class
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

        from pprint import pprint
        for _class in ["paladin", "antipaladin"]:
            pprint({_class: weapon_test[_class]})

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
    unittest.main()
