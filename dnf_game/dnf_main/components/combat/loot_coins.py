"""..."""

import random

from dnf_game.dnf_main.components.combat.char_roll import roll


class Coins:
    """..."""

    def __init__(self, quantity=0):
        """..."""
        self.quantity = quantity

    def value(self):
        """..."""
        return self.quantity

    def weight(self):
        """..."""
        pass
        # self.quantity x something

    def __str__(self):
        """..."""
        return "{} gp".format(self.quantity)

    def __repr__(self):
        """..."""
        return self.__str__()

    def __add__(self, y):
        """..."""
        try:
            v = self.quantity + y.quantity
        except AttributeError:
            v = self.quantity + y
        return Coins(v)

    def __sub__(self, y):
        """..."""
        try:
            v = self.quantity - y.quantity
        except AttributeError:
            v = self.quantity - y
        return Coins(v)


def calculate_hoard(total):
    """..."""
    if total < 10:
        return Coins(total)
    if total < 100:
        q = roll(faces=10,
                 rolls=total // 5,
                 modifier=random.randint(-2, 1))
        return Coins(q)
    else:
        q = roll(faces=100,
                 rolls=total // 50,
                 modifier=random.randint(-2, 1))
        return Coins(q)
