"""..."""

import os

from dnf_game.util import packer, dnf_path


PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..')
SRC_PATH = os.path.join(PATH, 'etc')
DST_PATH = os.path.join(dnf_path(), 'data')

OBJECTS = {
    "armors": {
        "source": os.path.join(SRC_PATH, 'armors.json'),
        "dest": os.path.join(DST_PATH, 'armors.bzp')},
    "weapons": {
        "source": os.path.join(SRC_PATH, 'weapons.json'),
        "dest": os.path.join(DST_PATH, 'weapons.bzp')},
    "descriptions": {
        "source": os.path.join(SRC_PATH, 'descriptions',
                               'descriptions.json'),
        "dest": os.path.join(DST_PATH, 'descriptions.bzp')},
    "bestiary": {
        "source": os.path.join(SRC_PATH, 'bestiary.json'),
        "dest": os.path.join(DST_PATH, 'bestiary_optimized.bzp')},

}

def create_tinydb():
    import json
    from pprint import pprint
    from dnf_game.util.tinydb import InMemoryBZ2PStorage

    """

    source = _type['source']
    """
    _type = OBJECTS["bestiary"]
    dest = _type['dest']

    old_data = packer.unpack_json(dest)
    # obj = {value for value in old_data.values()}
    # pprint(obj, indent=4)
    # exit()

    bz2p = dest.replace(".bzp", ".bz2p")

    # packer.pack_data(obj, bz2p)

    from tinydb import TinyDB, Query

    db = TinyDB(bz2p, storage=InMemoryBZ2PStorage)
    db.insert_multiple([value for value in old_data.values()])
    db._storage.write_to_disk()

def create_tiny_db():
    import json
    from pprint import pprint
    from dnf_game.util.tinydb import InMemoryBZ2PStorage

    """

    source = _type['source']
    """
    _type = OBJECTS["bestiary"]
    dest = _type['dest']

    old_data = packer.unpack_json(dest)
    # obj = {value for value in old_data.values()}
    # pprint(obj, indent=4)
    # exit()

    bz2p = dest.replace(".bzp", ".bz2p")

    # packer.pack_data(obj, bz2p)

    from tinydb import TinyDB, Query

    db = TinyDB(bz2p, storage=InMemoryBZ2PStorage)
    db.insert_multiple([value for value in old_data.values()])
    print(db._storage.memory)
    db._storage.write_to_disk()


if __name__ == '__main__':
    from tinydb import TinyDB, Query
    from dnf_game.util.tinydb import InMemoryBZ2PStorage
    from pprint import pprint

    _type = OBJECTS["bestiary"]
    dest = _type['dest']
    bz2p = dest.replace(".bzp", ".bz2p")
    db = TinyDB(bz2p, storage=InMemoryBZ2PStorage)
    Beast = Query()
    pprint(db.search(Beast.fancy == 'Hawk'), indent=4)
    pprint(db.search(Beast.cr < 1), indent=4)
