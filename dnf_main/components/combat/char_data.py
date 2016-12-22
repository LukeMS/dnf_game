"""..."""

from dnf_game.util import RangedDictionary
# Fort Save, Ref Save, Will Save

data = {

    # playable races
    "races": [
        'dwarf',
        'elf',
        'gnome',
        'half-elf',
        'half-orc',
        'halfling',
        'human'
    ],
    # will be playable after implementation
    "__races__possible": [
        "aasimar",
        "catfolk",
        "changeling",
        "dhampir",
        "drow",
        "duergar",
        "dwarf",
        "elf",
        "fetchling",
        "gillman",
        "gnome",
        "goblin",
        "grippli",
        "half-elf",
        "half-orc",
        "halfling",
        "hobgoblin",
        "human",
        "ifrit",
        "kitsune",
        "kobold",
        "merfolk",
        "nagaji",
        "orc",
        "oread",
        "ratfolk",
        "samsaran",
        "strix",
        "suli",
        "svirfneblin",
        "sylph",
        "tengu",
        "tiefling",
        "undine",
        "vanara",
        "vishkanya",
        "wayang"],

    "race_mod": {
        'human': {},
        'dwarf': {'con': +2, 'cha': -2},
        'elf': {'dex': +2, 'con': -2},
        'gnome': {'con': +2, 'str': -2},
        'half-elf': {},
        'half-orc': {'str': +2, 'int': -2, 'cha': -2},
        'halfling': {'dex': +2, 'str': -2}
    },

    #######
    # LEVEL ADVANCEMENT
    #
    # Format:
    #   "level": ["slow", "medium", "fast"]
    #######
    "level_adv": [
        [0, 0, 0],
        [3000, 2000, 1300],
        [7500, 5000, 3300],
        [14000, 9000, 6000],
        [23000, 15000, 10000],
        [35000, 23000, 15000],
        [53000, 35000, 23000],
        [77000, 51000, 34000],
        [115000, 75000, 50000],
        [160000, 105000, 71000],
        [235000, 155000, 105000],
        [330000, 220000, 145000],
        [475000, 315000, 210000],
        [665000, 445000, 295000],
        [955000, 635000, 425000],
        [1350000, 890000, 600000],
        [1900000, 1300000, 850000],
        [2700000, 1800000, 1200000],
        [3850000, 2550000, 1700000],
        [5350000, 3600000, 2400000]
    ],

    "cr": [
        0.13,
        0.17,
        0.25,
        0.33,
        0.5,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25
    ],

    # "CR";"Total XP";"1–3";"4–5";"6+"
    "xp_award": {
        0.13: [50, 15, 15, 10],
        0.17: [65, 20, 15, 10],
        0.25: [100, 35, 25, 15],
        0.33: [135, 45, 35, 25],
        0.5: [200, 65, 50, 35],
        1: [400, 135, 100, 65],
        2: [600, 200, 150, 100],
        3: [800, 265, 200, 135],
        4: [1200, 400, 300, 200],
        5: [1600, 535, 400, 265],
        6: [2400, 800, 600, 400],
        7: [3200, 1070, 800, 535],
        8: [4800, 1600, 1200, 800],
        9: [6400, 2130, 1600, 1070],
        10: [9600, 3200, 2400, 1600],
        11: [12800, 4270, 3200, 2130],
        12: [19200, 6400, 4800, 3200],
        13: [25600, 8530, 6400, 4270],
        14: [38400, 12800, 9600, 6400],
        15: [51200, 17100, 12800, 8530],
        16: [76800, 25600, 19200, 12800],
        17: [102400, 34100, 25600, 17100],
        18: [153600, 51200, 38400, 25600],
        19: [204800, 68300, 51200, 34100],
        20: [307200, 102000, 76800, 51200],
        21: [409600, 137000, 102400, 68300],
        22: [614400, 205000, 153600, 102400],
        23: [819200, 273000, 204800, 137000],
        24: [1228800, 410000, 307200, 204800],
        25: [1638400, 546000, 409600, 273000]
    },

    "starting_wealth": RangedDictionary({
        ('sorcerer', 'wizard', 'summoner', 'druid'
         ): ['2d6', '10'],

        ('fighter', 'paladin', 'cavalier', 'antipaladin', 'slayer',
         'warpriest', 'samurai', 'ranger', 'swashbuckler'
         ): ['5d6', '10'],

        ('brawler', 'oracle', 'skald', 'investigator', 'witch', 'shaman',
         'alchemist', 'barbarian', 'bloodrager', 'bard'
         ): ['3d6', '10'],

        ('cleric', 'inquisitor', 'rogue', 'hunter', 'ninja', 'magus'
         ): ['4d6', '10'],

        ('monk', 'arcanist'
         ): ['1d6', '10']
    }),

    "bab": RangedDictionary({
        ('sorcerer', 'arcanist', 'wizard', 'witch'): [
            [0],
            [1],
            [1],
            [2],
            [2],
            [3],
            [3],
            [4],
            [4],
            [5],
            [5],
            [6, 1],
            [6, 1],
            [7, 2],
            [7, 2],
            [8, 3],
            [8, 3],
            [9, 4],
            [9, 4],
            [10, 5]
        ],
        ('inquisitor', 'warpriest', 'investigator', 'skald', 'bard', 'shaman',
         'hunter', 'ninja', 'monk', 'summoner', 'rogue', 'druid', 'oracle',
         'cleric', 'magus', 'alchemist'): [
            [0],
            [1],
            [2],
            [3],
            [3],
            [4],
            [5],
            [6, 1],
            [6, 1],
            [7, 2],
            [8, 3],
            [9, 4],
            [9, 4],
            [10, 5],
            [11, 6, 1],
            [12, 7, 2],
            [12, 7, 2],
            [13, 8, 3],
            [14, 9, 4],
            [15, 10, 5]
        ],
        ('fighter', 'barbarian', 'samurai', 'cavalier', 'ranger', 'slayer',
         'paladin', 'antipaladin', 'brawler', 'bloodrager', 'swashbuckler'
         ): [
            [1],
            [2],
            [3],
            [4],
            [5],
            [6, 1],
            [7, 2],
            [8, 3],
            [9, 4],
            [10, 5],
            [11, 6, 1],
            [12, 7, 2],
            [13, 8, 3],
            [14, 9, 4],
            [15, 10, 5],
            [16, 11, 6, 1],
            [17, 12, 7, 2],
            [18, 13, 8, 3],
            [19, 14, 9, 4],
            [20, 15, 10, 5]
        ]
    }),
    "save_names": [
        "fort",
        "ref",
        "will"
    ],

    "saving_throws": RangedDictionary({
        ('magus', 'druid', 'warpriest', 'skald', 'inquisitor', 'antipaladin',
         'cleric', 'paladin'): [
            [2, 0, 2],
            [3, 0, 3],
            [3, 1, 3],
            [4, 1, 4],
            [4, 1, 4],
            [5, 2, 5],
            [5, 2, 5],
            [6, 2, 6],
            [6, 3, 6],
            [7, 3, 7],
            [7, 3, 7],
            [8, 4, 8],
            [8, 4, 8],
            [9, 4, 9],
            [9, 5, 9],
            [10, 5, 10],
            [10, 5, 10],
            [11, 6, 11],
            [11, 6, 11],
            [12, 6, 12]
        ],
        ('swashbuckler', 'rogue', 'ninja'): [
            [0, 2, 0],
            [0, 3, 0],
            [1, 3, 1],
            [1, 4, 1],
            [1, 4, 1],
            [2, 5, 2],
            [2, 5, 2],
            [2, 6, 2],
            [3, 6, 3],
            [3, 7, 3],
            [3, 7, 3],
            [4, 8, 4],
            [4, 8, 4],
            [4, 9, 4],
            [5, 9, 5],
            [5, 10, 5],
            [5, 10, 5],
            [6, 11, 6],
            [6, 11, 6],
            [6, 12, 6]
        ],
        ('monk', 'monk'): [
            [2, 2, 2],
            [3, 3, 3],
            [3, 3, 3],
            [4, 4, 4],
            [4, 4, 4],
            [5, 5, 5],
            [5, 5, 5],
            [6, 6, 6],
            [6, 6, 6],
            [7, 7, 7],
            [7, 7, 7],
            [8, 8, 8],
            [8, 8, 8],
            [9, 9, 9],
            [9, 9, 9],
            [10, 10, 10],
            [10, 10, 10],
            [11, 11, 11],
            [11, 11, 11],
            [12, 12, 12]
        ],
        ('bloodrager', 'barbarian', 'fighter', 'cavalier', 'samurai'): [
            [2, 0, 0],
            [3, 0, 0],
            [3, 1, 1],
            [4, 1, 1],
            [4, 1, 1],
            [5, 2, 2],
            [5, 2, 2],
            [6, 2, 2],
            [6, 3, 3],
            [7, 3, 3],
            [7, 3, 3],
            [8, 4, 4],
            [8, 4, 4],
            [9, 4, 4],
            [9, 5, 5],
            [10, 5, 5],
            [10, 5, 5],
            [11, 6, 6],
            [11, 6, 6],
            [12, 6, 6]
        ],
        ('bard', 'investigator'): [
            [0, 2, 2],
            [0, 3, 3],
            [1, 3, 3],
            [1, 4, 4],
            [1, 4, 4],
            [2, 5, 5],
            [2, 5, 5],
            [2, 6, 6],
            [3, 6, 6],
            [3, 7, 7],
            [3, 7, 7],
            [4, 8, 8],
            [4, 8, 8],
            [4, 9, 9],
            [5, 9, 9],
            [5, 10, 10],
            [5, 10, 10],
            [6, 11, 11],
            [6, 11, 11],
            [6, 12, 12]
        ],
        ('alchemist', 'hunter', 'brawler', 'ranger', 'slayer', 'gunslinger'): [
            [2, 2, 0],
            [3, 3, 0],
            [3, 3, 1],
            [4, 4, 1],
            [4, 4, 1],
            [5, 5, 2],
            [5, 5, 2],
            [6, 6, 2],
            [6, 6, 3],
            [7, 7, 3],
            [7, 7, 3],
            [8, 8, 4],
            [8, 8, 4],
            [9, 9, 4],
            [9, 9, 5],
            [10, 10, 5],
            [10, 10, 5],
            [11, 11, 6],
            [11, 11, 6],
            [12, 12, 6]
        ],
        ('arcanist', 'shaman', 'sorcerer', 'witch', 'wizard', 'summoner',
         'oracle'): [
            [0, 0, 2],
            [0, 0, 3],
            [1, 1, 3],
            [1, 1, 4],
            [1, 1, 4],
            [2, 2, 5],
            [2, 2, 5],
            [2, 2, 6],
            [3, 3, 6],
            [3, 3, 7],
            [3, 3, 7],
            [4, 4, 8],
            [4, 4, 8],
            [4, 4, 9],
            [5, 5, 9],
            [5, 5, 10],
            [5, 5, 10],
            [6, 6, 11],
            [6, 6, 11],
            [6, 6, 12]
        ]
    }),

    "att_names": [
        'strenght', 'dexterity', 'constitution',
        'intelligence', 'wisdom', 'charisma'
    ],

    # playable classes
    "classes": [
        "barbarian", "cleric", "fighter", "monk", "paladin", "ranger",
        "rogue", "wizard"],
    # will be playable after implementation
    "__classes__possible": [
        "alchemist", "antipaladin", "arcanist", "barbarian", "bard",
        "bloodrager", "brawler", "cavalier", "cleric", "druid", "fighter",
        "hunter", "inquisitor", "investigator", "magus", "monk", "ninja",
        "oracle", "paladin", "ranger", "rogue", "samurai", "shaman", "skald",
        "slayer", "sorcerer", "summoner", "swashbuckler", "warpriest",
        "witch", "wizard"],

    "alignments": RangedDictionary({
        ("alchemist", "arcanist", "bard",
         "bloodrager", "brawler", "cavalier", "cleric", "fighter",
         "gunslinger", "inquisitor", "investigator", "magus",
         "ninja", "oracle", "ranger", "rogue",
         "samurai", "shaman", "skald", "slayer", "sorcerer", "summoner",
         "swashbuckler", "warpriest", "witch", "wizard"): [
            "Lawful Good", "Neutral Good", "Chaotic Good",
            "Lawful Neutral", "Neutral", "Chaotic Neutral",
            "Lawful Evil", "Neutral Evil", "Chaotic Evil"],

        ("druid", "hunter"): [
            "Neutral Good",
            "Lawful Neutral", "Neutral", "Chaotic Neutral",
            "Neutral Evil"],

        ("antipaladin", "antipaladin"): ["Chaotic Evil"],

        ("paladin", "paladin"): ["Lawful Good"],

        ("monk", "monk"): ["Lawful Good", "Lawful Neutral", "Lawful Evil"],

        ("barbarian", "barbarian"): [
            "Neutral Good", "Chaotic Good",
            "Neutral", "Chaotic Neutral",
            "Neutral Evil", "Chaotic Evil"]
    }),
    "age_mod": {
        'mid': {
            'str': -1, 'dex': -1, 'con': -1,
            'int': +1, 'wis': +1, 'cha': +1
        },
        'old': {
            'str': -2, 'dex': -2, 'con': -2,
            'int': +1, 'wis': +1, 'cha': +1
        },
        'ven': {
            'str': -3, 'dex': -3, 'con': -3,
            'int': +1, 'wis': +1, 'cha': +1
        }
    },
    "hw_dict_bysize": {
        "fine": {},
        "Diminutive": {},
        "Tiny": {},
        "Small": {},
        "Medium": {},
        "Large (tall)": {},
        "Large (long)": {},
        "Huge (tall)": {},
        "Huge (long)": {},
        "Gargantuan (tall)": {},
        "Gargantuan (long)": {},
        "Colossal (tall)": {},
        "Colossal (long)": {}
    },
    "hw_dict": {
        #                      n d x   *y
        #        Base    Base  Modi-   Weight
        #        Height Weight fier    Modifier
        "human": {
            "size": "medium",
            "male": ["4'10", 120, (2, 10), 5],
            "female": ["4'5", 85, (2, 10), 4.5]},
        "dwarf": {
            "size": "medium",
            "male": ["3'9", 150, (2, 4), 7],
            "female": ["3'7", 120, (2, 4), 7]},
        "elf": {
            "size": "medium",
            "male": ["4'6", 85, (2, 6), 3.5],
            "female": ["4'6", 80, (2, 6), 3.5]},
        "gnome": {
            "size": "medium",
            "male": ["3'0", 45, (2, 4), 3],
            "female": ["2'10", 40, (2, 4), 3]},
        "half-elf": {
            "size": "medium",
            "male": ["4'7", 100, (2, 8), 4],
            "female": ["4'7", 80, (2, 6), 4]},
        "half-orc": {
            "size": "medium",
            "male": ["4'10", 150, (2, 12), 5],
            "female": ["4'5", 110, (2, 12), 5]},
        "halfling": {
            "size": "medium",
            "male": ["2'8", 40, (2, 4), 3],
            "female": ["2'6", 35, (2, 4), 3]},
        "aasimar": {
            "size": "medium",
            "male": ["5'2", 110, (2, 8), 5],
            "female": ["5'0", 90, (2, 8), 5]},
        "catfolk": {
            "size": "medium",
            "male": ["4'10", 120, (2, 8), 5],
            "female": ["4'5", 85, (2, 8), 5]},
        "dhampir": {
            "size": "medium",
            "male": ["4'10", 120, (2, 10), 5],
            "female": ["4'5", 85, (2, 10), 5]},
        "drow": {
            "size": "medium",
            "male": ["5'4", 90, (2, 6), 3],
            "female": ["5'4", 100, (2, 8), 3]},
        "fetchling": {
            "size": "medium",
            "male": ["5'4", 90, (2, 6), 3],
            "female": ["5'2", 80, (2, 6), 3]},
        "goblin": {
            "size": "medium",
            "male": ["2'8", 30, (2, 4), 1],
            "female": ["2'6", 25, (2, 4), 1]},
        "hobgoblin": {
            "size": "medium",
            "male": ["4'2", 165, (2, 8), 5],
            "female": ["4'0", 145, (2, 8), 5]},
        "ifrit": {
            "size": "medium",
            "male": ["5'2", 110, (2, 8), 5],
            "female": ["5'0", 90, (2, 8), 5]},
        "kobold": {
            "size": "medium",
            "male": ["2'6", 25, (2, 4), 1],
            "female": ["2'4", 20, (2, 4), 1]},
        "orc": {
            "size": "medium",
            "male": ["5'1", 160, (2, 12), 7],
            "female": ["4'9", 120, (2, 12), 7]},
        "oread": {
            "size": "medium",
            "male": ["4'0", 150, (2, 6), 7],
            "female": ["3'9", 120, (2, 6), 7]},
        "ratfolk": {
            "size": "medium",
            "male": ["3'7", 65, (2, 4), 3],
            "female": ["3'4", 50, (2, 4), 3]},
        "sylph": {
            "size": "medium",
            "male": ["5'2", 110, (2, 8), 5],
            "female": ["5'0", 90, (2, 8), 5]},
        "tengu": {
            "size": "medium",
            "male": ["4'0", 65, (2, 6), 3],
            "female": ["3'10", 55, (2, 6), 3]},
        "tiefling": {
            "size": "medium",
            "male": ["4'10", 120, (2, 10), 5],
            "female": ["4'5", 85, (2, 10), 5]},
        "undine": {
            "size": "medium",
            "male": ["4'10", 120, (2, 10), 5],
            "female": ["4'5", 85, (2, 10), 5]},
        "changeling": {
            "size": "medium",
            "female": ["5'2", 85, (2, 4), 5]},
        "duergar": {
            "size": "medium",
            "male": ["3'9", 150, (2, 4), 7],
            "female": ["3'7", 120, (2, 4), 7]},
        "gillman": {
            "size": "medium",
            "male": ["4'10", 120, (2, 10), 5],
            "female": ["4'5", 85, (2, 10), 5]},
        "grippli": {
            "size": "medium",
            "male": ["1'7", 25, (2, 4), 1],
            "female": ["1'5", 20, (2, 4), 1]},
        "kitsune": {
            "size": "medium",
            "male": ["4'10", 100, (2, 8), 5],
            "female": ["4'5", 85, (2, 8), 5]},
        "merfolk": {
            "size": "medium",
            "male": ["5'10", 145, (2, 10), 5],
            "female": ["5'8", 135, (2, 10), 5]},
        "nagaji": {
            "size": "medium",
            "male": ["5'9", 180, (2, 10), 7],
            "female": ["5'6", 160, (2, 10), 7]},
        "samsaran": {
            "size": "medium",
            "male": ["5'4", 110, (2, 8), 5],
            "female": ["5'6", 110, (2, 8), 5]},
        "strix": {
            "size": "medium",
            "male": ["5'4", 125, (2, 8), 5],
            "female": ["5'2", 115, (2, 8), 5]},
        "suli": {
            "size": "medium",
            "male": ["4'10", 120, (2, 10), 5],
            "female": ["4'5", 85, (2, 10), 5]},
        "svirfneblin": {
            "size": "medium",
            "male": ["3'0", 35, (2, 4), 1],
            "female": ["2'10", 30, (2, 4), 1]},
        "vanara": {
            "size": "medium",
            "male": ["4'8", 105, (2, 8), 5],
            "female": ["4'2", 90, (2, 8), 5]},
        "vishkanya": {
            "size": "medium",
            "male": ["5'3", 85, (2, 8), 5],
            "female": ["5'1", 75, (2, 8), 5]},
        "wayang": {
            "size": "medium",
            "male": ["3'0", 35, (2, 4), 1],
            "female": ["2'10", 30, (2, 4), 1]}
    },

    "speed": {
        'human': {"land": {"speed": "30"}},
        'dwarf': {"land": {"speed": "20", "ability": "slow and steady"}},
        'elf': {"land": {"speed": "30"}},
        'gnome': {"land": {"speed": "20"}},
        'half-elf': {"land": {"speed": "30"}},
        'half-orc': {"land": {"speed": "30"}},
        'halfling': {"land": {"speed": "20"}}
    },

    "size_modifier": {
        "colossal": -8,
        "gargantuan": -4,
        "huge": -2,
        "large": -1,
        "medium": 0,
        "small": 1,
        "tiny": 2,
        "diminutive": 4,
        "fine": 8
    },

    "hit_dice": RangedDictionary({
        ('barbarian', 'barbarian'): 12,

        ('cavalier', 'ranger', 'slayer', 'paladin', 'fighter', 'antipaladin',
         'bloodrager', 'samurai', 'swashbuckler', 'brawler'): 10,

        ('ninja', 'cleric', 'inquisitor', 'skald', 'oracle', 'rogue',
         'alchemist', 'warpriest', 'investigator', 'hunter', 'druid', 'monk',
         'magus', 'bard', 'shaman', 'summoner'): 8,

        ('arcanist', 'sorcerer', 'wizard', 'witch'): 6
    }),

    "skills": {
        'acrobatics': {
            'armor_check': True,
            'untrained': True,
            'ability': 'dex'},
        'appraise': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'bluff': {
            'armor_check': False,
            'untrained': True,
            'ability': 'cha'},
        'climb': {
            'armor_check': True,
            'untrained': True,
            'ability': 'str'},
        'craft (alchemy)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (armor)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (baskets)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (books)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (bows)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (calligraphy)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (carpentry)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (cloth)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (clothing)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (glass)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (jewelry)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (leather)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (locks)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (paintings)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (pottery)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (sculptures)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (ships)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (shoes)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (stonemasonry)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (traps)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'craft (weapons)': {
            'armor_check': False,
            'untrained': True,
            'ability': 'int'},
        'diplomacy': {
            'armor_check': False,
            'untrained': True,
            'ability': 'cha'},
        'disable device': {
            'armor_check': True,
            'untrained': False,
            'ability': 'dex'},
        'disguise': {
            'armor_check': False,
            'untrained': True,
            'ability': 'cha'},
        'escape artist': {
            'armor_check': True,
            'untrained': True,
            'ability': 'dex'},
        'fly': {
            'armor_check': True,
            'untrained': True,
            'ability': 'dex'},
        'handle animal': {
            'armor_check': False,
            'untrained': False,
            'ability': 'cha'},
        'heal': {
            'armor_check': False,
            'untrained': True,
            'ability': 'wis'},
        'intimidate': {
            'armor_check': False,
            'untrained': True,
            'ability': 'cha'},
        'knowledge(arcana)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(dungeoneering)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(engineering)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(geography)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(history)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(local)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(nature)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(nobility)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(planes)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'knowledge(religion)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'linguistics': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'perception': {
            'armor_check': False,
            'untrained': True,
            'ability': 'wis'},
        'perform': {
            'armor_check': False,
            'untrained': True,
            'ability': 'cha'},
        'profession (architect)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (baker)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (barrister)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (brewer)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (butcher)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (clerk)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (cook)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (courtesan)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (driver)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (engineer)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (farmer)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (fisherman)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (gambler)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (gardener)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (herbalist)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (innkeeper)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (librarian)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (merchant)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (midwife)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (miller)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (miner)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (porter)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (sailor)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (scribe)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (shepherd)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (soldier)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (stable master)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (tanner)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (trapper)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'profession (woodcutter)': {
            'armor_check': False,
            'untrained': False,
            'ability': 'wis'},
        'ride': {
            'armor_check': True,
            'untrained': True,
            'ability': 'dex'},
        'sense motive': {
            'armor_check': False,
            'untrained': True,
            'ability': 'wis'},
        'sleight of hand': {
            'armor_check': True,
            'untrained': False,
            'ability': 'dex'},
        'spellcraft': {
            'armor_check': False,
            'untrained': False,
            'ability': 'int'},
        'stealth': {
            'armor_check': True,
            'untrained': True,
            'ability': 'dex'},
        'survival': {
            'armor_check': False,
            'untrained': True,
            'ability': 'wis'},
        'swim': {
            'armor_check': True,
            'untrained': True,
            'ability': 'str'},
        'use magic device': {
            'armor_check': False,
            'untrained': False,
            'ability': 'cha'}
    },


    "skills_per_class": RangedDictionary({
        ('barbarian', 'druid', 'oracle', 'cavalier', 'monk',
         'alchemist', 'bloodrager', 'brawler', 'shaman', 'skald',
         'swashbuckler', 'samurai'): 4,

        ('inquisitor', 'bard', 'ranger', 'slayer', 'hunter', 'investigator'
         ): 6,

        ('antipaladin', 'arcanist', 'witch', 'cleric', 'fighter',
         'sorcerer', 'wizard', 'paladin', 'magus', 'summoner', 'warpriest'): 2,

        ('rogue', 'ninja'): 8
    }),

    "class_skills": RangedDictionary({
        ('linguistics', 'linguistics'): [
            'arcanist', 'bard', 'cleric', 'investigator', 'ninja', 'rogue',
            'skald', 'summoner', 'wizard'],

        ('survival', 'survival'): [
            'alchemist', 'barbarian', 'bloodrager', 'druid', 'fighter',
            'gunslinger', 'hunter', 'inquisitor', 'ranger', 'shaman',
            'slayer', 'warpriest'],

        ('knowledge (nature)', 'knowledge (nature)'): [
            'alchemist', 'arcanist', 'barbarian', 'bard', 'druid', 'hunter',
            'inquisitor', 'investigator', 'ranger', 'shaman', 'skald',
            'summoner', 'witch', 'wizard'],

        ('escape artist', 'escape artist'): [
            'bard', 'brawler', 'investigator', 'monk', 'ninja', 'rogue',
            'skald', 'swashbuckler'],

        ('disguise', 'disguise'): [
            'antipaladin', 'bard', 'inquisitor', 'investigator', 'ninja',
            'rogue', 'slayer'],

        ('sense motive', 'sense motive'): [
            'antipaladin', 'bard', 'brawler', 'cavalier', 'cleric',
            'inquisitor', 'investigator', 'monk', 'ninja', 'oracle',
            'paladin', 'rogue', 'samurai', 'skald', 'slayer', 'swashbuckler',
            'warpriest'],

        ('climb', 'climb'): [
            'barbarian', 'bard', 'bloodrager', 'brawler', 'cavalier', 'druid',
            'fighter', 'gunslinger', 'hunter', 'inquisitor', 'investigator',
            'magus', 'monk', 'ninja', 'ranger', 'rogue', 'samurai', 'skald',
            'slayer', 'swashbuckler', 'warpriest'],

        ('knowledge (history)', 'knowledge (history)'): [
            'arcanist', 'bard', 'cleric', 'investigator', 'monk', 'oracle',
            'skald', 'summoner', 'witch', 'wizard'],

        ('knowledge (arcana)', 'knowledge (arcana)'): [
            'alchemist', 'arcanist', 'bard', 'bloodrager', 'cleric',
            'inquisitor', 'investigator', 'magus', 'skald', 'sorcerer',
            'summoner', 'witch', 'wizard'],

        ('acrobatics', 'acrobatics'): [
            'barbarian', 'bard', 'bloodrager', 'brawler', 'gunslinger',
            'investigator', 'monk', 'ninja', 'rogue', 'skald', 'slayer',
            'swashbuckler'],

        ('swim', 'swim'): [
            'barbarian', 'bloodrager', 'brawler', 'cavalier', 'druid',
            'fighter', 'gunslinger', 'hunter', 'inquisitor', 'magus', 'monk',
            'ninja', 'ranger', 'rogue', 'samurai', 'skald', 'slayer',
            'swashbuckler', 'warpriest'],

        ('knowledge (religion)', 'knowledge (religion)'): [
            'antipaladin', 'arcanist', 'bard', 'cleric', 'inquisitor',
            'investigator', 'monk', 'oracle', 'paladin', 'shaman', 'skald',
            'summoner', 'warpriest', 'wizard'],

        ('sleight of hand', 'sleight of hand'): [
            'alchemist', 'bard', 'gunslinger', 'investigator', 'ninja',
            'rogue', 'swashbuckler'],

        ('craft (clothing)', 'craft (armor)', 'craft (jewelry)',
         'craft (paintings)', 'craft (leather)', 'craft (baskets)',
         'craft (traps)', 'craft (weapons)', 'craft (locks)',
         'craft (bows)', 'craft (stonemasonry)', 'craft (books)',
         'craft (cloth)', 'craft (carpentry)', 'craft (shoes)',
         'craft (sculptures)', 'craft (calligraphy)', 'craft (ships)',
         'craft (alchemy)', 'craft (pottery)', 'craft (glass)'): [
            'alchemist', 'antipaladin', 'arcanist', 'barbarian', 'bard',
            'bloodrager', 'brawler', 'cavalier', 'cleric', 'druid', 'fighter',
            'gunslinger', 'hunter', 'inquisitor', 'investigator', 'magus',
            'monk', 'ninja', 'oracle', 'paladin', 'ranger', 'rogue',
            'samurai', 'shaman', 'skald', 'slayer', 'sorcerer', 'summoner',
            'swashbuckler', 'warpriest', 'witch', 'wizard'],

        ('perform (sing)', 'perform (string)', 'perform (oratory)',
         'perform (percussion)', 'perform (wind)'): [
            'bard', 'skald'],

        ('disable device', 'disable device'): [
            'alchemist', 'investigator', 'ninja', 'rogue'],

        ('profession (clerk)', 'profession (cook)', 'profession (driver)',
         'profession (trapper)', 'profession (merchant)',
         'profession (porter)', 'profession (librarian)',
         'profession (gambler)', 'profession (scribe)',
         'profession (architect)', 'profession (courtesan)',
         'profession (miner)', 'profession (gardener)',
         'profession (soldier)', 'profession (brewer)',
         'profession (barrister)', 'profession (shepherd)',
         'profession (farmer)', 'profession (innkeeper)',
         'profession (butcher)', 'profession (baker)',
         'profession (engineer)', 'profession (sailor)',
         'profession (midwife)', 'profession (woodcutter)',
         'profession (miller)', 'profession (tanner)',
         'profession (herbalist)', 'profession (stable master)',
         'profession (fisherman)'): [
            'alchemist', 'antipaladin', 'arcanist', 'bard', 'brawler',
            'cavalier', 'cleric', 'druid', 'fighter', 'gunslinger',
            'inquisitor', 'investigator', 'magus', 'monk', 'ninja', 'oracle',
            'paladin', 'ranger', 'rogue', 'samurai', 'shaman', 'skald',
            'slayer', 'sorcerer', 'summoner', 'swashbuckler', 'warpriest',
            'witch', 'wizard'],

        ('bluff', 'bluff'): [
            'antipaladin', 'bard', 'cavalier', 'gunslinger', 'inquisitor',
            'investigator', 'ninja', 'rogue', 'samurai', 'skald', 'slayer',
            'sorcerer', 'swashbuckler'],

        ('knowledge (planes)', 'knowledge (planes)'): [
            'arcanist', 'bard', 'cleric', 'inquisitor', 'investigator',
            'magus', 'oracle', 'shaman', 'skald', 'summoner', 'witch',
            'wizard'],

        ('ride', 'ride'): [
            'antipaladin', 'barbarian', 'bloodrager', 'brawler', 'cavalier',
            'druid', 'fighter', 'gunslinger', 'hunter', 'inquisitor', 'magus',
             'monk', 'paladin', 'ranger', 'samurai', 'shaman', 'skald',
             'slayer', 'summoner', 'swashbuckler', 'warpriest'],

        ('knowledge (nobility)', 'knowledge (nobility)'): [
            'arcanist', 'bard', 'cleric', 'investigator', 'ninja', 'paladin',
            'skald', 'summoner', 'swashbuckler', 'wizard'],

        ('diplomacy', 'diplomacy'): [
            'bard', 'cavalier', 'cleric', 'inquisitor', 'investigator',
            'ninja', 'oracle', 'paladin', 'rogue', 'samurai', 'shaman',
            'skald', 'swashbuckler', 'warpriest'],

        ('knowledge (geography)', 'knowledge (geography)'): [
            'arcanist', 'bard', 'druid', 'hunter', 'investigator', 'ranger',
            'skald', 'slayer', 'summoner', 'wizard'],

        ('stealth', 'stealth'): [
            'antipaladin', 'bard', 'hunter', 'inquisitor', 'investigator',
            'monk', 'ninja', 'ranger', 'rogue', 'slayer'],

        ('spellcraft', 'spellcraft'): [
            'alchemist', 'antipaladin', 'arcanist', 'bard', 'bloodrager',
            'cleric', 'druid', 'hunter', 'inquisitor', 'investigator',
            'magus', 'oracle', 'paladin', 'ranger', 'shaman', 'skald',
            'sorcerer', 'summoner', 'warpriest', 'witch', 'wizard'],

        ('handle animal', 'handle animal'): [
            'antipaladin', 'barbarian', 'bloodrager', 'brawler', 'cavalier',
            'druid', 'fighter', 'gunslinger', 'hunter', 'paladin', 'ranger',
            'samurai', 'shaman', 'skald', 'summoner', 'warpriest'],

        ('perception', 'perception'): [
            'alchemist', 'barbarian', 'bard', 'bloodrager', 'brawler',
            'druid', 'gunslinger', 'hunter', 'inquisitor', 'investigator',
            'monk', 'ninja', 'ranger', 'rogue', 'skald', 'slayer',
            'swashbuckler'],

        ('perform', 'perform'): [
            'investigator', 'monk', 'ninja', 'rogue', 'swashbuckler'],

        ('appraise', 'appraise'): [
            'alchemist', 'arcanist', 'bard', 'cleric', 'investigator',
            'ninja', 'rogue', 'skald', 'sorcerer', 'wizard'],

        ('intimidate', 'intimidate'): [
            'antipaladin', 'barbarian', 'bard', 'bloodrager', 'brawler',
            'cavalier', 'fighter', 'gunslinger', 'hunter', 'inquisitor',
            'investigator', 'magus', 'monk', 'ninja', 'ranger', 'rogue',
            'samurai', 'skald', 'slayer', 'sorcerer', 'swashbuckler',
            'warpriest', 'witch'],

        ('knowledge (local)', 'knowledge (local)'): [
            'arcanist', 'bard', 'brawler', 'gunslinger', 'investigator',
            'ninja', 'rogue', 'skald', 'slayer', 'summoner', 'swashbuckler',
            'wizard'],

        ('perform (keyboard)', 'perform (dance)', 'perform (act)',
         'perform (comedy)'): [
            'bard'],

        ('use magic device', 'use magic device'): [
            'alchemist', 'arcanist', 'bard', 'investigator', 'magus', 'ninja',
            'rogue', 'skald', 'sorcerer', 'summoner', 'witch'],

        ('knowledge (dungeoneering)', 'knowledge (dungeoneering)'): [
            'arcanist', 'bard', 'brawler', 'fighter', 'hunter', 'inquisitor',
            'investigator', 'magus', 'ranger', 'rogue', 'skald', 'slayer',
            'summoner', 'wizard'],

        ('heal', 'heal'): [
            'alchemist', 'cleric', 'druid', 'gunslinger', 'hunter',
            'inquisitor', 'investigator', 'oracle', 'paladin', 'ranger',
            'shaman', 'slayer', 'warpriest', 'witch'],

        ('fly', 'fly'): [
            'alchemist', 'arcanist', 'druid', 'magus', 'shaman', 'sorcerer',
            'summoner', 'witch', 'wizard'],

        ('knowledge (engineering)', 'knowledge (engineering)'): [
            'arcanist', 'bard', 'fighter', 'gunslinger', 'investigator',
            'skald', 'summoner', 'warpriest', 'wizard']
    }),

    "racial_skill_mods": {
        "dwarf": [("appraise", 2), ("perception", 2)],
        "elf": [("perception", 2)],
        "gnome": [("perception", 2)],
        "half-elf": [("perception", 2)],
        "halfling": [("perception", 2)],
        "half-orc": [("intimidate", 2)],
        "human": [],

        "aasimar": [("diplomacy", 2), ("perception", 2)],
        "catfolk": [("perception", 2), ("stealth", 2), ("survival", 2)],
        "dhampir": [("bluff", 2), ("perception", 2)],
        "drow": [("perception", 2)],
        "fetchling": [("knowledge (planes)", 2), ("stealth", 2)],
        "goblin": [("ride", 4), ("stealth", 4)],
        "hobgoblin": [("stealth", 4)],
        "ifrit": [],
        "kobold": [("craft (traps)", 2), ("perception", 2),
                   ("profession (miner)", 2)],
        "orc": [],
        "oread": [],
        "ratfolk": [("craft (alchemy)", 2), ("perception", 2),
                    ("use magic device", 2)],
        "sylph": [],
        "tengu": [("perception", 4), ("stealth", 2),
                  ("linguistics", 4)],
        "tiefling": [("bluff", 2), ("stealth", 2)],
        "undine": [],

        "changeling": [],
        "duergar": [],
        "gillman": [],
        "grippli": [("stealth", 4)],
        "kitsune": [("acrobatics", 4)],
        "merfolk": [],
        "nagaji": [("handle animal", 2), ("perception", 2)],
        "samsaran": [],
        "strix": [("perception", 2), ("stealth", 2)],
        "suli": [("diplomacy", 2), ("sense motive", 2)],
        "svirfneblin": [("stealth", 2), ("craft (alchemy)", 2),
                        ("perception", 2)],
        "vanara": [],
        "vishkanya": [],
        "wayang": []
    }
}

