import os
import sys

if not os.path.isdir('map_gen'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game_types import TileFeature, MapHeader
import map_gen.rnd_gen
# import mylib.heightmaps.creative02 as particle_map_02
from common import packer


def pack_map(_heightmaps, fname):
    """..."""
    data = {'map': _heightmaps.grid,
            'height': _heightmaps.height,
            'width': _heightmaps.width}

    path = os.path.join(os.path.dirname(__file__), fname + ".bzp")
    packer.save_dict(data, path)


def unpack_map(fname):
    """..."""
    path = os.path.join(os.path.dirname(__file__), fname + ".bzp")
    data = packer.load_dict(path)

    grid = data['map']
    height = data['height']
    width = data['width']

    return grid, width, height


class Surface001(map_gen.rnd_gen.RndMap2):
    """..."""

    def make_map(self, *args, **kwargs):
        """..."""
        # _heightmaps = particle_map_02.ParticleDeposition(256, 128)
        # pack_map(_heightmaps, 'creative02')
        self._heightmap, cols, rows = unpack_map('creative02')

        self.header = MapHeader(name="surface0", level=0, split=0, cr=0,
                                mode='external')
        map_gen.rnd_gen.MapCreatorBase.make_map(self, cols=cols, rows=rows)
        self.create_tiles()
        self.print()

    def create_tiles(self):
        """..."""
        def get_tile(pos):
            v = self._heightmap[pos]
            if v > 0.7:
                desc = "mountain"
            elif v > 0.6:
                desc = "hill"
            elif v > 0.4:
                desc = "land"
            elif v > 0.28:
                desc = "coast"
            elif v > 0.2:
                desc = "shallow_water"
            else:
                desc = "deep_water"

            return TileFeature(pos, desc)

        _map = self.map
        [tile.set_feature(get_tile(pos))
         for pos, tile in _map.items()]

    def test(self):
        """..."""
        from manager import Game
        from terminal import SurfaceGrid

        Game(width=1024, height=768, show_fps=False,
             scene=SurfaceGrid, scene_args={'map_gen': self})


if __name__ == '__main__':

    m = Surface001()
    m.test()
