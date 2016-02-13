import os

from pprint import pprint

import json
import bz2
import pickle


ARMORS = (os.path.join('..', 'etc', 'armors.json'),
          os.path.join('.', 'data', 'armors.bzp'))
WEAPONS = (os.path.join('..', 'etc', 'weapons.json'),
           os.path.join('.', 'data', 'weapons.bzp'))
JOBJ = os.path.join('.', 'data', 'weapons.json')
BZOBJ = os.path.join('.', 'data', 'weapons.bzp')


def split_path(string):
    path = os.path.dirname(string)
    no_ext_f = os.path.basename(os.path.splitext(string)[0])
    return path, no_ext_f


def pack_json(source=JOBJ, dest=BZOBJ):
    with open(source) as f:
        bin_data = bz2.compress(pickle.dumps(json.load(f)))
    with open(dest, "wb") as f:
        f.write(bin_data)


def unpack_json(fname=BZOBJ):
    with open(fname, 'rb') as f:
        data = pickle.loads(bz2.decompress(f.read()))
    return data


def write_json(data, obj=JOBJ):
    with open(obj, 'w') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == '__main__':
    pack_json(*ARMORS)
