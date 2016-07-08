import sys
import os
import random
import re

try:
    import combat
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    import combat
from rnd_utils import RangedDictionary, test_range100

rnd_armor_grade = {
    # (armor/shield bonus, (n lvl x abilities))
    "lesser minor": RangedDictionary({
        range(1, 81): (1, []),
        range(81, 101): "specific"
    }),
    "greater minor": RangedDictionary({
        range(1, 27): (1, []),
        range(27, 54): (2, []),
        range(54, 81): (1, [1]),
        range(81, 101): "specific"
    }),
    "lesser medium": RangedDictionary({
        range(1, 11): (1, []),
        range(11, 21): (2, []),
        range(21, 33): (3, []),
        range(33, 45): (1, [1]),
        range(45, 57): (1, [1, 2]),
        range(57, 69): (1, [2]),
        range(69, 81): (2, [1]),
        range(81, 101): "specific"
    }),
    "greater medium": RangedDictionary({
        range(1, 11): (2, []),
        range(11, 23): (3, []),
        range(23, 33): (1, [1]),
        range(33, 45): (1, [2]),
        range(45, 57): (2, [1]),
        range(57, 69): (2, [2]),
        range(69, 81): (3, [1]),
        range(81, 101): "specific"
    }),
    "lesser major": RangedDictionary({
        range(1, 11): (3, []),
        range(11, 23): (4, []),
        range(23, 33): (1, [2]),
        range(33, 45): (1, [3]),
        range(45, 57): (2, [2]),
        range(57, 69): (3, [1]),
        range(69, 81): (4, [1]),
        range(81, 101): "specific"
    }),
    "greater major": RangedDictionary({
        range(1, 11): (4, []),
        range(11, 21): (5, []),
        range(21, 31): (4, [1]),
        range(31, 39): (4, [2]),
        range(39, 47): (4, [3]),
        range(47, 52): (4, [4]),
        range(52, 60): (5, [1]),
        range(60, 68): (5, [2]),
        range(68, 72): (5, [3]),
        range(72, 75): (5, [2, 2]),
        range(75, 78): (5, [4]),
        range(78, 81): (5, [5]),
        range(81, 101): "specific"
    })
}

rnd_armor_abilities = {
    1: {
        'armor': RangedDictionary({
            range(1, 7): "benevolent",
            range(7, 13): "poison-resistant",
            range(13, 19): "balanced",
            range(19, 25): "bitter",
            range(25, 31): "bolstering",
            range(31, 37): "brawling",
            range(37, 43): "champion",
            range(43, 49): "dastard",
            range(49, 55): "deathless",
            range(55, 61): "defiant",
            range(61, 67): "fortification (light)",
            range(67, 72): "grinding",
            range(72, 77): "impervious",
            range(77, 83): "mirrored",
            range(83, 89): "spell storing",
            range(89, 95): "stanching",
            range(95, 101): "warding"
        }),
        'shield': RangedDictionary({
            range(1, 11): "poison-resistant",
            range(11, 20): "arrow catching",
            range(20, 29): "bashing",
            range(29, 38): "blinding",
            range(38, 47): "clangorous",
            range(47, 56): "defiant",
            range(56, 65): "fortification (light)",
            range(65, 74): "grinding",
            range(74, 83): "impervious",
            range(83, 92): "mirrored",
            range(92, 101): "ramming"
        })
    },
    2: {
        'armor': RangedDictionary({
            range(1, 13): "glamered",
            range(13, 25): "jousting",
            range(25, 39): "shadow",
            range(39, 53): "slick",
            range(53, 65): "expeditious",
            range(65, 77): "creeping",
            range(77, 89): "rallying",
            range(89, 101): "spell resistance (13)"
        }),
        'shield': RangedDictionary({
            range(1, 16): "rallying",
            range(16, 31): "wyrmsbreath",
            range(31, 51): "animated",
            range(51, 68): "arrow deflection",
            range(68, 83): "merging",
            range(83, 101): "spell resistance (13)"
        })
    },
    3: {
        'armor': RangedDictionary({
            range(1, 9): "adhesive",
            range(9, 18): "hosteling",
            range(18, 27): "radiant",
            range(27, 37): "delving",
            range(37, 46): "putrid",
            range(46, 56): "fortification (moderate)",
            range(56, 66): "ghost touch",
            range(66, 75): "invulnerability",
            range(75, 85): "spell resistance (15)",
            range(85, 93): "titanic",
            range(93, 101): "wild"
        }),
        'shield': RangedDictionary({
            range(1, 16): "hosteling",
            range(16, 33): "radiant",
            range(33, 50): "fortification (moderate)",
            range(50, 67): "ghost touch",
            range(67, 84): "spell resistance (15)",
            range(84, 101): "wild"
        })
    },
    4: {
        'armor': RangedDictionary({
            range(1, 17): "harmonizing",
            range(17, 34): "shadow, improved",
            range(34, 51): "slick, improved",
            range(51, 68): "energy resistance",
            range(68, 84): "martyring",
            range(84, 101): "spell resistance (17)"
        }),
        'shield': RangedDictionary({
            range(1, 51): "energy resistance",
            range(51, 101): "spell resistance (17)"
        })
    },
    5: {
        'armor': RangedDictionary({
            range(1, 9): "righteous",
            range(9, 16): "unbound",
            range(16, 24): "unrighteous",
            range(24, 31): "vigilant",
            range(31, 38): "determination",
            range(38, 46): "shadow, greater",
            range(46, 54): "slick, greater",
            range(54, 62): "energy resistance, improved",
            range(62, 70): "etherealness",
            range(70, 77): "undead controlling",
            range(77, 85): "energy resistance, greater",
            range(85, 93): "fortification (heavy)",
            range(93, 101): "spell resistance (19)"
        }),
        'shield': RangedDictionary({
            range(1, 12): "determination",
            range(12, 28): "energy resistance, improved",
            range(28, 39): "undead controlling",
            range(39, 56): "energy resistance, greater",
            range(56, 71): "fortification (heavy)",
            range(71, 86): "reflecting",
            range(86, 101): "spell resistance (19)"
        })
    }
}

