"""Perform every test on the 'test' folder."""

import os
import unittest

if __name__ == '__main__':
    path = os.path.join(os.getcwd(), "tests")
    loader = unittest.defaultTestLoader
    suite = loader.discover(path, pattern='*test.py')
    runner = unittest.TextTestRunner(verbosity=10)
    runner.run(suite)
