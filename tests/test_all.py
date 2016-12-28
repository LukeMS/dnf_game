"""Perform every test on the 'test' folder."""

import os
import unittest

from dnf_game.util import dnf_path

if __name__ == '__main__':
    path = os.path.join(dnf_path(), '..', "tests")
    loader = unittest.defaultTestLoader
    suite = loader.discover(path, pattern='*test.py')
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)
