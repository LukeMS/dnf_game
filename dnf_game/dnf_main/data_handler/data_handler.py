"""Helper functions to open and handle bz2 compressed json file's content."""

import os

from dnf_game.data import specific_weapons
from dnf_game.util import packer, dnf_path


PATH = dnf_path()

STD_WEAPONS = os.path.join(PATH, 'data', 'weapons.bzp')
SPEC_WEAPONS = specific_weapons.SPECIFIC

STD_ARMORS = os.path.join(PATH, 'data', 'armors.bzp')
SPEC_ARMORS = {}


def get_all_weapon_names():
    """..."""
    specific_names = list(SPEC_WEAPONS.keys())

    std_db = packer.unpack_json(STD_WEAPONS)
    std_names = list(std_db.keys())
    return specific_names + std_names


def get_all_weapons():
    """..."""
    std = packer.unpack_json(STD_WEAPONS)
    return {**SPEC_WEAPONS, **std}
    """
    try:
    except:
        retur
        d = SPEC_WEAPONS.copy()
        d.update(STD_WEAPONS)
        return d
    """


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


def get_all_armor_names():
    """..."""
    specific_names = list(SPEC_ARMORS.keys())

    std_db = packer.unpack_json(STD_ARMORS)
    std_names = list(std_db.keys())
    return specific_names + std_names


def get_all_armors():
    """..."""
    std = packer.unpack_json(STD_ARMORS)
    return {**SPEC_ARMORS, **std}
    """
    try:
    except:
        retur
        d = SPEC_ARMORS.copy()
        d.update(STD_ARMORS)
        return d
    """


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
    get_all_weapons()
    get_all_armors()
