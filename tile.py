class Tile:
    # a tile of the map and its properties
    def __init__(self, block_mov, block_sight=None, id=0):
        self.block_mov = block_mov

        # by default, if a tile is block_mov, it also blocks sight
        if block_sight is None:
            block_sight = block_mov
        self.block_sight = block_sight

        self.id = id
        self.visible = False
        self.explored = False


class Floor(Tile):
    def __init__(self, block_mov=False, block_sight=None, id=ord(".")):
        super().__init__(
            block_mov=block_mov,
            block_sight=block_sight,
            id=id)


class Wall(Tile):
    def __init__(self, block_mov=True, block_sight=True, id=ord("#")):
        super().__init__(
            block_mov=block_mov,
            block_sight=block_sight,
            id=id)
