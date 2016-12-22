import os
import sys

from pyflakes.checker import Checker

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    import cnl015_2_pysdl2

Checker(['cnl015_2_pysdl2'])
