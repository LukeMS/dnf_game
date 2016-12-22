"""Test for specific_weapons.py."""
import os
import sys
# from memory_profiler import profile

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dnf_main.data_handler.template_handler import TemplateHandler
import data
from util import packer


# @profile
def main():
    """..."""
    from pprint import pprint
    th = TemplateHandler()
    """
    th_cache = th.cache
    print("th_cache: %.2f kb" % (sys.getsizeof(th_cache) / 1024.0))
    th_bzp = packer.pack(th.cache)
    print("th_bzp: %.2f kb" % (sys.getsizeof(th_bzp) / 1024.0))
    th_raw = data.templates.get_templates()
    print("th_raw: %.2f kb" % (sys.getsizeof(th_raw) / 1024.0))
    print(th_cache == th_raw)
    exit()

    te = th.get("TileEntity", "floor")
    pprint(te, indent=4)
    wc1 = th.get("WeaponComponent", 'wushu dart')
    pprint(wc1, indent=4)
    """
    wc2 = th.get("WeaponComponent", "bastard's sting")
    pprint(wc2, indent=4)

if __name__ == '__main__':
    main()
