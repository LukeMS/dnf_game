import sys
import os
import random


def bubble_sort(_items):
    """..."""
    items = list(_items)

    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j].start > items[j + 1].start:
                items[j], items[j + 1] = items[j + 1], items[j]  # Swap!
    return items


def insertion_sort(_list):
    """..."""
    for i in range(1, len(_list)):
        tmp = _list[i]
        k = i
        while k > 0 and tmp.start < _list[k - 1].start:
            _list[k] = _list[k - 1]
            k -= 1
        _list[k] = tmp
    return _list


def test_range100(obj):
    """..."""
    if isinstance(obj, RangedDictionary):
        try:
            rng_list = sorted(list(obj.keys()))
        except TypeError:
            rng_list = bubble_sort(list(obj.keys()))

        for i, rng in enumerate(rng_list):
            print(rng, obj[rng], "previous:", rng_list[i - 1])
            if i == 0:
                assert(rng.start == 1)
            elif i == len(rng_list) - 1:
                a = rng.start
                b = rng_list[i - 1].stop

                try:
                    assert(a == b)
                except AssertionError:
                    print(a, b)
                    raise(AssertionError)

                try:
                    assert(rng.stop == 101)
                except AssertionError:
                    print(rng.stop, "!=", 101)
                    raise(AssertionError)
            else:
                a = rng.start
                b = rng_list[i - 1].stop
                try:
                    assert(a == b)
                except AssertionError:
                    print(a, b)
                    raise(AssertionError)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            test_range100(v)


class RangedDictionary(dict):
    """..."""

    def __getitem__(self, key):
        """..."""
        for rng in self.keys():
            if key == rng:
                return super().__getitem__(key)
            if key in rng:
                return super().__getitem__(rng)
        return super().__getitem__(key)


def rnd_dic_rng(dic):
    """..."""
    min_v = min([key.start for key in dic.keys()])
    max_v = max([key.stop for key in dic.keys()])
    rnd = random.randint(min_v, max_v - 1)
    result = dic.__getitem__(rnd)
    # print(rnd, result)
    return result


class RandomDictionary:
    """..."""

    @classmethod
    def random(cls):
        """..."""
        return rnd_dic_rng(cls.dic)


class RoomItems(RandomDictionary):
    """Use RoomItems.random() to get a random item quantity roll."""

    dic = RangedDictionary({
        range(0, 70): 0,  # min <= x < max: 0 items
        range(70, 90): 1,  # min <= x < max: 1 item
        range(90, 100): 2  # min <= x < max: 2 items
    })


def rnd_cr_per_level(level):
    """..."""
    if not os.path.isdir('combat'):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from combat import char_roll
    dic = RangedDictionary({
        range(0, 10): 0,
        range(10, 35): 1,
        range(35, 65): 2,
        range(65, 90): 3,
        range(90, 100): 4
    })

    v = dic[random.randrange(100)] + level
    v = min(v, len(char_roll.cr) - 1)
    return char_roll.cr[v]


def set_rnd_dic(_class):
    """..."""
    dic = RangedDictionary()

    max_v = 0
    for name, template in _class.templates.items():
        rng = (100 - template['_rarity'])
        dic[range(max_v, max_v + rng)] = name
        max_v += rng

    return dic

"""
class ItemTypes(RandomDictionary):
    # Use RoomItems.random() to get a random item quantity roll.
    from sprite import Item
    dic = set_rnd_dic(Item)
"""

"""
class MonsterTypes(RandomDictionary):
    # Use RoomItems.random() to get a random item quantity roll.
    from sprite import NPC
    dic = set_rnd_dic(NPC)
"""

"""
d = {}
for i in range(10000):
    v = rnd_cr_per_level(1)
    d.setdefault(v, 0)
    d[v] += 1

from pprint import pprint
pprint(d)
"""

"""
rnd_potions_grade = RangedDictionary({
    range(1, 40): (0, 1),
    range(41, 101): (1, 1)
})

test_range100(rnd_potions_grade)
print(rnd_potions_grade)
"""

if __name__ == '__main__':
    pass
