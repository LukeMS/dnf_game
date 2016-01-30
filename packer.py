import os

from pprint import pprint

import json
import bz2
import pickle

JOBJ = os.path.join('.', 'data', 'bestiary', 'bestiary_optimized.json')
BZOBJ = os.path.join('.', 'data', 'bestiary', 'bestiary_optimized.bzp')


def split_path(string):
    path = os.path.dirname(string)
    no_ext_f = os.path.basename(os.path.splitext(string)[0])
    return path, no_ext_f


def pack_json():
    with open(JOBJ) as f:
        bin_data = bz2.compress(pickle.dumps(json.load(f)))
    with open(BZOBJ, "wb") as f:
        f.write(bin_data)


def unpack_json(fname):
    with open(fname, 'rb') as f:
        data = pickle.loads(bz2.decompress(f.read()))
    return data


def write_json(data):
    with open(JOBJ, 'w') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == '__main__':
    pack_json()
