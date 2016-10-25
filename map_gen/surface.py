import os
import sys

if not os.path.isdir('map_gen'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import map_gen.rnd_gen
import mylib.heightmaps.creative02 as particle_map_02
from common import packer
from tile import Tile


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

    return grid, height, width


class Surface001(map_gen.rnd_gen.RndMapChamber):
    """..."""

    def make_map(self, *args, **kwargs):
        """..."""
        # _heightmaps = particle_map_02.ParticleDeposition(256, 128)
        # pack_map(_heightmaps, 'creative02')
        self._heightmap, self.height, self.width = unpack_map('creative02')

        self.terminal.print = self.print
        self.terminal.map_w = self.width
        self.terminal.map_h = self.height
        self.create_tiles()
        self.terminal.map = self.map
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

            return Tile(pos, desc)

        width = self.width
        height = self.height
        self.map = {(x, y): get_tile((x, y))
                    for x in range(width) for y in range(height)}

    def test(self):
        """..."""
        from pygame_manager import manager
        from terminal import SurfaceTiledGrid

        scene = manager.Manager(scene=SurfaceTiledGrid, framerate=10,
                                width=None, height=None, show_fps=False)
        scene.current_scene.text = [' ']
        scene.wrap = False

        self.visualize = True

        self.terminal = scene.current_scene
        self.make_map()
        while scene.alive:
            scene.on_event()


if __name__ == '__main__':

    m = Surface001()
    m.test()
