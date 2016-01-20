from pickle import Pickler, Unpickler
from io import BytesIO

import shelve

import bz2


class ZShelf(shelve.Shelf):
    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            f = BytesIO(
                bz2.decompress(self.dict[key.encode(self.keyencoding)]))
            value = Unpickler(f).load()
            if self.writeback:
                self.cache[key] = value
        return value

    def __setitem__(self, key, value):
        if self.writeback:
            self.cache[key] = value
        f = BytesIO()
        p = Pickler(f, self._protocol)
        # print(key, value)  # to figure error out
        p.dump(value)
        self.dict[key.encode(self.keyencoding)] = bz2.compress(f.getvalue())


class DbfilenameZShelf(ZShelf):
    def __init__(self, filename, flag='c', protocol=None, writeback=False):
        import dbm
        super().__init__(dbm.open(filename, flag), protocol, writeback)


def open(filename, flag='c'):
    return DbfilenameZShelf(filename, flag)
