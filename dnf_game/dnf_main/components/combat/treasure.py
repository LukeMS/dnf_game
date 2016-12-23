"""..."""

import random
import json
from pprint import pprint
import re

from dnf_game.dnf_main.components.combat import loot_coins
from dnf_game.dnf_main.components.combat import loot_gems
from dnf_game.dnf_main.data_handler.bestiary import Bestiary


treasure_budget = {
    "none": 0,
    "incidental": 0.5,
    "standard": 1,
    "double": 2,
    "triple": 3
}

"""Treasure Values per Encounter"""
treasure_values = {
    # http://www.d20pfsrd.com/gamemastering#Table-Treasure-Values-per-Encounter
    # APL: [Slow, Medium, Fast]
    0.13: [20, 35, 50],  # 1/8
    0.17: [30, 45, 65],  # 1/6
    0.25: [40, 65, 100],  # 1/4
    0.33: [55, 85, 135],  # 1/3
    0.5: [85, 130, 200],  # 1/2
    1: [170, 260, 400],
    2: [350, 550, 800],
    3: [550, 800, 1200],
    4: [750, 1150, 1700],
    5: [1000, 1550, 2300],
    6: [1350, 2000, 3000],
    7: [1750, 2600, 3900],
    8: [2200, 3350, 5000],
    9: [2850, 4250, 6400],
    10: [3650, 5450, 8200],
    11: [4650, 7000, 10500],
    12: [6000, 9000, 13500],
    13: [7750, 11600, 17500],
    14: [10000, 15000, 22000],
    15: [13000, 19500, 29000],
    16: [16500, 25000, 38000],
    17: [22000, 32000, 48000],
    18: [28000, 41000, 62000],
    19: [35000, 53000, 79000],
    20: [44000, 67000, 100000],
    21: [55000, 84000, 125000],
    22: [69000, 104000, 155000],
    23: [85000, 127000, 190000],
    24: [102000, 155000, 230000],
    25: [125000, 185000, 275000],
    26: [150000, 220000, 330000],
    27: [175000, 260000, 390000],
    28: [205000, 305000, 460000],
    29: [240000, 360000, 540000],
    30: [280000, 420000, 630000]
}

npc_gear_table = {
    0.13: 35,  # 1/8
    0.17: 45,  # 1/6
    0.25: 65,  # 1/4
    0.33: 85,  # 1/3
    0.5: 130,  # 1/2
    1: 260,
    2: 390,
    3: 780,
    4: 1650,
    5: 2400,
    6: 3450,
    7: 4650,
    8: 6000,
    9: 7800,
    10: 10050,
    11: 12750,
    12: 16350,
    13: 21000,
    14: 27000,
    15: 34800,
    16: 45000,
    17: 58500,
    18: 75000,
    19: 96000,
    20: 123000
}



"""
"Standard" treasure indicates the total value of the creature's treasure
is that of a CR equal to the average party level, as listed on
Table 12-5 on page 399 in the  Core Rulebook.
"Double" or "triple" treasure indicates the creature has double or triple
this standard value.
"Incidental" indicates the creature has half this standard value, and then
only within the confines of its lair.
"None" indicates that the creature normally has no treasure (as is typical for
an unintelligent creature that has no real lair, although such creatures are
often used to guard treasures of varying amounts).
"NPC gear" indicates the monster has treasure as normal for an NPC of a level
equal to the monster's CR (see page 454 of the  Core Rulebook).
"""

"""
Monsters with specified treasure:

The Goblin entry lists its NPC Gear as:
Treasure: NPC gear (leather armor, light wooden shield, short sword, short bow
with 20 arrows, other treasure).
Totalling up everything (except "other treasure" of course) gives a value of
54gp. You could thus assume you have 32gp (86-54) of wiggling room. Either
give them about 30gp or an item worth about that much.
(http://rpg.stackexchange.com/a/40954/26974)
"""


def get_treasure_budget(creature):
    search_type = re.search(
        '(?P<type>none|incidental|standard|double|triple|npc gear)',
        creature['treasure'], re.I)
    if search_type:
        d = {}
        d['name'] = creature['def_name']
        d['cr'] = float(creature['cr'])
        d['treasure'] = creature['treasure']
        stats = {}
        for stat in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            stats[stat] = creature[stat]
        d['stats'] = stats

        d['type'] = search_type.group("type").lower()
        if d['type'] != "npc gear":
            base_value = treasure_values[d['cr']][0]
            d['value'] = treasure_budget[d['type']] * base_value
        else:
            d['value'] = npc_gear_table[d['cr']]
        return d
    else:
        raise ValueError('"{}": "{}" (source: {})'.format(
            creature['def_name'], creature['treasure'], creature['source']))


