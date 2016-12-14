"""..."""

import rect


class Rect(rect.Rect):
    """..."""

    def collidedictall2(self, other_dict, rects_values=0):
        """Test if one rectangle instersect with others in a dictionary.

        Returns a list of tuples with the key and value of the rectangles in
        the argument dictionary that intersect with the Rect. If no
        collisions are found an empty list is returned.

        Rect objects are not hashable and cannot be used as keys in a
        dictionary, only as values.

        Usage:
            collidedictall(dict)

        Returns:
            list of tuples ([(key, value), ...] with the rectangles that
            collide)
            empty list (if none collide)
        """
        ret = []
        for key, val in other_dict.items():
            if self.colliderect(val):
                ret.append((key, val))
        return ret


def setup():
    """..."""
    import random

    other_dict = {(x, y): Rect(x, y, 10, 10)
                  for x in range(20) for y in range(20)}
    _rect = other_dict.pop(random.choice(list(other_dict.keys())))

    return _rect, other_dict


def main(_rect, other_dict):
    """..."""
    def collidedictall(_rect, other_dict):
        return [_rect.collidedictall(other_dict) for x in range(n)]

    def collidedictall2(_rect, other_dict):
        return [_rect.collidedictall2(other_dict) for x in range(n)]

    n = 500
    r0 = collidedictall(_rect, other_dict)
    r1 = collidedictall2(_rect, other_dict)
    assert r0 == r1

if __name__ == '__main__':
    import cProfile
    import os

    _rect, other_dict = setup()

    f = os.path.basename(__file__).replace(".py", "")

    tmp = "%s.%s" % (f, "tmp")
    txt = "%s.%s" % (f, "txt")

    cProfile.run('main(_rect, other_dict)', tmp)

    import pstats
    stream = open(txt, 'w')
    p = pstats.Stats(tmp, stream=stream)

    # 'time', 'cumulative', 'ncalls'
    p.sort_stats('cumulative').print_stats()
