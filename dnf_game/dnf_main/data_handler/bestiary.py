"""..."""

import os
import random

from dnf_game.util import packer, dnf_path, SingletonMeta
from dnf_game.util.ext.queries import Query, where

PATH = dnf_path()


class Bestiary(metaclass=SingletonMeta):
    """...

    Usage:
        Bestiary().get("aasimar")
    """

    _cr_dict = None
    _db = None

    def __init__(self, optmize=False):
        """..."""

    @property
    def cr_dict(self):
        """Return cr_dict."""
        if getattr(self, "_cr_dict") is None:
            print("%s: caching cr_dict" % self.__class__.__name__)

            cr_dict = {}
            for k, v in self.db.items():
                cr = float(v.__getitem__('cr'))
                try:
                    cr_dict[cr].append(v.__getitem__('def_name'))
                except KeyError:
                    cr_dict[cr] = []
                    cr_dict[cr].append(v.__getitem__('def_name'))
            self._cr_dict = cr_dict

        return self._cr_dict

    @property
    def db(self):
        """Return db."""
        if getattr(self, "_db") is None:
            print("%s: caching db" % self.__class__.__name__)
            fname = os.path.join(dnf_path(), 'data', 'bestiary_optimized.bzp')
            self._db = packer.unpack_json(fname)
        return self._db

    def filter_empty_melee(self, creature_key):
        """..."""
        creature = self.db[creature_key]
        status = creature['melee'] != ""
        print("Creature {}'s melee: '{}', valid:{}".format(
            creature_key,
            creature['melee'],
            status
        ))
        return status

    def search(self, cond):
        """Search for all elements matching a 'where' cond.

        :param cond: the condition to check against
        :type cond: Query

        :returns: list of matching elements
        :rtype: list[Element]
        """
        elements = [element for element in self.db.values() if cond(element)]

        return elements

    def get_model(self):
        """..."""
        creature = Query()
        creatures = self.search((creature.cr != "") &
                                (creature.melee != ""))
        return random.choice(creatures)

    def get(self, creature=None):
        """..."""
        creature = (self.db.__getitem__(creature)
                    if creature
                    else self.get_model())

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

    def get_by_cr(self, cr):
        """..."""
        cr = float(cr)
        return random.choice(self.cr_dict[cr])

    def get_field(self, string):
        """..."""
        return [v[string] for v in self.db.values()]

    def get_field_with_value(self, string, value=None):
        """..."""
        return self.search((where(string) == value))


if __name__ == '__main__':
    from dnf_game.util.rnd_utils import rnd_cr_per_level
    b = Bestiary()
    b.get()
    b.get("tarrasque")
    b.search((
        (where('type') == "aberration") &
        (where('hp') < 10)
    ))
    b.search((
        (where('feats').any(["light armor proficiency"]))
    ))
    from pprint import pprint
    pprint(b.get_by_cr(rnd_cr_per_level(2)), indent=4)
