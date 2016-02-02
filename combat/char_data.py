import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rnd_utils import RangedDictionary
# Fort Save, Ref Save, Will Save

data = {

    # playable races
    "races": [
        'human',
        'dwarf',
        'elf',
        'gnome',
        'half-elf',
        'half-orc',
        'halfling'
    ],

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

    "starting_wealth": {
        "barbarian": ['3d6', '10'],
        "bard": ['3d6', '10'],
        "cleric": ['4d6', '10'],
        "druid": ['2d6', '10'],
        "fighter": ['5d6', '10'],
        "monk": ['1d6', '10'],
        "paladin": ['5d6', '10'],
        "ranger": ['5d6', '10'],
        "rogue": ['4d6', '10'],
        "sorcerer": ['2d6', '10'],
        "wizard": ['2d6', '10']
    },

    "bab": {
        "barbarian": [
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
            [20, 15, 10, 5]],
        "bard": [
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
            [15, 10, 5]],
        "cleric": [
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
            [15, 10, 5]],
        "druid": [
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
            [15, 10, 5]],
        "fighter": [
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
            [20, 15, 10, 5]],
        "monk": [
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
            [15, 10, 5]],
        "paladin": [
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
            [20, 15, 10, 5]],
        "ranger": [
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
            [20, 15, 10, 5]],
        "rogue": [
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
            [15, 10, 5]],
        "sorcerer": [
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
            [10, 5]],
        "wizard": [
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
            [10, 5]]
    },

    "save_names": [
        "fort",
        "ref",
        "will"
    ],

    "saving_throws": {
        "barbarian": [
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
            [12, 6, 6]],
        "bard": [
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
            [6, 12, 12]],
        "cleric": [
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
            [12, 6, 12]],
        "druid": [
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
            [12, 6, 12]],
        "fighter": [
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
            [12, 6, 6]],
        "monk": [
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
            [12, 12, 12]],
        "paladin": [
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
            [12, 6, 12]],
        "ranger": [
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
            [12, 12, 6]],
        "rogue": [
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
            [6, 12, 6]],
        "sorcerer": [
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
            [6, 6, 12]],
        "wizard": [
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
            [6, 6, 12]]
    },

    "att_names": [
        'strenght', 'dexterity', 'constitution',
        'intelligence', 'wisdom', 'charisma'
    ],

    "classes": [
        "barbarian", "bard", "cleric", "druid", "fighter", "monk",
        "paladin", "ranger", "rogue", "sorcerer", "wizard"
    ],

    "alignments": RangedDictionary({
        ("barbarian", "rogue", "sorcerer", "bard",
            "fighter", "paladin", "ranger", "cleric",
            "druid", "monk", "wizard"): [
            "Lawful Good", "Neutral Good", "Chaotic Good",
            "Lawful Neutral", "Neutral", "Chaotic Neutral",
            "Lawful Evil", "Neutral Evil", "Chaotic Evil"
        ]
    }),

    "age_dict": {
        'human': {
            'ini': 15,
            'mid': 35,
            'old': 53,
            'ven': 70,
            'max': (2, 20),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 4),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (1, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 6)})},
        'dwarf': {
            'ini': 40,
            'mid': 125,
            'old': 188,
            'ven': 250,
            'max': (2, 100),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (3, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (5, 6),
                ("cleric", "druid", "monk", "wizard"): (7, 6)})},
        'elf': {
            'ini': 110,
            'mid': 175,
            'old': 263,
            'ven': 350,
            'max': (4, 100),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (4, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (6, 6),
                ("cleric", "druid", "monk", "wizard"): (10, 6)})},
        'gnome': {
            'ini': 40,
            'mid': 100,
            'old': 150,
            'ven': 200,
            'max': (3, 100),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (4, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (6, 6),
                ("cleric", "druid", "monk", "wizard"): (9, 6)})},
        'half-elf': {
            'ini': 20,
            'mid': 62,
            'old': 93,
            'ven': 125,
            'max': (3, 20),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (3, 6)})},
        'half-orc': {
            'ini': 14,
            'mid': 30,
            'old': 45,
            'ven': 60,
            'max': (2, 10),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 4),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (1, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 6)})},
        'halfling': {
            'ini': 20,
            'mid': 50,
            'old': 75,
            'ven': 100,
            'max': (5, 20),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (2, 4),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (3, 6),
                ("cleric", "druid", "monk", "wizard"): (4, 6)})},
        "aasimar": {
            "ini": 20, "mid": 35, "old": 53, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "catfolk": {
            "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "dhampir": {
            "ini": 20, "mid": 35, "old": 53, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (10, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "drow": {
            "ini": 110, "mid": 175, "old": 263, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (10, 6),
                ("cleric", "druid", "monk", "wizard"): (4, 100)})},
        "fetchling": {
            "ini": 20, "mid": 62, "old": 93, "ven": 70, "max": (1, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (2, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (3, 6),
                ("cleric", "druid", "monk", "wizard"): (3, 20)})},
        "goblin": {
            "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 20)})},
        "hobgoblin": {
            "ini": 14, "mid": 30, "old": 45, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 10)})},
        "ifrit": {
            "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (6, 100)})},
        "kobold": {
            "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 20)})},
        "orc": {
            "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 20)})},
        "oread": {
            "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (6, 100)})},
        "ratfolk": {
            "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 20)})},
        "sylph": {
            "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (6, 100)})},
        "tengu": {
            "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "tiefling": {
            "ini": 20, "mid": 35, "old": 53, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "undine": {
            "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (6, 100)})},
        "changeling": {
            "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "duergar": {
            "ini": 40, "mid": 125, "old": 188, "ven": 70, "max": (3, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (5, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (7, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 100)})},
        "gillman": {
            "ini": 20, "mid": 62, "old": 93, "ven": 70, "max": (1, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (2, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (3, 6),
                ("cleric", "druid", "monk", "wizard"): (3, 20)})},
        "grippli": {
            "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 20)})},
        "kitsune": {
            "ini": 15, "mid": 32, "old": 50, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (3, 12)})},
        "merfolk": {
            "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "nagaji": {
            "ini": 20, "mid": 60, "old": 90, "ven": 70, "max": (1, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (2, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (3, 6),
                ("cleric", "druid", "monk", "wizard"): (3, 20)})},
        "samsaran": {
            "ini": 60, "mid": 150, "old": 200, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (8, 6),
                ("cleric", "druid", "monk", "wizard"): (6, 100)})},
        "strix": {
            "ini": 12, "mid": 20, "old": 30, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 20)})},
        "suli": {
            "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "svirfneblin": {
            "ini": 40, "mid": 100, "old": 150, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (6, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (9, 6),
                ("cleric", "druid", "monk", "wizard"): (3, 100)})},
        "vanara": {
            "ini": 14, "mid": 30, "old": 45, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 10)})},
        "vishkanya": {
            "ini": 15, "mid": 35, "old": 53, "ven": 70, "max": (1, 4),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (1, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (2, 6),
                ("cleric", "druid", "monk", "wizard"): (2, 20)})},
        "wayang": {
            "ini": 40, "mid": 100, "old": 150, "ven": 70, "max": (4, 6),
            'var': RangedDictionary({
                ("barbarian", "rogue", "sorcerer"): (5, 6),
                ("bard", "fighter", "warrior", "paladin", "ranger"): (6, 6),
                ("cleric", "druid", "monk", "wizard"): (1, 100)})}
    },

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
        "human": {
            "size": "medium",
            #                      n d x   *y
            #        Base    Base  Modi-   Weight
            #        Height Weight fier    Modifier
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

    "hit_dice": {
        "barbarian": 12,
        "bard": 8,
        "cleric": 8,
        "druid": 8,
        "fighter": 10,
        "monk": 8,
        "paladin": 10,
        "ranger": 10,
        "rogue": 8,
        "sorcerer": 6,
        "wizard": 6
    }
}


if __name__ == '__main__':
    from mylib.data_tree import tk_tree_view
    tk_tree_view(data)