"""..."""

import random

from dnf_game.util.rnd_utils import RangedDictionary, test_range100

rnd_potions = {
    0: {
        'common': RangedDictionary({
            range(1, 15): 'arcane mark',
            range(15, 29): 'guidance',
            range(29, 45): 'light',
            range(45, 59): 'purify food and drink',
            range(59, 73): 'resistance',
            range(73, 87): 'stabilize',
            range(87, 101): 'virtue'
        })
    },
    1: {
        'common': RangedDictionary({
            range(1, 5): 'bless weapon',
            range(5, 15): 'cure light wounds',
            range(15, 20): 'endure elements',
            range(20, 28): 'enlarge person',
            range(28, 34): 'jump',
            range(34, 42): 'mage armor',
            range(42, 48): 'magic fang',
            range(48, 56): 'magic weapon',
            range(56, 61): 'pass without trace',
            range(61, 65): 'protection from chaos',
            range(65, 69): 'protection from evil',
            range(69, 73): 'protection from good',
            range(73, 77): 'protection from law',
            range(77, 82): 'reduce person',
            range(82, 88): 'remove fear',
            range(88, 93): 'sanctuary',
            range(93, 101): 'shield of faith'
        }),
        'uncommon': RangedDictionary({
            range(1, 5): 'animate rope',
            range(5, 12): 'ant haul',
            range(12, 17): 'cloak of the shade',
            range(17, 21): 'erase',
            range(21, 27): 'feather step',
            range(27, 31): 'goodberry',
            range(31, 35): 'grease',
            range(35, 42): 'hide from animals',
            range(42, 50): 'hide from undead',
            range(50, 54): 'hold portal',
            range(54, 59): 'invigorate',
            range(59, 65): 'keen senses',
            range(65, 69): 'magic stone',
            range(69, 76): 'remove sickness',
            range(76, 81): 'sanctify corpse',
            range(81, 85): 'shillelagh',
            range(85, 93): 'touch of the sea',
            range(93, 101): 'vanish',
        })
    },
    2: {
        'common': RangedDictionary({
            range(1, 5): 'aid',
            range(5, 8): 'align weapon',
            range(8, 12): 'barkskin',
            range(12, 17): "bear's endurance",
            range(17, 21): 'blur',
            range(21, 26): "bull's strength",
            range(26, 31): "cat's grace",
            range(31, 38): 'cure moderate wounds',
            range(38, 42): 'darkvision',
            range(42, 45): 'delay poison',
            range(45, 50): "eagle's splendor",
            range(50, 55): "fox's cunning",
            range(55, 62): 'invisibility',
            range(62, 67): 'levitate',
            range(67, 72): "owl's wisdom",
            range(72, 74): 'protection from arrows',
            range(74, 77): 'remove paralysis',
            range(77, 81): 'resist energy, acid',
            range(81, 85): 'resist energy, cold',
            range(85, 89): 'resist energy, electricity',
            range(89, 93): 'resist energy, fire',
            range(93, 95): 'resist energy, sonic',
            range(95, 99): 'spider climb',
            range(99, 101): 'undetectable alignment',
        }),
        'uncommon': RangedDictionary({
            range(1, 7): 'ablative barrier',
            range(7, 15): 'acute senses',
            range(15, 20): 'arcane lock',
            range(20, 25): 'bullet shield',
            range(25, 31): 'certain grip',
            range(31, 36): 'continual flame',
            range(36, 41): 'corruption resistance',
            range(41, 49): 'disguise other',
            range(49, 57): 'gentle repose',
            range(57, 62): 'make whole',
            range(62, 68): 'obscure object',
            range(68, 73): 'reduce animal',
            range(73, 77): 'rope trick',
            range(77, 83): 'slipstream',
            range(83, 91): 'status',
            range(91, 96): 'warp wood',
            range(96, 101): 'wood shape',
        })
    },
    3: {
        'common': RangedDictionary({
            range(1, 7): 'cure serious wounds',
            range(7, 11): 'dispel magic',
            range(11, 15): 'displacement',
            range(15, 21): 'fly',
            range(21, 26): 'gaseous form',
            range(26, 30): 'good hope',
            range(30, 36): 'haste',
            range(36, 41): 'heroism',
            range(41, 45): 'keen edge',
            range(45, 49): 'magic fang, greater',
            range(49, 53): 'magic vestment',
            range(53, 58): 'neutralize poison',
            range(58, 61): 'protection from energy, acid',
            range(61, 64): 'protection from energy, cold',
            range(64, 67): 'protection from energy, electricity',
            range(67, 70): 'protection from energy, fire',
            range(70, 72): 'protection from energy, sonic',
            range(72, 75): 'rage',
            range(75, 78): 'remove blindness/deafness',
            range(78, 82): 'remove curse',
            range(82, 87): 'remove disease',
            range(87, 92): 'tongues',
            range(92, 97): 'water breathing',
            range(97, 101): 'water walk'
        }),
        'uncommon': RangedDictionary({
            range(1, 11): 'burrow',
            range(11, 23): 'countless eyes',
            range(23, 35): 'daylight',
            range(35, 50): 'draconic reservoir',
            range(50, 59): 'flame arrow',
            range(59, 68): 'shrink item',
            range(68, 78): 'stone shape',
            range(78, 88): 'fire trap',
            range(88, 101): 'nondetection'
        })
    }
}

rnd_potions_grade = {
    #                (spell level, caster level, type)
    "lesser minor": RangedDictionary({
        range(1, 41): (0, 1),
        range(41, 101): (1, 1)
    }),
    "greater minor": RangedDictionary({
        range(1, 11): (0, 1),
        range(11, 61): (1, 1),
        range(61, 101): (2, 3)
    }),
    "lesser medium": RangedDictionary({
        range(1, 26): (1, 1),
        range(26, 86): (2, 3),
        range(86, 101): (3, 5)
    }),
    "greater medium": RangedDictionary({
        range(1, 11): (1, 1),
        range(11, 51): (2, 3),
        range(51, 101): (3, 5)
    }),
    "lesser major": RangedDictionary({
        range(1, 36): (2, 3),
        range(36, 101): (3, 5)
    }),
    "greater major": RangedDictionary({
        range(1, 11): (2, 3),
        range(11, 101): (3, 5)
    })
}

rnd_potions_rarity = RangedDictionary({
    range(1, 76): "common",
    range(76, 101): "uncommon"
})


def get_potion(grade):
    """..."""
    def d100():
        return random.randint(1, 100)

    spell_lvl, caster_lvl = rnd_potions_grade[grade][d100()]
    if spell_lvl > 0:
        rarity = rnd_potions_rarity[d100()]
    else:
        rarity = "common"
    potion = rnd_potions[spell_lvl][rarity][d100()]

    # TO-DO: IMPLEMENT CASTER LEVEL

    return potion

if __name__ == '__main__':
    test_range100(rnd_potions_rarity)
    test_range100(rnd_potions_grade)
    test_range100(rnd_potions)

    for g in ["lesser minor", "greater minor", "lesser medium",
              "greater medium", "lesser major", "greater major"]:
        print("{}: {}".format(g, get_potion(g)))
