"""Utility classes and methods used by various parts of the game."""

import heapq

import pygame


class PriorityQueue:
    """..."""

    def __init__(self):
        """..."""
        self.elements = []

    def empty(self):
        """..."""
        return len(self.elements) == 0

    def put(self, item, priority):
        """..."""
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """..."""
        return heapq.heappop(self.elements)[1]


def get_mod_case(event):
    """Check the state of the shift and caps lock keys.

    Switches the case of the s string if needed.

    Adapted from: http://inventwithpython.com/extra/gorillas.py
    """
    s = chr(event.key)
    mod = event.mod
    if (bool(mod & pygame.KMOD_RSHIFT or mod & pygame.KMOD_LSHIFT) ^
            bool(mod & pygame.KMOD_CAPS)):
        return s.swapcase()
    else:
        return s


def shoehorn(s):
    """Remove accents (but also other things, like ß‘’“”)."""
    import unicodedata as ud
    return ud.normalize('NFKD', s).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
