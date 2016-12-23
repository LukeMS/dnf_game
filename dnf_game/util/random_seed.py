import os
import random

import inspect

stack = inspect.stack()
start = 2

_seed = None


class Random(random.Random):

    def seed(self, a=None, version=3):
        from os import urandom as _urandom
        from hashlib import sha512 as _sha512
        if a is None:
            try:
                # Seed with enough bytes to span the 19937 bit
                # state space for the Mersenne Twister
                a = int.from_bytes(_urandom(2500), 'big')
            except NotImplementedError:
                import time
                a = int(time.time() * 256)  # use fractional seconds

        if version == 2:
            if isinstance(a, (str, bytes, bytearray)):
                if isinstance(a, str):
                    a = a.encode()
                a += _sha512(a).digest()
                a = int.from_bytes(a, 'big')

        self._current_seed = a
        super().seed(a)

    def get_seed(self):
        return self._current_seed

def get_seeded(f):
    fname = (f.replace('.py', '') + '.seed')
    if os.path.isfile(fname):
        with open(fname) as f:
            _seed = int(f.read())
    else:
        _seed = None

    rnd = Random(_seed)
    if _seed is None:
        _seed = rnd.get_seed()

    if not os.path.isfile(fname):
        with open(fname, 'w') as f:
            f.write(str(_seed))

    return rnd
