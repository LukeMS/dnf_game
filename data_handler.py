import os

import packer

from data.items import specific_weapons

STD_WEAPONS = os.path.join(os.path.dirname(__file__),
                           'data', 'items', 'weapons.bzp')
SPEC_WEAPONS = specific_weapons.SPECIFIC

def get_all_weapons():
    specific_names = list(SPEC_WEAPONS.keys())

    std_db = packer.unpack_json(STD_WEAPONS)
    std_names = list(std_db.keys())
    return specific_names + std_names

def get_weapon(item):


    specific = None
    if item in specific_weapons.SPECIFIC:
        specific = specific_weapons.SPECIFIC[item]

    db = packer.unpack_json(STD_WEAPONS)

    if specific:
        base = db[specific['base_item']]
        base.update(specific)
        return base

    else:
        return db[item]


if __name__ == '__main__':
    print(get_all_weapons())
