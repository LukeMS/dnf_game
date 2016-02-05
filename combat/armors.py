import sys
import os
import random

if not os.path.isdir('combat'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rnd_utils import RangedDictionary, test_range100


rnd_weapons_grade = {
    # (weapon bonus, (n lvl x abilities))
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
        range(45, 57): (1, [1, 1]),
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
        range(72, 75): (5, [4]),
        range(75, 78): (5, [4, 1]),
        range(78, 81): (5, [3, 2]),
        range(81, 101): "specific"
    })
}

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

rnd_armors_abilities = {
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

rnd_weapons_abilities = {
    1: {
        'melee': RangedDictionary({
            range(1, 2): "impervious",
            range(2, 3): "glamered",
            range(3, 4): "allying",
            range(4, 9): "bane",
            range(9, 10): "benevolent",
            range(10, 11): "called",
            range(11, 13): "conductive",
            range(13, 17): "corrosive",
            range(17, 18): "countering",
            range(18, 19): "courageous",
            range(19, 20): "cruel",
            range(20, 22): "cunning",
            range(22, 23): "deadly",
            range(23, 27): "defending",
            range(27, 28): "dispelling",
            range(28, 34): "flaming",
            range(34, 40): "frost",
            range(40, 42): "furious",
            range(42, 46): "ghost touch",
            range(46, 48): "grayflame",
            range(48, 49): "grounding",
            range(49, 50): "guardian",
            range(50, 51): "heartseeker",
            range(51, 53): "huntsman",
            range(53, 55): "jurist",
            range(55, 60): "keen",
            range(60, 62): "ki focus",
            range(62, 63): "limning",
            range(63, 65): "menacing",
            range(65, 66): "merciful",
            range(66, 69): "mighty cleaving",
            range(69, 70): "mimetic",
            range(70, 71): "neutralizing",
            range(71, 72): "ominous",
            range(72, 73): "planar",
            range(73, 74): "quenching",
            range(74, 75): "seaborne",
            range(75, 81): "shock",
            range(81, 86): "spell storing",
            range(86, 87): "thawing",
            range(87, 92): "throwing",
            range(92, 97): "thundering",
            range(97, 98): "valiant",
            range(98, 101): "vicious"
        }),
        'ranged': RangedDictionary({
            range(1, 2): "adaptive",
            range(2, 3): "impervious",
            range(3, 4): "glamered",
            range(4, 7): "allying",
            range(7, 16): "bane",
            range(16, 17): "called",
            range(17, 20): "conductive",
            range(20, 21): "conserving",
            range(21, 25): "corrosive",
            range(25, 26): "cruel",
            range(26, 29): "cunning",
            range(29, 37): "distance",
            range(37, 46): "flaming",
            range(46, 55): "frost",
            range(55, 59): "huntsman",
            range(59, 63): "jurist",
            range(63, 64): "limning",
            range(64, 65): "lucky",
            range(65, 67): "merciful",
            range(67, 68): "planar",
            range(68, 69): "reliable",
            range(69, 77): "returning",
            range(77, 85): "seeking",
            range(85, 93): "shock",
            range(93, 101): "thundering"
        })
    },
    2: {
        'melee': RangedDictionary({
            range(1, 2): "advancing",
            range(2, 11): "anarchic",
            range(11, 20): "anchoring",
            range(20, 21): "axiomatic",
            range(21, 28): "corrosive burst",
            range(28, 29): "defiant",
            range(29, 30): "dispelling burst",
            range(30, 39): "disruption",
            range(39, 48): "flaming burst",
            range(48, 49): "furyborn",
            range(49, 50): "glorious",
            range(50, 59): "holy",
            range(59, 68): "icy burst",
            range(68, 69): "igniting",
            range(69, 70): "impact",
            range(70, 71): "invigorating",
            range(71, 72): "ki intensifying",
            range(72, 73): "lifesurge",
            range(73, 74): "negating",
            range(74, 75): "phase locking",
            range(75, 84): "shocking burst",
            range(84, 85): "stalking",
            range(85, 92): "unholy",
            range(92, 101): "wounding"
        }),
        'ranged': RangedDictionary({
            range(1, 11): "anarchic",
            range(11, 14): "anchoring",
            range(14, 24): "axiomatic",
            range(24, 32): "corrosive burst",
            range(32, 35): "designating, lesser",
            range(35, 38): "endless ammunition",
            range(38, 49): "flaming burst",
            range(49, 59): "holy",
            range(59, 70): "icy burst",
            range(70, 74): "igniting",
            range(74, 77): "phase locking",
            range(77, 87): "shocking burst",
            range(87, 91): "stalking",
            range(91, 101): "unholy"
        })
    },
    3: {
        'melee': RangedDictionary({
            range(1, 21): "nullifying",
            range(21, 41): "repositioning",
            range(41, 81): "speed",
            range(81, 101): "spellstealing"
        }),
        'ranged': RangedDictionary({
            range(1, 26): "lucky, greater",
            range(26, 46): "reliable, greater",
            range(46, 86): "speed",
            range(86, 95): "brilliant energy",
            range(95, 97): "designating, greater",
            range(97, 99): "nimble shot",
            range(99, 101): "second chance"
        })
    },
    4: {
        'melee': RangedDictionary({
            range(1, 41): "brilliant energy",
            range(41, 81): "dancing",
            range(81, 91): "vorpal",
            range(91, 96): "transformative",
            range(96, 101): "dueling"
        }),
        'ranged': RangedDictionary({
            range(1, 26): "lucky, greater",
            range(26, 46): "reliable, greater",
            range(46, 86): "speed",
            range(86, 95): "brilliant energy",
            range(95, 97): "designating, greater",
            range(97, 99): "nimble shot",
            range(99, 101): "second chance"
        })
    }
}

rnd_armors_type = RangedDictionary({
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

rnd_weapons_type = RangedDictionary({
    range(1, 2): ("bastard sword", "melee"),
    range(2, 6): ("battleaxe", "melee"),
    range(6, 7): ("bolas", "melee"),
    range(7, 9): ("club", "melee"),
    range(9, 11): ("composite longbow", "ranged"),
    range(11, 13): ("composite shortbow", "ranged"),
    range(13, 17): ("dagger", "melee"),
    range(17, 18): ("dart", "ranged"),
    range(18, 19): ("dwarven waraxe", "melee"),
    range(19, 20): ("falchion", "melee"),
    range(20, 21): ("gauntlet", "melee"),
    range(21, 22): ("glaive", "melee"),
    range(22, 25): ("greataxe", "melee"),
    range(25, 26): ("greatclub", "melee"),
    range(26, 29): ("greatsword", "melee"),
    range(29, 30): ("halberd", "melee"),
    range(30, 31): ("handaxe", "melee"),
    range(31, 34): ("heavy crossbow", "ranged"),
    range(34, 35): ("heavy flail", "melee"),
    range(35, 36): ("heavy mace", "melee"),
    range(36, 38): ("lance", "melee"),
    range(38, 41): ("light crossbow", "ranged"),
    range(41, 42): ("light flail", "melee"),
    range(42, 43): ("light hammer", "melee"),
    range(43, 45): ("light mace", "melee"),
    range(45, 46): ("light pick", "melee"),
    range(46, 50): ("longbow", "ranged"),
    range(50, 52): ("longspear", "melee"),
    range(52, 59): ("longsword", "melee"),
    range(59, 61): ("morningstar", "melee"),
    range(61, 62): ("nunchaku", "melee"),
    range(62, 64): ("quarterstaff", "melee"),
    range(64, 66): ("rapier", "melee"),
    range(66, 67): ("sai ", "melee"),
    range(67, 68): ("sap ", "melee"),
    range(68, 70): ("scythe ", "melee"),
    range(70, 74): ("shortbow ", "ranged"),
    range(74, 76): ("shortspear ", "melee"),
    range(76, 81): ("shortsword ", "melee"),
    range(81, 82): ("shuriken ", "melee"),
    range(82, 83): ("sickle ", "melee"),
    range(83, 85): ("sling", "melee"),
    range(85, 88): ("spear", "melee"),
    range(88, 89): ("trident", "melee"),
    range(89, 92): ("warhammer", "melee"),
    range(92, 93): ("whip", "melee"),
    range(93, 95): ("light melee weapon, other", "melee"),
    range(95, 97): ("one-handed melee weapon, other", "melee"),
    range(97, 99): ("two-handed melee weapon, other", "melee"),
    range(99, 101): ("ranged weapon, other", "ranged")
})

rnd_weapons_specific = {
    "lesser minor": RangedDictionary({
        range(1, 3): ("tracer bullet", 100),
        range(3, 9): ("sleep arrow", 132),
        range(9, 11): ("dustburst bullet", 196),
        range(11, 17): ("tangle bolt", 226),
        range(17, 23): ("screaming bolt", 267),
        range(23, 33): ("masterwork silver dagger", 322),
        range(33, 35): ("alchemist's bullet", 330),
        range(35, 45): ("cold iron masterwork longsword", 330),
        range(45, 51): ("hushing arrow", 547),
        range(51, 57): ("hushing arrow, greater", 1047),
        range(57, 67): ("javelin of lightning", 1500),
        range(67, 75): ("searing arrow", 1516),
        range(75, 83): ("sizzling arrow", 1516),
        range(83, 85): ("burrowing bullet, lesser", 1722),
        range(85, 93): ("dust bolt", 1730),
        range(93, 101): ("slaying arrow", 2282),
    }),
    "greater minor": RangedDictionary({
        range(1, 21): ("adamantine dagger", 3002),
        range(21, 41): ("adamantine battleaxe", 3010),
        range(41, 51): ("burrowing bullet, greater", 3447),
        range(51, 71): ("slaying arrow, greater", 4057),
        range(71, 81): ("lance of jousting", 4310),
        range(81, 101): ("shatterspike", 4315),
    }),
    "lesser medium": RangedDictionary({
        range(1, 4): ("bloodletting kukri", 6308),
        range(4, 10): ("boulderhead mace", 6812),
        range(10, 15): ("beaststrike club", 7300),
        range(15, 21): ("fighter's fork", 7315),
        range(21, 24): ("everflowing aspergillum", 7805),
        range(24, 29): ("hurricane quarterstaff", 7840),
        range(29, 35): ("dagger of venom", 8302),
        range(35, 40): ("gloom blade", 8810),
        range(40, 44): ("frostbite sling", 9380),
        range(45, 50): ("trident of stability", 9815),
        range(50, 55): ("trident of warning", 10115),
        range(55, 61): ("assassin's dagger", 10302),
        range(61, 67): ("dagger of doubling", 10302),
        range(67, 72): ("earthenflail", 11315),
        range(72, 80): ("swift obsidian greataxe", 11320),
        range(80, 86): ("polarity hammer", 12310),
        range(86, 94): ("blade of binding", 12350),
        range(94, 101): ("shifter's sorrow", 12780),
    }),
    "greater medium": RangedDictionary({
        range(1, 8): ("dragoncatch guisarme", 13308),
        range(8, 16): ("ten-ring sword", 14315),
        range(16, 22): ("triton's trident", 15065),
        range(22, 30): ("mace of smiting, lesser", 16012),
        range(30, 38): ("disarming blade", 17820),
        range(38, 43): ("lash of the howler", 18305),
        range(43, 48): ("shieldsplitter lance", 18310),
        range(48, 54): ("trident of fish command", 18650),
        range(54, 60): ("quarterstaff of vaulting", 19100),
        range(60, 66): ("firedrake pistol", 20300),
        range(66, 72): ("ricochet hammer", 20301),
        range(72, 78): ("flame tongue", 20715),
        range(78, 86): ("sparkwake starknife", 21324),
        range(86, 91): ("luck blade (0 wishes)", 22060),
        range(91, 96): ("sword of subtlety", 22310),
        range(96, 101): ("sword of the planes", 22315),
    }),
    "lesser major": RangedDictionary({
        range(1, 13): ("nine lives stealer", 23057),
        range(13, 27): ("undercutting axe", 23310),
        range(27, 41): ("spirit caller", 25302),
        range(41, 56): ("dwarfbond hammer", 25312),
        range(56, 71): ("oathbow", 25600),
        range(71, 86): ("sword of life stealing", 25715),
        range(86, 101): ("cutthroat's apprentice", 33910),
    }),
    "greater major": RangedDictionary({
        range(1, 3): ("ghoul's lament", 35312),
        range(3, 6): ("mace of terror", 38552),
        range(6, 8): ("hellscourge", 39305),
        range(8, 10): ("dragon's doom", 40310),
        range(10, 14): ("life-drinker", 40320),
        range(14, 17): ("valor's minion", 41335),
        range(17, 19): ("summoner's sorrow", 42816),
        range(19, 22): ("sylvan scimitar", 47315),
        range(22, 24): ("spirit blade", 48502),
        range(24, 27): ("heartswood spear", 50302),
        range(27, 30): ("rapier of puncturing", 50320),
        range(30, 33): ("sun blade", 50335),
        range(33, 38): ("blade of the rising sun", 51850),
        range(38, 41): ("frost brand", 54475),
        range(41, 46): ("dwarven thrower", 60312),
        range(46, 51): ("bloodthirst dagger", 60802),
        range(51, 54): ("warbringer", 61375),
        range(54, 58): ("luck blade (1 wish)", 62360),
        range(58, 62): ("guarding blade", 65310),
        range(62, 65): ("pistol of the infinite sky", 73300),
        range(65, 70): ("mace of smiting", 75312),
        range(70, 74): ("blade of the sword-saint", 75350),
        range(74, 77): ("scimitar of the spellthief", 75815),
        range(77, 80): ("spider's fang", 79102),
        range(80, 83): ("demonsorrow curve blade", 90469),
        range(83, 86): ("void scythe", 95318),
        range(86, 90): ("luck blade (2 wishes)", 102660),
        range(90, 93): ("holy avenger", 120630),
        range(93, 97): ("bastard's sting", 123035),
        range(97, 101): ("luck blade (3 wishes)", 142960),
    })
}

rnd_armors_specific = {
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


def get_weapon(grade):
    d100 = lambda: (random.randint(1, 100))

    weapon_name, weapon_type = rnd_weapons_type[d100()]
    rnd_grade = rnd_weapons_grade[grade][d100()]
    if rnd_grade == "specific":
        cost, weapon = rnd_weapons_specific[grade][d100()]
        # bonus?
        # ability_lvls?
        print("{} {}: {}".format(grade, weapon_type, weapon_name))
    else:

        try:
            bonus, ability_lvls = rnd_grade
        except ValueError:
            print(rnd_grade)
            raise ValueError
        abilities = []
        for i in ability_lvls:
            abilities.append(rnd_weapons_abilities[i][weapon_type][d100()])
        print("{} {}: {} +{}, {}".format(
            grade, weapon_type, weapon_name, bonus, abilities))


    exit()




    spell_lvl, caster_lvl = rnd_scrolls_grade[grade][d100()]
    scroll_rarity, scroll_type = rnd_scrolls_type[d100()]

    scroll = rnd_scrolls[scroll_type][spell_lvl][scroll_rarity][d100()]

    # TO-DO: IMPLEMENT CASTER LEVEL

    return scroll


if __name__ == '__main__':
    # test_range100(rnd_armors_type)
    # test_range100(rnd_armor_grade)
    # test_range100(rnd_armors_abilities)
    test_range100(rnd_armors_specific)

    # test_range100(rnd_weapons_type)
    # test_range100(rnd_weapons_grade)
    # test_range100(rnd_weapons_abilities)
    test_range100(rnd_weapons_specific)

    grades = ["lesser minor", "greater minor", "lesser medium",
              "greater medium", "lesser major", "greater major"]
    get_weapon(random.choice(grades))
