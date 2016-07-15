"""..."""

import os
import bz2
import pickle
from pickle import Pickler, Unpickler
from io import BytesIO
import shelve

import json


ARMORS = (os.path.join('..', '..', 'etc', 'armors.json'),
          os.path.join('..', '.', 'data', 'armors.bzp'))
WEAPONS = (os.path.join('..', '..', 'etc', 'weapons.json'),
           os.path.join('..', '.', 'data', 'weapons.bzp'))
JOBJ = os.path.join('..', '.', 'data', 'weapons.json')
BZOBJ = os.path.join('..', '.', 'data', 'weapons.bzp')


def split_path(string):
    """..."""
    path = os.path.dirname(string)
    no_ext_f = os.path.basename(os.path.splitext(string)[0])
    return path, no_ext_f


def pack_json(source=JOBJ, dest=BZOBJ):
    """..."""
    with open(source) as f:
        bin_data = bz2.compress(pickle.dumps(json.load(f)))
    with open(dest, "wb") as f:
        f.write(bin_data)


def unpack_json(fname=BZOBJ):
    """..."""
    with open(fname, 'rb') as f:
        data = pickle.loads(bz2.decompress(f.read()))
    return data


def write_json(data, obj=JOBJ):
    """..."""
    with open(obj, 'w') as outfile:
        json.dump(data, outfile, indent=4)


class ZShelf(shelve.Shelf):
    """
    A simple subclassing of shelve.Shelf to compress/uncompress the saved
    pickles with bz2, generating smaller saved game files.
    """
    def __getitem__(self, key):
        """..."""
        try:
            value = self.cache[key]
        except KeyError:
            f = BytesIO(
                bz2.decompress(self.dict[key.encode(self.keyencoding)]))
            value = Unpickler(f).load()
        return value

    def __setitem__(self, key, value):
        """..."""
        f = BytesIO()
        p = Pickler(f, self._protocol)
        p.dump(value)
        self.dict[key.encode(self.keyencoding)] = bz2.compress(f.getvalue())


class DbfilenameZShelf(ZShelf):
    """..."""

    def __init__(self, filename, flag='c'):
        """..."""
        import dbm
        super().__init__(dbm.open(filename, flag))


def zshelf_open(filename, flag='c'):
    """..."""
    return DbfilenameZShelf(filename, flag)

def zshelf_unpack(data):
    """Decompress and unpickle data."""
    return pickle.loads(bz2.decompress(data))

def zshelf_pack(data):
    """Compress and pickled data."""
    return bz2.compress(pickle.dumps(data))


if __name__ == '__main__':
    pass
