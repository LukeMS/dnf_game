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

rnd_armor_material = RangedDictionary({
    range(1, 96): "standard",
    range(96, 101): "special"
})

def get_equipment(string):
    pattern = ""

def calculate_hoard(total, specifics=None):
    specifics = specifics if specifics else []
    for specific in specifics:

