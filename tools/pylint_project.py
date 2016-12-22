import os
import sys

from pylint.lint import Run
if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pylint.lint import Run
Run(['cnl015_2_pysdl2'])