def get_treasure_types(creature, budget):

    # Aberration: Many aberrations have little use for treasure, possessing
    # only what hangs from the remains of their previous victims. Others are
    # cunning adversaries that use various magic items and treasure to enhance
    # their abilities.
    #
    # Treasure Types: A, B, D, E (add F, G, H if the creature is cunning).
    if creature['type'] == "aberration":
        if budget['type'] not in ['none', 'incidental', 'standard']:
            return ["A", "B", "D", "E", "F", "G", "H"]
        else:
            return ["A", "B", "D", "E"]

    # Animal: Animals place little to no value on treasure, instead leaving
    # such coins and objects with the remains of their meals. For those with
    # treasure, it is typically found in their lairs, scattered amid bones and
    # other refuse.
    #
    # Treasure Types: A, B, D, E.
    elif creature['type'] == "animal":
        return ["A", "B", "D", "E"]

    # Construct: The only treasure carried by constructs is usually part of
    # their construction, such as a weapon or magic item. Constructs are,
    # however, typically used to guard more valuable treasures or magic items.
    #
    # Treasure Types: E, F (add B, C, H if the creature is guarding a
    # treasure).
    elif creature['type'] == "construct":
        return ["E", "F"]

    # Dragon: Known for their valuable treasures, dragons often brood over
    # vast piles of coins, gems, magic items, and other expensive objects.
    #
    # Treasure Types: A, B, C, H, I.
    elif creature['type'] == "dragon":
        return ["A", "B", "C", "H", "I"]

    # Fey: Above all other things, fey value items of magic and beauty. They
    # have little use for tools of trade and commerce used by the more
    # civilized races, such as coins and valuables.
    #
    # Treasure Types: B, C, D, G.
    elif creature['type'] == "fey":
        return ["B", "C", "D", "G"]

    # Humanoid: Creatures of this type are quite varied, but even the most
    # primitive humanoids use gear and magic items to some extent. In bigger
    # groups such as communities, humanoids often posses larger amounts of
    # treasure that they collectively guard.
    #
    # Treasure Types: A, B, D, E, F, G (add H for an entire community).
    elif creature['type'] == "humanoid":
        return ["A", "B", "D", "E", "F", "G"]

    # Magical Beast: Caring little for valuables, most magical beasts are only
    # in search of their next meal. The lairs of these creatures are often
    # strewn with a few valuable trinkets and magic items.
    #
    # Treasure Types: A, B, D, E.
    elif creature['type'] == "magical beast":
        return ["A", "B", "D", "E"]

    # Monstrous Humanoid: Most monstrous humanoids care only about treasures
    # that they can use, although some have been known to hoard valuables in
    # their lairs.
    #
    # Treasure Types: A, B, C, D, E, H.
    elif creature['type'] == "monstrous humanoid":
        return ["A", "B", "C", "D", "E", "H"]

    # Ooze: Oozes have no concept of treasure and leave any they find behind
    # as they search for their next meal. Any treasure they might carry is
    # entirely accidental.
    #
    # Treasure Types: A, B, D.
    elif creature['type'] == "ooze":
        return ["A", "B", "D"]

    # Outsider: Outsiders are one of the most varied creature types and as a
    # result might truly have any type of treasure on them or hidden in their
    # lair. The GM should consider the creature individually to determine the
    # treasure type that best fits the outsider.
    #
    # Treasure Types: any.
    elif creature['type'] == "outsider":
        return ["A", "B", "C", "D", "E", 'F', 'G', "H", "I"]

    # Plant: Like animals, plant creatures do not care for treasure, and any
    # that might be found where they grow is simply the indigestible remnants
    # of a previous victim.
    #
    # Treasure Types: A, B, D, E.
    elif creature['type'] == "plant":
        return ["A", "B", "D", "E"]

    # Undead: The treasure carried by undead varies depending on whether or
    # not the creature is intelligent. Unintelligent undead typically only
    # possess meager valuables carried on themselves in life, rarely actually
    # using such treasures, while intelligent undead take advantage of a wide
    # variety of magic items in order to destroy the living.
    #
    # Treasure Types:  (add F, G for intelligent undead).
    if creature['type'] == "undead":
        if (
            budget['type'] not in ['none', 'incidental'] and
            creature['int'] != '-' and
            int(creature['int']) > 4
        ):
            return ["A", "B", "D", "E", "F", "G"]
        else:
            return ["A", "B", "D", "E"]

    # Vermin: Like other mindless creatures, vermin do not covet treasure,
    # although such creatures are sometimes found infesting areas where
    # valuables are kept.
    #
    # Treasure Types: A, B, D.
    elif creature['type'] == "vermin":
        return ["A", "B", "D"]

    else:
        raise ValueError(creature['type'], "is not a valid creature type")


