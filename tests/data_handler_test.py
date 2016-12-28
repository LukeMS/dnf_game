"""Data Handler Test."""

import unittest

from dnf_game.dnf_main.map_entities import FeatureEntity
from dnf_game.dnf_main.data_handler.template_handler import TemplateHandler


class TestDataHandler(unittest.TestCase):
    """..."""

    def test_bastards_sting(self):
        """..."""
        TemplateHandler()
        FeatureEntity(name="stair_up", scene=None, pos=(0, 0))


if __name__ == '__main__':
    unittest.main(verbosity=2)
