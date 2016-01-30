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
from combat.bestiary import Bestiary
from rnd_name import NameGen

import effects


class Creature:
    """docstring for Creature"""

    owner = None

    name = None
    age = None
    max_age = None
    gender = None
    race = None
    _class = None
    alignment = None
    race_mod = [0] * 6
    age_mod = [0] * 6
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

    def attack(self, target):
        """
        When the result of the die roll to
        make  an  attack  is  a  natural  20  (that  is,  the  die  actually
        shows  a  20),  this  is  known  as  a  critical  threat  (although
        some weapons can score a critical threat on a roll of less
        than 20). If a critical threat is scored, another attack roll is
        made, using the same modifiers as the original attack roll.
        If this second attack roll exceeds the target’s AC, the hit
        becomes a critical hit, dealing additional damage.
        """
        def log_atk(atk_type, hit_roll, atk_bab, result):
            string = (
                "{} attacks ({}) {}".format(
                    self.fancy_name,
                    atk_type,
                    target.combat.fancy_name) +
                "({}[d20] + {}[bonus] = {}) x AC {}".format(
                    hit_roll, atk_bab, result, target.combat.ac)
            )
            msg_log.add(string)

        def log_hit(dmg, critical=False):
            if critical:
                string = "and lands a critical hit for {} dmg".format(dmg)
            else:
                string = "and hits for {} dmg".format(dmg)
            msg_log.add(string)

        def log_miss():
            string = "but misses"
            msg_log.add(string)

        msg_log = self.owner.scene.gfx.msg_log

        roll = combat.char_roll.roll

        atk = self.melee[random.choice(list(self.melee.keys()))]
        # print(self.melee, atk)

        for i in range(len(atk['melee'])):

            base_result = roll(string='1d20', verbose=False)

            bonus = atk['melee'][i]
            result = base_result + bonus

            log_atk(
                atk['melee_desc'][i],
                base_result,
                bonus,
                result)

            if atk['melee_crit'][i] is None:
                crit_range = 20
            else:
                crit_range = int(atk['melee_crit'][i])

            if result >= target.combat.ac or base_result == 20:
                if base_result >= crit_range:
                    """
                    IMPLEMENT PROPER CRITICAL ROLL HERE
                    """
                    critical = True
                    dmg = roll(atk['melee_dmg'][i])
                    dmg *= atk['melee_crit_dmg'][i]
                else:
                    critical = False
                    dmg = roll(atk['melee_dmg'][i])

                # If penalties reduce the damage result to less than 1, a hit
                # still deals 1 point of nonlethal(?) damage.
                dmg = max(dmg, 1)
                log_hit(dmg, critical=critical)
                target.combat.receive_dmg(dmg=dmg, source=self.owner)
            else:
                log_miss()

    def receive_dmg(self, dmg, source=None):
        """
        Hit Points
        When your hit point total reaches 0, you’re disabled. When
        it  reaches  –1,  you’re  dying.  When  it  gets  to  a  negative
        amount equal to your Constitution score, you’re dead.
        """
        # apply damage if possible
        if dmg > 0:
            self.damage += dmg

        # check for death. if there's a death function, call it
        if self.hit_points_current <= 0:
                self.death_func(self.owner)

                # "CR";"Total XP";"1–3";"4–5";"6+" creatures
                source.gain_xp(self.xp_award)

        self.owner.update_hp()

    def heal(self, amount):
        # heal by the given amount, without going over the maximum
        self.damage -= amount
        self.damage = max(0, self.damage)  # no negative damage
        self.owner.update_hp()

    def change_gender(self, value=None):
        if value is None:
            if self.race == 'changeling':
                self.gender = "female"
            else:
                self.gender = random.choice(["male", "female"])

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
                # print(self.__dict__)
                self.height_, self.weight_ = combat.char_roll.height_weight(
                    self.race, self.gender, self.race_mod)
                self.height = combat.char_roll.unit_conversion(
                    self.height_, 'ft')
                self.weight = combat.char_roll.unit_conversion(
                    self.weight_, 'lb')

    def set_equipment_slots(self):
        pass

    @classmethod
    def test(cls):
        import types

        class Owner:
            inventory = []

        creature = cls()
        creature.owner = Owner()

        dic = {}
        dic_keys = dir(creature)
        for att in dic_keys:
            if isinstance(getattr(creature, att), types.FunctionType):
                continue
            elif att[-2:] == "__":
                continue
            elif isinstance(getattr(type(creature), att, None), property):
                dic[att] = getattr(
                    type(creature), att).__get__(creature, type(creature))

            else:
                dic[att] = getattr(creature, att, None)

        from mylib.data_tree import tk_tree_view
        tk_tree_view(dic)


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
    xp = 0

    def __init__(self, rnd=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__dict__.update(kwargs)

        self._base_att = combat.char_roll.roll_attributes()
        self.races = combat.char_roll.races
        self.classes = combat.char_roll.classes

        self.change_race()
        self.change_class()
        self.change_gender()
        self.change_height_weight()
        self.change_alignment()
        self.change_name()
        self.change_age()

        self.set_hit_points()
        self.set_unarmed_atk()

        self.death_func = effects.player_death

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

    def change_alignment(self, value=None):
        if value is None:
            self.alignment = random.choice(self.alignments)

    def change_name(self, value=None):
        if value is None:
            if self.race and self.gender:
                self.first_name, self.surname = NameGen.get_name(
                    race=self.race,
                    gender=self.gender,
                    number=1)
                if self.surname != "":
                    self.name = self.first_name[0] + ' ' + self.surname[0]
                else:
                    self.name = self.first_name[0]
                self.fancy_name = self.name

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

        return combat.char_roll.xp_award[cr_list[hd_cr - 1]][1]

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

    def set_atk(self, obj):
        atk = {
            'melee_desc': [],
            'melee': [],
            'melee_dmg': [],
            'melee_crit': [],
            'melee_crit_dmg': [],
            'melee_esp': []
        }
        if not isinstance(obj, dict):
            base_atk = {}
            for key in atk.keys():
                try:
                    base_atk[key] = obj.__dict__[key]
                except KeyError:
                    pass
        else:
            base_atk = obj

        base_atk.setdefault('melee', 0)
        base_atk.setdefault('melee_esp', None)

        for i in self.bab:
            if self.att_mod[0] < 0:
                melee_dmg = "{}{}".format(
                    base_atk['melee_dmg'], self.att_mod[0])

            elif self.att_mod[0] > 0:
                melee_dmg = "{}+{}".format(
                    base_atk['melee_dmg'], self.att_mod[0])

            else:
                melee_dmg = base_atk['melee_dmg']

            atk['melee_dmg'].append(melee_dmg)
            atk['melee_desc'].append(base_atk['melee_desc'])
            atk['melee_crit'].append(base_atk['melee_crit'])
            atk['melee_crit_dmg'].append(base_atk['melee_crit_dmg'])
            atk['melee_esp'].append(base_atk['melee_esp'])

            atk['melee'].append(
                base_atk['melee'] + self.att_mod[0] + self.size_modifier)

        self.melee['main'] = atk

    def set_melee_atk(self):
        items = self.all_equipped(slot='right hand')
        # print("items", items)
        item = items[0] if items else None
        # print("item", item)
        if item:
            self.set_atk(item.equipment)
        else:
            self.set_unarmed_atk()

    def set_unarmed_atk(self):
        punch = {
            'melee_dmg': "1d3",
            'melee_desc': "Unarmed strike",
            'melee_crit': None,
            'melee_crit_dmg': 2,
            "melee_esp": "nonlethal"
        }

        self.set_atk(punch)

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
                self.ac_from_equip +
                # dodge_bonus
                self.att_mod[1] +
                self.size_modifier)

    @property
    def ac_from_equip(self):
        return sum(getattr(item.equipment, 'ac_bonus', 0)
                   for item in self.all_equipped())

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
                self.ac_from_equip +
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
    def attributes(self):
        return [b + r for b, r in zip(self._base_att, self.race_mod)]

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
    def save_mod(self):
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
                for x in self.attributes]

    def all_equipped(self, slot=None):
        return [
            item for item in self.owner.inventory if
            item.equipment and item.equipment.is_equipped and
            (slot is None or (getattr(item.equipment, 'slot', None) == slot))
        ]

    def equipment_bonus(self, bonus):
        return sum(
            getattr(item.equipment, bonus) for item in self.all_equipped())


