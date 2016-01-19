import random


class RangedDictionary(dict):
    def __getitem__(self, key):
        for rng in self.keys():
            if key == rng:
                return super().__getitem__(key)
            if key in rng:
                return super().__getitem__(rng)
        return super().__getitem__(key)


def rnd_dic_rng(dic):
    min_v = min([key.start for key in dic.keys()])
    max_v = max([key.stop for key in dic.keys()])
    rnd = random.randint(min_v, max_v - 1)
    result = dic.__getitem__(rnd)
    return result


class RoomItems:
    """
    Use RoomItems.random() to get a random item quantity roll.
    """
    dic = RangedDictionary({
        range(0, 70): 0,  # min <= x < max: 0 items
        range(70, 90): 1,  # min <= x < max: 1 item
        range(90, 100): 2  # min <= x < max: 2 items
    })

    @classmethod
    def random(cls):
        return rnd_dic_rng(cls.dic)

if __name__ == '__main__':
    print(RoomItems.random())
