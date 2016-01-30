# coding=utf-8

import sys
import os
import random

if not os.path.isdir('combat'):
    if os.path.isdir(os.path.join('..')):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import combat.char_roll
import combat.parse_saves
import combat.parse_atk


class Creature:
    """docstring for Creature"""

    history = {}
    name = None
    age = None
    max_age = None
    gender = None
    race = None
    _class = None
    alignment = None
    race_mod = [None] * 6
    age_mod = [None] * 6
    weight = None
    height = None
    save_mod = [None] * 3
    level = 1
    ac_enforce = None
    ac_armor = None
    specials_saves = {}
    damage = 0

    def __init__(self, *args, **kwargs):

        self.__dict__.update(kwargs)

        if hasattr(self, "game"):
            self.bestiary = self.game.bestiary
            self.namegen = self.game.namegen
        else:
            import rnd_name
            self.namegen = rnd_name.NameGen()

    def get_status(self):
        return {
            "Name": self.name,
            "Age": self.age,
            "Max. Age": self.max_age,
            "Gender": self.gender,
            "Race": self.race,
            "CLass": self._class,
            "Alignment": self.alignment,
            "Base Attributes": self.base_att,
            "Racial Modifiers": self.race_mod,
            "Age Modifiers": self.age_mod,
            "Weight": self.weight,
            "Height": self.height
        }

    @property
    def hit_points_current(self):
        return self.hit_points_total - self.damage

    def receive_dmg(self, dmg, source=False):
        """
        Hit Points
        When your hit point total reaches 0, you’re disabled. When
        it  reaches  –1,  you’re  dying.  When  it  gets  to  a  negative
        amount equal to your Constitution score, you’re dead.
        """
        self.hit_points_current -= dmg
        if "health_bar" in self.__dict__:
            self.update_health_bar()

    def update_health_bar(self):
        total = int(self.hit_points_total)
        current = self.hit_points_current
        if current < 0:
            current = 0
        self.health_bar.set_frame(
            int(round(
                current / total * 10,
                0)))

    def set_equipment_slots(self):
        pass


