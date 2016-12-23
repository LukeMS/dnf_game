"""..."""

from tinydb.storages import Storage, touch

from dnf_game.util import packer


class InMemoryBZ2PStorage(Storage):
    """In-memory dict, (un)pickled from/to a bz2 file (bz2p)."""

    def __init__(self, path):
        """Initialization.

        Read from the storage file and store it in memory. If the file doesn't
        exist it will be created.

        :param path: Where to store/load the JSON data.
        :type path: str
        """
        super().__init__()
        self._f_path = path
        touch(path)  # Create file if not exists
        with open(path, "r+") as f:
            f.seek(0, 2)
            size = f.tell()
        if size:
            self.memory = packer.load_dict(path)
        else:
            self.memory = {}

    def read(self):
        """..."""
        return self.memory

    def write(self, data):
        """Write the current state of the database to the storage.

        :param data: The current state of the database.
        :type data: dict
        """
        self.memory = data

    def write_to_disk(self):
        """..."""
        packer.save_dict(data=self.memory, fname=self._f_path)
