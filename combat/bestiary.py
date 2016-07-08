import sys
import os
import random

if not os.path.isdir('combat'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import packer


class Bestiary:
    """
    Example:
    bestiary = Bestiary()
    pprint(bestiary.get())
    """
    @classmethod
    def __init__(cls, optmize=False):
        if os.path.isdir(os.path.join('.', 'data')):
            _path = os.path.join('.', 'data')
        else:
            _path = os.path.join('..', 'data')

        fname = os.path.join(_path, 'bestiary_optimized.bzp')

        cls.db = packer.unpack_json(fname)

        cls.create_cr_dict()

    @classmethod
    def create_cr_dict(cls):
        cls.cr_dict = {}
        for creature in sorted(list(cls.db.keys())):
            cr = float(cls.db[creature]['cr'])
            if cr not in cls.cr_dict:
                cls.cr_dict[cr] = []
            cls.cr_dict[cr].append(cls.db[creature]['def_name'])
        return cls.cr_dict

    @classmethod
    def print_cr_dict(cls):
        if "cr_dict" not in cls.__dict__:
            cls.create_cr_dict()
        for cr in sorted(list(cls.cr_dict.keys())):
            print("CR {}: {}".format(cr, cls.cr_dict[cr]))

    @classmethod
    def filter_empty_melee(cls, creature_key):
        creature = cls.db[creature_key]
        status = creature['melee'] != ""
        print("Creature {}'s melee: '{}', valid:{}".format(
            creature_key,
            creature['melee'],
            status
        ))
        return status

    @classmethod
    def get_model(cls):
        return random.choice(cls.get_filtered())

    @classmethod
    def get(cls, creature=None):
        if creature is None:
            model = cls.get_model()
        else:
            model = creature

        creature = cls.db[model]

        if creature["type"] in [
            "aberration", "vermin", "outsider", "undead", "magical beast",
            "ooze"
        ] and creature['str'] == "-":
            creature['str'] = 10

        if creature["type"] in [
            "construct"
        ] and creature['dex'] == "-":
            creature['dex'] = 10

        """
        Constructs do not have a Constitution score. Any DCs or other
        Statistics that rely on a Constitution score treat a construct as
        having a score of 10 (no bonus or penalty).
        """
        if creature["type"] in [
            "construct"
        ] and creature['con'] == "-":
            creature['con'] = 10

        """
        Undead creatures do not have a Constitution score. Undead use their
        Charisma score in place of their Constitution score when calculating
        hit points, Fortitude saves, and any special ability that relies on
        Constitution(such as when calculating a breath weapon’s DC).
        """
        if creature["type"] in [
            "undead"
        ] and creature['con'] == "-":
            creature['con'] = creature['cha']

        if creature["type"] in [
            "vermin", "undead", "plant", "construct", "ooze", "magical beast",
            "outsider"
        ] and creature['int'] == "-":
            creature['int'] = 0

        for att in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            creature[att] = int(creature[att])

        return creature

    @classmethod
    def get_by_cr(cls, cr):
        cr = float(cr)
        return random.choice(cls.cr_dict[cr])

    @classmethod
    def get_field(cls, string):
        list_ = []
        for creature in cls.db.keys():
            list_.append(cls.db[creature][string])
        return list_

    @classmethod
    def get_field_with_value(cls, string, value=None):
        d = {}
        [d.update({key: field[string]})
         for key, field in cls.db.items() if not value or
         field[string] == value]
        return d

    @classmethod
    def get_filtered(cls, filter_list=[]):
        """
        filter_list: a list of 4 element tuples containing:
            [0] the key to be searched;
            [1] the value to be searched;
            [2] the re function (match or search);
            [3] the condition: if True, the result will be valid
            if the function returns True.
        """

        import re

        matches = []

        for name, creature in cls.db.items():
            match = True
            if name == "":
                continue
            if creature['def_name'] == "":
                continue
            if creature['melee'] == "":
                continue
            for filter in filter_list:
                field, pattern, func, match = filter
                func = getattr(re, func)
                string = creature[field]
                match_result = True
                if pattern is None or string is None:
                    if match:
                        if pattern == string:
                            continue
                        else:
                            match_result = False
                            break
                    else:
                        if pattern == string:
                            match_result = False
                            break
                        else:
                            continue
                else:
                    result = func(pattern, string)
                    if result:
                        if filter[3]:
                            continue
                        else:
                            match_result = False
                            break
                    else:
                        if not filter[3]:
                            continue
                        else:
                            match_result = False
                            break
            if match_result:
                matches.append(name)

        return matches

Bestiary()

"""
Get a beast by its name:
    Bestiary.get("tarrasque")

Get a beast that pass on certain filters:
    Bestiary.get_filtered(filter_list=[
        ("type", "aberration", "match", True)
    ])
"""
"""
    print(Bestiary.get_filtered(filter_list=[
        ("feats", "light armor proficiency", "search", True)
    ]))
"""

"""
Get all "field" values of existing monsters:
    fields = set()
    bestiary_fields = Bestiary.get_field("source")
    for creature in bestiary_fields:
        for feat in creature.split(","):
            fields.add(feat.strip())

    import json
    print(json.dumps(list(fields), indent=4))
"""

if __name__ == '__main__':
    print(Bestiary.get_filtered(filter_list=[
        ("treasure", "SQ", "search", True)
    ]))