def set_percent_per_type(creature, treasure_types):
    percents = {}

    [percents.setdefault(k, 0) for k in treasure_types]

    total = 100

    attempts = 0
    i = len(treasure_types) - 1
    while True:
        # print(total)

        t_type = treasure_types[i]

        # we're finished
        if total == 0:
            break

        # trow the 15% left anywhere
        elif total <= 15:
            percents[t_type] += total
            total -= total
            break
        # this is taking too long
        elif attempts > len(treasure_types) * 2:
            percents[treasure_types[0]] += total
            total -= total
            break

        # its an item type
        if t_type > "C":
            # 50% chance to be ignored
            if random.randrange(100) >= 50:

                # not ignored, get some of the total
                chance = random.randrange(100)

                #   25% chance to take 100% of total
                if chance >= 75 or total <= 25:
                    percents[t_type] += total
                    total -= total

                #   25% chance to take 75% of total
                elif chance >= 50:
                    v = 5 * ((total * 0.75) // 5)
                    percents[t_type] += v
                    total -= v

                #   50% chance to take 50% of total
                else:
                    v = 5 * ((total * 0.5) // 5)
                    percents[t_type] += v
                    total -= v
        else:
            # not artwork for now...
            if t_type == "C":
                    t_type = treasure_types[0]

            #   50% chance to take 100% of total
            if total <= 25 or random.randrange(100) >= 50:
                percents[t_type] += total
                total -= total

            #   50% chance to take 50% of total
            else:
                v = 5 * ((total * 0.75) // 5)
                percents[t_type] += v
                total -= v

        attempts += 1
        i -= 1
        i = i % len(treasure_types)

    # print(json.dumps(creature, indent=4))
    # print(percents)

    if "F" in treasure_types and "G" in treasure_types:
        # both combatant and spellcaster gear...
        # pick the one that seems proper
        melee_value = max(creature['str'],
                          creature['con'],
                          creature['dex'])

        caster_value = max(creature['int'],
                           creature['wis'],
                           creature['cha'])

        try:
            if abs(melee_value - caster_value) > 5:
                # print('big dif')
                if random.randrange(100) < 50:
                    if melee_value > caster_value:
                        # print('removing "G"')
                        percents["F"] = percents["F"] + percents["G"]
                        percents["G"] = 0
                    else:
                        # print('removing "F"')
                        percents["G"] = percents["F"] + percents["G"]
                        percents["F"] = 0
        except TypeError:
            print(creature)
            raise TypeError

        # print("melee_value", melee_value)
        # print("caster_value", caster_value)
        # print('caster or melee?')

    return percents

print()


def set_value_per_type(value, percents):
    values = dict(percents)
    for k in values:
        values[k] = 5 * int(value / 100 * values[k] / 5)

    # total = sum(v for k, v in values.items())
    return {k: v for k, v in values.items() if v}


def set_hoard(values):
    hoard = {
        'coins': loot_coins.Coins(),
        'gems': []
    }
    if "A" in values:
        # Treasure of this type is made up entirely of coins.
        hoard['coins'] += loot_coins.calculate_hoard(values["A"])
        print(hoard['coins'])
    if "B" in values:
        res = loot_gems.calculate_hoard(values["B"])
        print(res['coins'])
        hoard['coins'] += res['coins']
        hoard['gems'].extend(res['gems'])
    if "C" in values:
        print("WTF!!! treasure type c")
    if "D" in values:
        pass

    return hoard


def main(creature):
    """..."""
    budget = get_treasure_budget(creature)

    treasure_types = get_treasure_types(creature, budget)

    treasure_percents = set_percent_per_type(creature, treasure_types)

    treasure_values = set_value_per_type(budget["value"], treasure_percents)

    hoard = set_hoard(treasure_values)

    for info in ['type', 'description']:
        budget[info] = creature[info]

    budget["treasure_types"] = treasure_types
    budget["treasure_percents"] = treasure_percents
    budget["treasure_values"] = treasure_values
    budget["hoard"] = hoard

    pprint(budget, indent=4)


if __name__ == '__main__':
    results = Bestiary.get_filtered(filter_list=[
        ('treasure', None, 'search', False)
    ])
    print(results)
    tables = {}

    for i, result in enumerate(results):
        tables[result] = main(Bestiary.get(result))

    with open('treasure_gen_test.json', 'w') as outfile:
        json.dump(tables, outfile, indent=4)
        # json.dumps(tables, indent=4)
"""
description:
view&mdash;
"""
