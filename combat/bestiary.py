import sys
import os
import random

if not os.path.isdir('combat'):
    if os.path.isdir(os.path.join('..')):
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
        if os.path.isdir(os.path.join('.', 'data', 'bestiary')):
            _path = os.path.join('.', 'data', 'bestiary')
        else:
            _path = os.path.join('..', 'data', 'bestiary')

        fname = os.path.join(_path, 'bestiary_optimized.bzp')

        cls.db = packer.unpack_json(fname)

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
        print("Checking creature {}'s melee: '{}'".format(
            creature_key,
            creature['melee']
        ))
        return creature['melee'] != ""

    @classmethod
    def get_model(cls):
        return random.choice(list(cls.db.keys()))

    @classmethod
    def get(cls, creature=False, filter_fields=['non_empty_melee']):
        if not creature:
            if filter_fields:
                status_all_filters = False
                while not status_all_filters:
                    creature = random.choice(list(cls.db.keys()))

                    # a filter; others should be built
                    if 'non_empty_melee' in filter_fields:
                        status_empty_melee = cls.filter_empty_melee(creature)
                    else:
                        status_empty_melee = True

                    status_all_filters = status_empty_melee  # and others
            else:
                creature = random.choice(list(cls.db.keys()))
        return cls.db[creature]

    @classmethod
    def get_by_cr(cls, cr):
        if "cr_dict" not in cls.__dict__:
            cls.create_cr_dict()
            cr = float(cr)
        return random.choice(cls.cr_dict[cr])

    @classmethod
    def get_field(cls, string):
        list_ = []
        for creature in cls.db.keys():
            list_.append(cls.db[creature][string])
        return list_

    @classmethod
    def get_field_with_value(cls, string, value):
        d = {}
        [d.update({key: field[string]})
         for key, field in cls.db.items() if field[string] == value]
        return d

Bestiary()

if __name__ == '__main__':
    from pprint import pprint
    pprint(Bestiary.get_field_with_value("ac_flat-footed", "38"))