class Beast(Creature):
    """docstring for Beast"""

    history = {}

    xp = 0

    def __init__(self, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model = model or Bestiary.get_model()

        self.table = Bestiary.get(model)

        # number of instances for sequential naming
        Beast.history.setdefault(model, 0)
        Beast.history[model] += 1

        self.race = model

        self.name = (model.capitalize() +
                     " " + str(Beast.history[model]).zfill(4))

        if self.table['class1']:
            self._class = self.table['class1']
        else:
            self._class = None

        self.set_att()
        self.set_save_mod()
        self.hit_dice = self.table["hd"]
        self.hit_points_total = int(self.table["hp"])
        self.speed = self.table["speed"]
        self.size = self.table["size"]

        self.ac = int(self.table["ac"])
        self.ac_flat = int(self.table["ac_flat-footed"])

        self.ac_touch = int(self.table["ac_touch"])

        self.set_melee()

        self.space = self.table["space"]
        self.reach = self.table["reach"]

        self.xp_award = int(self.table["xp award"].replace(',', ''))
        self.cr = float(self.table["cr"])

        self.fancy_name = self.table["fancy"]

        self.age, self.max_age = combat.char_roll.get_age(self.race,
                                                          self._class)

        self.change_gender()

        self.alignment = self.table['alignment']

        """
        weight: d&d 3.5 monster manual appears to have a table of creature's
        weight/size. If so, make a similar base per size table, creating of
        inheriting some variance.
        """
        combat.char_roll.get_age
        self.change_height_weight()

        self.death_func = effects.monster_death

    def set_att(self):
        """ ['strenght', 'dexterity', 'constitution',
        'intelligence', 'wisdom', 'charisma']"""

        if self.table["type"] in [
            "aberration", "vermin", "outsider", "undead", "magical beast",
            "ooze"
        ] and self.table['str'] == "-":
            self.table['str'] = 10

        if self.table["type"] in [
            "construct"
        ] and self.table['dex'] == "-":
            self.table['dex'] = 10

        """
        Constructs do not have a Constitution score. Any DCs or other
        Statistics that rely on a Constitution score treat a construct as
        having a score of 10 (no bonus or penalty).
        """
        if self.table["type"] in [
            "construct"
        ] and self.table['con'] == "-":
            self.table['con'] = 10

        """
        Undead creatures do not have a Constitution score. Undead use their
        Charisma score in place of their Constitution score when calculating
        hit points, Fortitude saves, and any special ability that relies on
        Constitution(such as when calculating a breath weapon’s DC).
        """
        if self.table["type"] in [
            "undead"
        ] and self.table['con'] == "-":
            self.table['con'] = self.table['cha']

        if self.table["type"] in [
            "vermin", "undead", "plant", "construct", "ooze", "magical beast",
            "outsider"
        ] and self.table['int'] == "-":
            self.table['int'] = 0

        # if table["Type"] == "undead": # ???
        # print(table)
        self.attributes = [0] * 6
        for att, i in zip(
                ['str', 'dex', 'con', 'int', 'wis', 'cha'],
                range(6)):
            self.attributes[i] = int(self.table[att])

    def set_save_mod(self):
        # {"fort": 0, "ref": 1, "will": 2}
        self.save_mod, self.specials_saves = combat.parse_saves.parse(
            self.table)

    def set_melee(self):
        self.melee = combat.parse_atk.parse_melee(
            self.table['melee'], verbose=False)
        if self.table['def_name'] == 'demilich':
            print(self.table['def_name'])
            print(self.melee)


if __name__ == '__main__':
    from mylib import compare_classes

    pc = Character()
    pc.test()
    beast = Beast()
    beast.test()
    exit()

    compare_classes.compare_classes(
        pc, beast,
        excluded=["alignments", "classes", "races", "first_name", "surname",
                  "height_", "weight_", "bestiary", "game", "hp_history",
                  "namegen", "table", "owner"],
        ordered=["name"])

