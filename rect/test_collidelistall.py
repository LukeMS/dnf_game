"""..."""

import rect


class Rect(rect.Rect):
    """..."""

    def collidelistall(self, other_list):
        """Test if all rectangles in a list intersect.

        Returns a list of all the indices that contain rectangles that
        collide with the Rect. If no intersecting rectangles are found, an
        empty list is returned.

        Usage:
            rect.collidelistall(list)

        Return:
            list (i.e. indices of rectangles that collide)
        """
        colliderect = self.colliderect
        ret = [i for i, other in enumerate(other_list) if colliderect(other)]
        return ret

    def collidelistall2(self, other_list):
        """Test if all rectangles in a list intersect.

        Returns a list of all the indices that contain rectangles that
        collide with the Rect. If no intersecting rectangles are found, an
        empty list is returned.

        Usage:
            rect.collidelistall(list)

        Return:
            list (i.e. indices of rectangles that collide)
        """
        ret = []
        for n, other in zip(range(len(other_list)), other_list):
            if self.colliderect(other):
                ret.append(n)
        return ret


def setup():
    """..."""
    import random

    other_list = [Rect(x, y, 10, 10) for x in range(20) for y in range(20)]
    _rect = random.choice(other_list)

    return _rect, other_list


def main(_rect, other_list):
    """..."""
    for i in range(500):
        r0 = _rect.collidelistall(other_list)
        r1 = _rect.collidelistall2(other_list)
    assert r0 == r1

if __name__ == '__main__':
    import cProfile
    import os

    _rect, other_list = setup()

    f = os.path.basename(__file__).replace(".py", "")

    tmp = "%s.%s" % (f, "tmp")
    txt = "%s.%s" % (f, "txt")

    cProfile.run('main(_rect, other_list)', tmp)

    import pstats
    stream = open(txt, 'w')
    p = pstats.Stats(tmp, stream=stream)

    # 'time', 'cumulative', 'ncalls'
    p.sort_stats('cumulative').print_stats()

    """
    Tue Dec 13 16:27:36 2016    test_collidelistall.tmp

    5312004 function calls in 21.390 seconds

    ncalls  tottime  percall  cumtime  percall (function)
       500    0.005    0.000   10.487    0.021 (collidelistall)
       500    0.649    0.001   10.898    0.022 (collidelistall2)
    """