# age_groups
intuitive = (
    "barbarian", "bloodrager", "ninja", "oracle", "rogue", "sorcerer")

self_taught = (
    "antipaladin", "arcanist", "bard", "cavalier", "fighter", "gunslinger",
    "investigator", "paladin", "ranger", "samurai", "shaman", "skald",
    "slayer", "summoner", "witch")

trained = (
    "alchemist", "brawler", "cleric", "druid", "hunter", "inquisitor",
    "magus", "monk", "warpriest", "wizard")

data["age_dict"] = {
    'human': {
        'ini': 15,
        'mid': 35,
        'old': 53,
        'ven': 70,
        'max': (2, 20),
        'var': RangedDictionary({
            intuitive: (1, 4),
            self_taught: (1, 6),
            trained: (2, 6)})},
    'dwarf': {
        'ini': 40,
        'mid': 125,
        'old': 188,
        'ven': 250,
        'max': (2, 100),
        'var': RangedDictionary({
            intuitive: (3, 6),
            self_taught: (5, 6),
            trained: (7, 6)})},
    'elf': {
        'ini': 110,
        'mid': 175,
        'old': 263,
        'ven': 350,
        'max': (4, 100),
        'var': RangedDictionary({
            intuitive: (4, 6),
            self_taught: (6, 6),
            trained: (10, 6)})},
    'gnome': {
        'ini': 40,
        'mid': 100,
        'old': 150,
        'ven': 200,
        'max': (3, 100),
        'var': RangedDictionary({
            intuitive: (4, 6),
            self_taught: (6, 6),
            trained: (9, 6)})},
    'half-elf': {
        'ini': 20,
        'mid': 62,
        'old': 93,
        'ven': 125,
        'max': (3, 20),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (3, 6)})},
    'half-orc': {
        'ini': 14,
        'mid': 30,
        'old': 45,
        'ven': 60,
        'max': (2, 10),
        'var': RangedDictionary({
            intuitive: (1, 4),
            self_taught: (1, 6),
            trained: (2, 6)})},
    'halfling': {
        'ini': 20,
        'mid': 50,
        'old': 75,
        'ven': 100,
        'max': (5, 20),
        'var': RangedDictionary({
            intuitive: (2, 4),
            self_taught: (3, 6),
            trained: (4, 6)})},
    "aasimar": {
        "ini": 20, "mid": 35, "old": 53, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (2, 20)})},
    "catfolk": {
        "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 20)})},
    "dhampir": {
        "ini": 20, "mid": 35, "old": 53, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (10, 6),
            trained: (2, 20)})},
    "drow": {
        "ini": 110, "mid": 175, "old": 263, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (10, 6),
            trained: (4, 100)})},
    "fetchling": {
        "ini": 20, "mid": 62, "old": 93, "ven": 70, "max": (1, 6),
        'var': RangedDictionary({
            intuitive: (2, 6),
            self_taught: (3, 6),
            trained: (3, 20)})},
    "goblin": {
        "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (1, 20)})},
    "hobgoblin": {
        "ini": 14, "mid": 30, "old": 45, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 10)})},
    "ifrit": {
        "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (6, 100)})},
    "kobold": {
        "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (1, 20)})},
    "orc": {
        "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (1, 20)})},
    "oread": {
        "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (6, 100)})},
    "ratfolk": {
        "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (1, 20)})},
    "sylph": {
        "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (6, 100)})},
    "tengu": {
        "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 20)})},
    "tiefling": {
        "ini": 20, "mid": 35, "old": 53, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (2, 20)})},
    "undine": {
        "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (6, 100)})},
    "changeling": {
        "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 20)})},
    "duergar": {
        "ini": 40, "mid": 125, "old": 188, "ven": 70, "max": (3, 6),
        'var': RangedDictionary({
            intuitive: (5, 6),
            self_taught: (7, 6),
            trained: (2, 100)})},
    "gillman": {
        "ini": 20, "mid": 62, "old": 93, "ven": 70, "max": (1, 6),
        'var': RangedDictionary({
            intuitive: (2, 6),
            self_taught: (3, 6),
            trained: (3, 20)})},
    "grippli": {
        "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (1, 20)})},
    "kitsune": {
        "ini": 15, "mid": 32, "old": 50, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (3, 12)})},
    "merfolk": {
        "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 20)})},
    "nagaji": {
        "ini": 20, "mid": 60, "old": 90, "ven": 70, "max": (1, 6),
        'var': RangedDictionary({
            intuitive: (2, 6),
            self_taught: (3, 6),
            trained: (3, 20)})},
    "samsaran": {
        "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (8, 6),
            trained: (6, 100)})},
    "strix": {
        "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (1, 20)})},
    "suli": {
        "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 20)})},
    "svirfneblin": {
        "ini": 40, "mid": 100, "old": 150, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (6, 6),
            self_taught: (9, 6),
            trained: (3, 100)})},
    "vanara": {
        "ini": 14, "mid": 30, "old": 45, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 10)})},
    "vishkanya": {
        "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
        'var': RangedDictionary({
            intuitive: (1, 6),
            self_taught: (2, 6),
            trained: (2, 20)})},
    "wayang": {
        "ini": 40, "mid": 100, "old": 150, "ven": 70, "max": (4, 6),
        'var': RangedDictionary({
            intuitive: (5, 6),
            self_taught: (6, 6),
            trained: (1, 100)})}
}


if __name__ == '__main__':
    print(data['saving_throws']['sorcerer'])
    exit()
    from mylib.data_tree import tk_tree_view
    tk_tree_view(data['bab'])
