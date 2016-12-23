"""..."""

from dnf_game.util.rnd_utils import RangedDictionary

rnd_armor_material = RangedDictionary({
    range(1, 96): "standard",
    range(96, 101): "special"
})


def get_equipment(string):
    """..."""
    pattern = ""


def calculate_hoard(total, specifics=None):
    """..."""
    specifics = specifics if specifics else []
    for specific in specifics:
        pass