all_armor_abilities = set({
    ability
    for level in rnd_armor_abilities.values()
    for _type in level.values()
    for ability in _type.values()})

rnd_armor_type = RangedDictionary({
    range(1, 5): ("banded mail", "armor"),
    range(5, 12): ("breastplate", "armor"),
    range(12, 15): ("buckler", "armor"),
    range(15, 22): ("chain shirt", "armor"),
    range(22, 28): ("chainmail", "armor"),
    range(28, 35): ("full plate", "armor"),
    range(35, 40): ("half-plate", "armor"),
    range(40, 46): ("heavy steel shield", "armor"),
    range(46, 52): ("heavy wooden shield", "armor"),
    range(52, 56): ("hide", "armor"),
    range(56, 62): ("leather armor", "armor"),
    range(62, 66): ("light steel shield", "armor"),
    range(66, 70): ("light wooden shield", "armor"),
    range(70, 73): ("padded armor", "armor"),
    range(73, 78): ("scale mail", "armor"),
    range(78, 82): ("splint mail", "armor"),
    range(82, 88): ("studded leather armor", "armor"),
    range(88, 91): ("tower shield", "armor"),
    range(91, 94): ("light armor, other)", "armor"),
    range(94, 96): ("medium armor, other", "armor"),
    range(96, 99): ("heavy armor, other", "armor"),
    range(99, 101): ("shield, other", "armor")
})

rnd_specific_armor = {
    "lesser minor": RangedDictionary({
        range(1, 21): ("living steel heavy shield", 120),
        range(21, 46): ("darkwood buckler", 203),
        range(46, 71): ("darkwood shield", 257),
        range(71, 101): ("mithral heavy shield", 1020),
    }),
    "greater minor": RangedDictionary({
        range(1, 31): ("zombie skin shield", 2159),
        range(31, 76): ("caster's shield", 3153),
        range(76, 101): ("burglar's buckler", 4655),
    }),
    "lesser medium": RangedDictionary({
        range(1, 36): ("spined shield", 5580),
        range(36, 51): ("dragonslayer's shield", 7170),
        range(51, 66): ("collapsible tower", 8170),
        range(66, 101): ("lion's shield", 9170),
    }),
    "greater medium": RangedDictionary({
        range(1, 21): ("caster's shield, greater", 10153),
        range(21, 41): ("celestial shield", 13170),
        range(41, 61): ("maelstrom shield", 14170),
        range(61, 81): ("volcanic shield", 14170),
        range(81, 101): ("tempest shield", 15170),
    }),
    "lesser major": RangedDictionary({
        range(1, 21): ("battlement shield", 16180),
        range(21, 41): ("winged shield", 17257),
        range(41, 61): ("avalanche shield", 19170),
        range(61, 81): ("fortress shield", 19180),
        range(81, 101): ("wyrmslayer's shield", 20170),
    }),
    "greater major": RangedDictionary({
        range(1, 21): ("spell ward tower shield", 25180),
        range(21, 36): ("quick block buckler", 36155),
        range(36, 51): ("belligerent shield", 36170),
        range(51, 66): ("force tower", 46030),
        range(66, 86): ("absorbing shield", 50170),
        range(86, 101): ("elysian shield", 52620),
    })
}


def get_armor_by_grade(grade):
    d100 = lambda: (random.randint(1, 100))

    armor_name, weapon_type = rnd_armor_type[d100()]
    rnd_grade = rnd_armor_grade[grade][d100()]
    if rnd_grade == "specific":
        cost, weapon = rnd_specific_armor[grade][d100()]
        # bonus?
        # ability_lvls?
        print("{} {}: {}".format(grade, weapon_type, armor_name))
    else:

        try:
            bonus, ability_lvls = rnd_grade
        except ValueError:
            print(rnd_grade)
            raise ValueError
        abilities = []
        for i in ability_lvls:
            abilities.append(rnd_armor_abilities[i][weapon_type][d100()])
        print("{} {}: {} +{}, {}".format(
            grade, weapon_type, armor_name, bonus, abilities))

    exit()

    spell_lvl, caster_lvl = rnd_scrolls_grade[grade][d100()]
    scroll_rarity, scroll_type = rnd_scrolls_type[d100()]

    scroll = rnd_scrolls[scroll_type][spell_lvl][scroll_rarity][d100()]

    # TO-DO: IMPLEMENT CASTER LEVEL

    return scroll

def get_weapon(string):
    pattern = ""


if __name__ == '__main__':
    test_range100(rnd_armor_type)
    test_range100(rnd_armor_grade)
    test_range100(rnd_armor_abilities)
    test_range100(rnd_specific_armor)

    grades = ["lesser minor", "greater minor", "lesser medium",
              "greater medium", "lesser major", "greater major"]

    get_armor_by_grade(random.choice(grades))
