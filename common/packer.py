"""..."""

import os
import bz2
import pickle
from pickle import Pickler, Unpickler
from io import BytesIO
import shelve

import json

objects = {
    "armors": {
        "source": os.path.join('..', '..', 'etc', 'armors.json'),
        "dest": os.path.join('..', '.', 'data', 'armors.bzp')},
    "weapons": {
        "source": os.path.join('..', '..', 'etc', 'weapons.json'),
        "dest": os.path.join('..', '.', 'data', 'weapons.bzp')},
    "descriptions": {
        "source": os.path.join('..', '..', 'etc', 'descriptions',
                               'descriptions.json'),
        "dest": os.path.join('..', '.', 'data', 'descriptions.bzp')},

}


def split_path(string):
    """..."""
    path = os.path.dirname(string)
    no_ext_f = os.path.basename(os.path.splitext(string)[0])
    return path, no_ext_f


def pack_json(source, dest):
    """..."""
    with open(source) as f:
        bin_data = bz2.compress(pickle.dumps(json.load(f)))
    with open(dest, "wb") as f:
        f.write(bin_data)


def save_dict(data, fname):
    """Save a dictionary data to a bz2-compressed pickle file."""
    bin_data = bz2.compress(pickle.dumps(data))
    with open(fname, "wb") as f:
        f.write(bin_data)


def load_dict(fname):
    """Load a dictionary from a bz2-compressed pickle file."""
    with open(fname, 'rb') as f:
        data = pickle.loads(bz2.decompress(f.read()))
    return data


def unpack_json(fname):
    """..."""
    with open(fname, 'rb') as f:
        data = pickle.loads(bz2.decompress(f.read()))
    return data


def write_json(data, obj):
    """..."""
    with open(obj, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def zshelf_open(filename, flag='c'):
    """..."""
    return DbfilenameZShelf(filename, flag)


def zshelf_unpack(data):
    """Decompress and unpickle data."""
    return pickle.loads(bz2.decompress(data))


def zshelf_pack(data):
    """Compress and pickled data."""
    return bz2.compress(pickle.dumps(data))


class ZShelf(shelve.Shelf):
    """Simple shelf subclassing integrating bz2 handling.

    It is used to compress/uncompress the saved pickles with bz2, generating
    smaller saved game files.
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


if __name__ == '__main__':
    obj = "descriptions"
    pack_json(source=objects[obj]['source'],
              dest=objects[obj]['dest'])