class Character(Creature):
    """docstring for Character"""
    hp_history = []
    melee = {
        'main': {
            'melee_desc': [],
            'melee': [],
            'melee_dmg': [],
            'melee_crit': [],
            'melee_crit_dmg': [],
            'melee_esp': []
        }
    }

    def __init__(self, rnd=True, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)

        self.__dict__.update(kwargs)

        self.base_att = combat.char_roll.roll_attributes()
        self.races = combat.char_roll.races
        self.classes = combat.char_roll.classes

        self.change_race()
        self.change_class()
        self.change_gender()
        self.change_alignment()
        self.change_name()
        self.change_age()

        self.set_hit_points()
        self.set_unarmed()

    def change_race(self, value=None):
        if value is None:  # make it random
            self.race = random.choice(self.races)
        elif isinstance(value, int):
            index = self.races.index(self.race)
            index += value
            index = index % len(self.races)
            self.race = self.races[index]
        else:
            self.race = value

        self.change_age()
        self.change_name()
        self.change_height_weight()

    def change_class(self, value=None):
        if value is None:
            self._class = random.choice(self.classes)

        self.alignments = combat.char_roll.alignments[
            self._class]

    def change_gender(self, value=None):
        if value == 'rnd':
            if self.race == 'changeling':
                self.gender = "female"
            else:
                self.gender = random.choice(["male", "female"])

    def change_alignment(self, value=None):
        if value is None:
            self.alignment = random.choice(self.alignments)

    def change_name(self, value=None):
        if value is None:
            if self.race and self.gender:
                self.first_name, self.surname = self.namegen.get_name(
                    race=self.race,
                    gender=self.gender,
                    number=1)
                if self.surname != "":
                    self.name = self.first_name[0] + ' ' + self.surname[0]
                else:
                    self.name = self.first_name[0]
                self.fancy_name = self.name

    def change_age(self, value=None):
        if value is None:  # make it random
            if self.race and self._class:
                self.age, self.max_age = combat.char_roll.get_age(
                    self.race, self._class)
            else:
                return

        self.age_mod = combat.char_roll.aging_modifiers(
            self.age, self.race)

    def change_height_weight(self, value=None):
        if value is None:  # make it random
            if self.race and self.gender and self.race_mod:
                self.height_, self.weight_ = combat.char_roll.height_weight(
                    self.race, self.gender, self.race_mod)
                self.height = combat.char_roll.unit_conversion(
                    self.height_, 'ft')
                self.weight = combat.char_roll.unit_conversion(
                    self.weight_, 'lb')

    def set_hit_points(self):
        """
        Hit Points (hp): Hit points are an abstraction signifying how robust
        and healthy a creature is at the current moment. To determine a
        creature's hit points, roll the dice indicated by its Hit Dice. A
        creature gains maximum hit points if its first Hit Die roll is for a
        character class level. Creatures whose first Hit Die comes from an NPC
        class or from his race roll their first Hit Die normally. Wounds
        subtract hit points, while healing (both natural and magical) restores
        hit points. Some abilities and spells grant temporary hit points that
        disappear after a specific duration. When a creature's hit points drop
        below 0, it becomes unconscious. When a creature's hit points reach a
        negative total equal to its Constitution score, it dies.
        """

        if len(self.hp_history) < self.level:
            dice = self.hit_dice
            att_mod = self.att_mod[2]  # constitution
            tough_mod = 0  # toughness
            if self.level == 1:
                result = dice
            else:
                result = combat.char_roll.roll(
                    faces=dice,
                    modifier=att_mod + tough_mod
                )

            self.hp_history.append({
                "dice": int(dice),
                'att_mod': int(att_mod),
                'tough_mod': int(tough_mod),
                'result': int(result)
            })

        self.hit_points_total = sum(
            [self.hp_history[x]['result']
                for x in range(self.level)])

    @property
    def xp_award(self):

        cr_list = sorted(list(combat.char_roll.xp_award.keys()))

        hd_cr = cr_list.index(int(self.level))

        return combat.char_roll.xp_award[cr_list[hd_cr - 1]]

    @property
    def bab(self):
        description = """Base Attack Bonus (BAB): Each creature has a base
        attack bonus and it represents its skill in combat.
        As a character gains levels or Hit Dice, his base attack bonus
        improves. When a creature's base attack bonus reaches +6, +11, or +16,
        he receives an additional attack in combat when he takes a full-attack
        action (which is one type of full-round action.
        Attack Roll: An attack roll represents your attempt to strike your
        opponent on your turn in a round. When you make an attack roll, you
        roll a d20 and add your attack bonus. (Other modifiers may also apply
        to this roll.) If your result equals or beats the target's Armor
        Class, you hit and deal damage.
        Automatic Misses and Hits: A natural 1 (the d20 comes up 1) on an
        attack roll is always a miss. A natural 20 (the d20 comes up 20) is
        always a hit. A natural 20 is also a threat — a possible critical
        hit.
        Melee Attack Bonus
            BAB + Strength modifier + size modifier
        Ranged Attack Bonus
            BAB + Dexterity modifier + size modifier + range penalty"""
        return combat.char_roll.bab[self._class][self.level - 1]

    @property
    def ranged(self):
        return [atk + self.att_mod[1] + self.size_modifier
                for atk in self.bab]

    def set_unarmed(self):
        punch = {
            'melee_desc': [],
            'melee': [],
            'melee_dmg': [],
            'melee_crit': [],
            'melee_crit_dmg': [],
            'melee_esp': []
        }
        for atk in self.bab:
            punch['melee_desc'].append("punch")
            punch['melee'].append(
                atk + self.att_mod[0] + self.size_modifier)
            if self.att_mod[0] < 0:
                melee_dmg = "1d4{}".format(self.att_mod[0])
            elif self.att_mod[0] > 0:
                melee_dmg = "1d4+{}".format(self.att_mod[0])
            else:
                melee_dmg = "1d4"
            punch['melee_dmg'].append(melee_dmg)
            punch['melee_crit'].append(None)
            punch['melee_crit_dmg'].append(2)
            punch['melee_esp'].append(None)

        self.melee['main'] = punch

    @property
    def hit_dice(self):
        description = """Hit Dice (HD): Hit Dice represent a creature's
        general level of power and skill. As a creature gains levels, it gains
        additional Hit Dice.
        Monsters, on the other hand, gain racial Hit Dice, which represent the
        monster's general prowess and ability. Hit Dice are represented by the
        number the creature possesses followed by a type of die, such as
        "3d8". This value is used to determine a creature's total hit points.
        In this example, the creature has 3 Hit Dice. When rolling for this
        creature's hit points, you would roll a d8 three times and add the
        results together, along with other modifiers."""

        return combat.char_roll.hit_dice[self._class]

    @property
    def ac(self):
        description = """10 + armor bonus + shield bonus + Dex modifier
         + other modifiers.
        Armor, shield and natural armor bonuses do not applyto touch AC.
        Dex and Dodge bonuses do not apply to flat footed AC (unless you have
        an ability like uncanny dodge to mitigate things)
        """
        return (10 +
                sum(item.equipment.ac_bonus for item in self.all_equipped()) +
                # dodge_bonus
                self.att_mod[1] +
                self.size_modifier)

    @property
    def ac_flat(self):
        description = """
            Flat-Footed: At the start of a battle, before you have had a
            chance to act (specifically, before your first regular turn in the
            initiative order), you are flat-footed. You can't use your
            Dexterity bonus to AC (if any) while flat-footed. Barbarians and
            rogues of high enough level have the uncanny dodge extraordinary
            ability, which means that they cannot be caught flat-footed.
            Characters with uncanny dodge retain their Dexterity bonus to
            their AC and can make attacks of opportunity before they have
            acted in the first round of combat. A flat-footed character can't
            make attacks of opportunity, unless he has the Combat Reflexes
            feat.
            """
        return (10 +
                sum(item.equipment.ac_bonus for item in self.all_equipped()) +
                # dodge_bonus
                # self.att_mod[1] if *uncanny dodge* else 0
                self.size_modifier)

    @property
    def ac_touch(self):
        description = """
            Touch Attacks: Some attacks completely disregard armor, including
            shields and natural armor—the aggressor need only touch a foe for
            such an attack to take full effect. In these cases, the attacker
            makes a touch attack roll (either ranged or melee). When you are
            the target of a touch attack, your AC doesn't include any armor
            bonus, shield bonus, or natural armor bonus. All other modifiers,
            such as your size modifier, Dexterity modifier, and deflection
            bonus (if any) apply normally. Some creatures have the ability to
            make incorporeal touch attacks. These attacks bypass solid
            objects, such as armor and shields, by passing through them.
            Incorporeal touch attacks work similarly to normal touch attacks
            except that they also ignore cover bonuses. Incorporeal touch
            attacks do not ignore armor bonuses granted by force effects, such
            as mage armor and bracers of armor."""
        return (10 +
                # dodge_bonus
                self.att_mod[1] +
                self.size_modifier)

    @property
    def race_mod(self):
        return combat.char_roll.race_modifiers(self.race)

    @property
    def size(self):
        return combat.char_roll.hw_dict[self.race]['size']

    @property
    def size_modifier(self):
        return combat.char_roll.size_modifier[self.size]

    @property
    def base_speed(self):
        return combat.char_roll.speed[self.race]

    @property
    def speed(self):
        return self.base_speed  # +- something

    @property
    def save_base(self):
        return combat.char_roll.saving_throws[self._class][self.level]

    @property
    def saves(self):
        return [base + mod for base, mod in zip(
                self.save_base, self.save_att_bonus)]

    @property
    def save_att_bonus(self):
        """
        Fortitude: + Constitution
        Reflex: + Dexterity
        Will: + Wisdom
        att: ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha'],
        """
        return [self.att_mod[2], self.att_mod[1], self.att_mod[4]]

    @property
    def att_mod(self):
        return [combat.char_roll.AttributeModifers.get(x)
                for x in self.base_att]

    @classmethod
    def test(cls):
        class Owner:
            inventory = []

        pc = Character()
        pc.owner = Owner()

        dic = dict(pc.__dict__)
        for att in [
            "hit_points_current", "melee", "xp_award", "bab", "melee",
            "ranged", "hit_dice", "ac", "ac_flat", "ac_touch", "race_mod",
            "size", "size_modifier", "base_speed", "speed", "save_base",
            "saves", "save_att_bonus", "att_mod"
        ]:
            dic[att] = getattr(pc, att)

        from mylib.data_tree import tk_tree_view
        tk_tree_view(dic)

    def all_equipped(self):
        return [
            item for item in self.owner.inventory if
            item.equipment and item.equipment.is_equipped
        ]

if __name__ == '__main__':
    def testy():
        print("testy!")
        return True
    True or testy()
