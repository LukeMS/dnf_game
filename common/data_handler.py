"""Helper functions to open and handle bz2 compressed json file's content."""

import os
import sys

if not os.path.isdir('combat'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from common import packer

from data import specific_weapons


STD_WEAPONS = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'weapons.bzp')
SPEC_WEAPONS = specific_weapons.SPECIFIC

STD_ARMORS = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'armors.bzp')
SPEC_ARMORS = {}


def get_all_weapons():
    """..."""
    specific_names = list(SPEC_WEAPONS.keys())

    std_db = packer.unpack_json(STD_WEAPONS)
    std_names = list(std_db.keys())
    return specific_names + std_names


def get_weapon(item):
    """..."""
    specific = None
    if item in SPEC_WEAPONS:
        specific = SPEC_WEAPONS[item]

    db = packer.unpack_json(STD_WEAPONS)

    if specific:
        base = db[specific['base_item']]
        base.update(specific)
        return base

    else:
        return db[item]

def get_all_armors():
    """..."""
    specific_names = list(SPEC_ARMORS.keys())

    std_db = packer.unpack_json(STD_ARMORS)
    std_names = list(std_db.keys())
    return specific_names + std_names


def get_armor(item):
    """..."""
    specific = None
    if item in SPEC_ARMORS:
        specific = SPEC_ARMORS[item]

    db = packer.unpack_json(STD_ARMORS)

    if specific:
        base = db[specific['base_item']]
        base.update(specific)
        return base

    else:
        return db[item]


if __name__ == '__main__':
    print(get_all_weapons())
