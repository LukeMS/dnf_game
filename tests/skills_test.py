"""Test for specific_weapons.py."""
import os
import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dnf_main.map_entities import ItemEntity, PCreature
from dnf_main.components import combat


class TestSkills(unittest.TestCase):
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
            def __init__(self, *args, **kwargs):
                self.msg_log = Dummy()
                self.msg_log.add = print
                self.add_obj = dummy
                self.rem_obj = dummy
                self.gfx = gfx = Dummy()
                gfx.hp_bar = Dummy()
                gfx.hp_bar.set_value = dummy

        print("\n", "#" * 30, "\n%s" % __file__)
        self.scene = Scene()

    def tearDown(self):
        """..."""
        pass

    def test_dwarf_rogue(self):
        """..."""
        player = PCreature(
            scene=self.scene, pos=(0, 0),
            _class="rogue", race="dwarf")

        self.assertEqual(
            player.combat.skills.skills['appraise'].trained, True)

        self.assertEqual(
            player.combat.skills.skills['appraise'].ranks, 2)

        self.assertEqual(
            player.combat.skills.skills['appraise'].value, 5)

        before_armor = int(player.combat.skills.skills['swim'].value)

        armor = ItemEntity(name="studded leather", pos=(0, 0),
                           scene=self.scene)
        armor.item.pick_up(player)
        armor.item.use(player)

        # armor.

        """

        import tree_view

        skills = player.combat.skills
        combat = player.combat
        inventory = player.inventory

        player_dict = tree_view.Tree(player)

        player_dict["combat"] = tree_view.Tree(combat)
        player_dict["inventory"] = [
            tree_view.Tree(item, expand=[obj_components.Armor])
            for item in inventory]


        player_dict["combat"]["skills"] = tree_view.Tree(skills)

        from mylib.data_tree import tk_tree_view

        tk_tree_view(player_dict)

        """

        self.assertEqual(
            player.combat.skills.skills['swim'].value,
            before_armor + armor.equipment.armor_check_penalty)

    def test_all(self):
        return

        import tree_view
        d = {}
        for _class in ["rogue"]:  # combat.char_roll.classes:
            for race in ["dwarf"]:  # combat.char_roll.races:
                d["_".join((_class, race))] = PCreature(
                    scene=self.scene, x=0, y=0,
                    _class=_class, race=race).combat

        for character in d.keys():
            skills = d[character].__dict__.pop('skills')
            d[character] = tree_view.Tree(d[character])
            d[character] = tree_view.Tree(
                skills, expand=[combat.skills.SkillNode])

        from mylib.data_tree import tk_tree_view

        tk_tree_view(d)


if __name__ == '__main__':
    unittest.main(verbosity=2)
