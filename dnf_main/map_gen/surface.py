"""Surface world map.

Ideas for heat map:
- latitudinal heat as distance to equatorial line (horizontal midline);
- heightmap heat as highest neighbor value with a given radius;
- rainmap as a result of hnv, lnv, lat, heat
- biome as result as indexed table with range keys:
    (heat, h_heat, l, h)


"""
# from collections import namedtuple
import math
import os
import sys
import time

import sdl2

WP = os.path.join(os.path.dirname(__file__), '..', '..')
if __name__ == '__main__':
    sys.path.insert(0, WP)
from dnf_main.scenes.scene_terminal import SurfaceGrid
from util import random_seed
from game_types import TileGroup, TileFeature, MapHeader
import map_gen.rnd_gen
import map_gen.opensimplex
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


class SurfaceGrid(SurfaceGrid):
    """..."""

    def on_key_press(self, event):
        """Handle key presses input for the level."""
        keys = pygame.key.get_pressed()
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if event.key == pygame.K_TAB:
                self.map_gen.next_state(-1 if shift else 1)
        super().on_key_press(event)


class HeightmapTile(TileFeature):
    """..."""

    @property
    def id(self):
        """..."""
        return self.templates[self.feature]["id"]

    @property
    def color(self):
        """..."""
        return self.templates[self.feature]["color"]

    @property
    def feature(self):
        """..."""
        return self._feature

    @property
    def _feature(self):
        """..."""
        interface = self.interface
        return interface.get_tile(
            interface._heightmap.grid.__getitem__(self.pos))


class HeatMapTile(TileFeature):
    """..."""

    @property
    def id(self):
        """..."""
        return ord("§")

    @property
    def value(self):
        """..."""
        x, y = self.pos
        return self.interface._heat_map.get(x, y)

    @property
    def color(self):
        """..."""
        v = self.value
        return (int(v * 255), 0, int((1 - v) * 255))


class RainfallMapTile(TileFeature):
    """..."""

    @property
    def id(self):
        """..."""
        return ord("~")

    @property
    def value(self):
        """..."""
        x, y = self.pos
        return self.interface._rainfall_map.get(x, y)

    @property
    def color(self):
        """..."""
        v = self.value
        return (int((1 - v) * 255), 0, int(v * 255))


class CompositeBiomeTile(HeightmapTile):
    """..."""

    @property
    def _feature(self):
        """..."""
        return self.interface._biome_map.grid.__getitem__(self.pos)


class HeightmapInterface(map_gen.rnd_gen.RndMap2):
    """Interface between heighmap and regular game map generator.

    States:
        height, heat, rain, biomes
    """

    states = {
        "default": HeightmapTile,
        "heat": HeatMapTile,
        "precipitation": RainfallMapTile,
        "biome": CompositeBiomeTile
    }

    def __init__(self, *, mode):
        """..."""
        self._heightmap_mode = mode
        self.state = "default"
        super().__init__()

    @staticmethod
    def get_tile(v):
        """..."""
        # v = _heightmap[pos]
        if v > 0.7:
            return "mountain"
        elif v > 0.6:
            return "hill"
        elif v > 0.4:
            return "land"
        elif v > 0.28:
            return "coast"
        elif v > 0.2:
            return "shallow_water"
        else:
            return "deep_water"

    def make_map(self, *args, **kwargs):
        """..."""
        def get_feature(pos):
            return grid.__getitem__(pos)._feature

        mode = self._heightmap_mode
        self.header = MapHeader(name="surface0", level=0, split=0, cr=0,
                                mode='external')
        cols = 168
        rows = 84
        self.map = map_gen.rnd_gen.Map(
            header=self.header, cols=cols, rows=rows)
        grid = self.map.grid

        self.set_state("default")

        self._heightmap = mode(width=cols, height=rows, interface=self)
        self._heightmap.make_map()
        # self.print()

        self._heat_map = LatitudinalHeatMap(
            width=cols, height=rows, interface=self)
        # self.next_state()

        self._rainfall_map = PrecipitationMap(
            width=cols, height=rows, interface=self)
        # self.next_state()

        self._biome_map = CompositeBiomeMap(
            width=cols, height=rows, interface=self)
        # self.next_state()

        return self.scaled_grid(cols, rows, 2)

    def scaled_grid(self, cols, rows, scale):
        """..."""
        def get_feature(x, y):
            return grid.__getitem__(x // scale, y // scale)

        grid = self._biome_map.grid

        scaled_grid = {(x, y): TileGroup(feature=TileFeature(
            pos=(x, y), template=get_feature(x, y)))
            for x in range(cols * scale) for y in range(rows * scale)}

        return map_gen.rnd_gen.Map(
            header=self.header, cols=cols, rows=rows, grid=scaled_grid)

    def set_state(self, state):
        """..."""
        def set_feature_interface(feature):
            feature.__class__ = feature_class
            feature.interface = self
        self.state = state
        grid = self.map.grid
        feature_class = self.states[state]
        [set_feature_interface(group._feature) for group in grid.values()]

    def next_state(self, k=1):
        """..."""
        if not hasattr(self, "possible_states"):
            self.possible_states = sorted(list(self.states.keys()))
        index = self.possible_states.index(self.state)
        index += k
        index = index % len(self.possible_states)
        state = self.possible_states[index]
        print("Changeing state:", state)
        self.set_state(state)

    def test(self):
        """..."""
        Game(width=1366, height=768, show_fps=False,
             scene=SurfaceGrid, scene_args={'map_gen': self})


class HeightmapBase(object):
    """..."""

    def __init__(self, *, _class, width, height, interface):
        """..."""
        self.interface = interface
        self.name = __file__ + "-" + _class
        self.random = random_seed.get_seeded(self.name)

        self.grid = {}
        self.width = width
        self.height = height
        self.noise = map_gen.opensimplex.OpenSimplex(
            seed=self.random._current_seed)

        print("Creating", width, "by", height, "heightmap...")

    def print(self):
        """..."""
        return
        self.interface.print()

    def erupt_grid(self, k=0.50, r=1, n=1):
        """Apply erupt effect on the grid n times."""
        w = self.width
        h = self.height
        erupt_func = self.erupt

        self.print_stats()
        print("Starting Global Erupt...", end="")
        t0 = time.time()

        [erupt_func(x, y, k, r)
         for x in range(w)
         for y in range(h)
         for i in range(n)]

        t1 = time.time()
        print("Done! (Time: {0:.2f}s)".format(t1 - t0))

    def erode_grid(self, k=0.50, r=1, n=1):
        """Apply erode effect on the grid n times."""
        w = self.width
        h = self.height
        erode_func = self.erode

        self.print_stats()
        print("Starting Global Erupt...", end="")
        t0 = time.time()

        [erode_func(x, y, k, r)
         for x in range(w)
         for y in range(h)
         for i in range(n)]

        t1 = time.time()
        print("Done! (Time: {0:.2f}s)".format(t1 - t0))

    def erupt(self, x, y, k=0.50, r=1):
        """Raise a value by k times its highest neighbor value(hnv).

        Higher k values result in a greater changes.
        No changes are made unless hnv is higher then the current value.
        """
        getv = self.get
        setv = self.set
        neighbors = self.neighbors
        # highest neighbor value
        hnv = max([getv(xn, yn)
                   for xn, yn in neighbors(x, y, r)])

        val = getv(x, y)

        new = hnv * k + val * (1 - k)

        if new > val:
            setv(x, y, new)

    def erode(self, x, y, k=0.50, r=1):
        """Lower a value by k times its lowest neighbor value(lnv).

        Higher k values result in a greater changes.
        No changes are made unless hnv is lower then the current value.
        """
        getv = self.get
        setv = self.set
        neighbors = self.neighbors

        lnv = min([getv(xn, yn) for xn, yn in neighbors(x, y, r)])

        val = getv(x, y)

        new = lnv * k + val * (1 - k)

        if new < val:
            setv(x, y, new)

    def init_grid(self, v=0, noise=False, rnd=False):
        """Fill grid."""
        print("Initializing grid... ", end="")
        t0 = time.time()

        if noise:
            [self.set(x, y, (self.noise.noise2d(x, y) + 1) / 2)
             for x in range(self.width)
             for y in range(self.height)]
        elif rnd:
            [self.set(x, y, self.random.random())
             for x in range(self.width)
             for y in range(self.height)]
        else:
            [self.set(x, y, v)
             for x in range(self.width)
             for y in range(self.height)]
        t1 = time.time()
        print("Done! (Time: {0:.2f}s)".format(t1 - t0))

    def print_stats(self):
        """..."""
        values = self.grid.values()
        _max = max(values)
        _min = min(values)
        _avg = sum(values) / len(values)

        print("max {max:.4f}, min {min:.4f}, avg {avg:.4f}.".format(
            max=_max, min=_min, avg=_avg))
        return _max, _min, _avg

    def smoothe(self, times=1, k=0.80, mode=0):
        """..."""
        getv = self.get
        setv = self.set
        w = self.width
        h = self.height
        # linear smoothing

        self.print_stats()

        if mode == 0:
            for i in range(times):
                print("Smoothing step {}...".format(i + 1), end="")
                t0 = time.time()

                # Rows, left to right
                [setv(x, y, getv(x - 1, y) * (1 - k) + getv(x, y) * k)
                 for x in range(w) for y in range(h)]

                # Rows, right to left
                [setv(x, y, getv(x + 1, y) * (1 - k) + getv(x, y) * k)
                 for x in range(w, -1, -1) for y in range(h)]

                # Columns, bottom to top
                [setv(x, y, getv(x, y - 1) * (1 - k) + getv(x, y) * k)
                 for x in range(w) for y in range(h)]

                # Columns, top to bottom
                [setv(x, y, getv(x, y + 1) * (1 - k) + getv(x, y) * k)
                 for x in range(w) for y in range(h, -1, -1)]

                t1 = time.time()
                print("Done! (Time: {0:.2f}s)".format(t1 - t0))

    def landtype(self, v):
        """..."""
        h = v * 255
        if h >= 200:
            return "land_height2"
        elif h < 200 and h >= 100:
            return "land_height1"
        elif h < 100 and h >= 70:
            return "land_height0"
        elif h < 70 and h >= 50:
            return "water_depth0"
        elif h < 50 and h > 20:
            return "water_depth1"
        else:
            return "water_depth2"

    def neighbors(self, x, y, r=1):
        """..."""
        return [(x + i, y + j)
                for i in range(-r, r + 1)
                for j in range(-r, r + 1)
                if i or j]

    def average_v(self, _list):
        """..."""
        avg_v = (sum(self.get(xn, yn) for xn, yn in _list) /
                 len(_list))
        return avg_v

    def get(self, x, y):
        """..."""
        pos = self._get_pos(x, y)
        return self.grid.__getitem__(pos)

    def _get_pos(self, x, y):
        """Take care of overlap."""
        x = x % self.width
        y = y % self.height
        return x, y

    def set(self, x, y, value):
        """Set a coord i,j to the value val."""
        pos = self._get_pos(x, y)
        self.grid.__setitem__(pos, value)

    def deposition(self, k=0.75):
        """..."""
        randint = self.random.randint
        randrange = self.random.randrange
        w = self.width
        h = self.height
        print_func = self.print
        get_func = self.get
        set_func = self.set
        erode_func = self.erode
        erupt_func = self.erupt

        self.print_stats()
        print("Starting Particle Deposition...", end="")
        t0 = time.time()

        n = 1.0
        area = (w * h)
        step = n / area * 0.70
        x = y = None
        i = 0
        sector_size = area / 40

        while n > 0:
            if not x or not y or (i > sector_size * 1.1):
                # Pick a new spot
                x = randrange(w)
                y = randrange(h)
                i = 0
                print_func()
            else:
                # Walk in a direction
                choice = randint(1, 4)
                if choice == 4:
                    x += 1
                elif choice == 3:
                    x -= 1
                elif choice == 2:
                    y += 1
                else:
                    y -= 1

            if randint(0, 1):
                v = get_func(x, y)
                v = v * (1 - k) + n * k
                set_func(x, y, v)
            else:
                v = get_func(x, y)
                if v > 0.8:
                    if randint(0, 1):
                        erode_func(x, y)
                elif v < 0.5:
                    erupt_func(x, y)
                else:
                    continue

            n -= step

            i += 1

        t1 = time.time()
        print("Done! (Time: {0:.2f}s)".format(t1 - t0))


class Creative02(HeightmapBase):
    """..."""

    def __init__(self, width, height, interface):
        """..."""
        super().__init__(
            _class=self.__class__.__name__, width=width, height=height,
            interface=interface
        )

        self.init_grid(v=0.09)

    def make_map(self):
        """..."""
        self.deposition()

        self.erupt_grid(k=0.7)
        self.print()

        self.smoothe(times=1, k=0.60, mode=0)


class LatitudinalHeatMap(HeightmapBase):
    """..."""

    def __init__(self, *, width, height, interface):
        self.interface = interface
        self.height = height
        self.grid = {y: (math.sin((y / height) * math.pi))
                     for y in range(height)}

    def get(self, x, y):
        """..."""
        pos = self._get_pos(y)
        return self.grid.__getitem__(pos)

    def _get_pos(self, y):
        """Take care of overlap."""
        return y % self.height

    def set(self, x, y, value):
        """Set a coord i,j to the value val."""
        pos = self.get(x, y)
        self.grid.__setitem__(pos, value)


class PrecipitationMap(HeightmapBase):
    """..."""

    def __init__(self, *, width, height, interface):
        def get_feature(pos):
            x, y = _get_pos(*pos)
            return interface.map.grid.__getitem__((x, y))._feature

        def heat(pos):
            x, y = pos
            return lat_heat_map.get(x, y)

        def water_in_r(radius, pos):
            x, y = pos
            neighbors = neighbors_func(x, y)
            count = sum(1 for pos in neighbors if
                        get_feature(pos) in ["shallow_water", "deep_water"])
            return count / len(neighbors)

        def precipitation(height, heat, water_proximity):
            return (
                (1 - height) * 0.25 +
                heat * 0.4 +
                water_proximity * 0.35)

        heighmap = interface._heightmap
        lat_heat_map = interface._heat_map
        neighbors_func = self.neighbors
        _get_pos = self._get_pos

        self.width = width
        self.height = height
        self.interface = interface
        self.grid = {
            pos: precipitation(h, heat(pos), water_in_r(5, pos))
            for pos, h in heighmap.grid.items()
        }


class CompositeBiomeMap(HeightmapBase):
    """..."""

    def __init__(self, *, width, height, interface):
        """..."""
        def get_feature(pos):
            x, y = _get_pos(*pos)
            return interface.map.grid.__getitem__((x, y))._feature

        def heat(pos):
            return heat_map.get(*pos)

        def rainfall(pos):
            return rainfall_map.get(*pos)

        def noise(pos):
            return (heighmap.noise.noise2d(*pos) + 1) / 2

        def compose_biome(pos, _height, _heat, rain):
            n = noise(pos)
            height = _height * 0.95 + n * 0.05
            height2 = _height * 0.90 + n * 0.1
            heat = _heat * 0.70 + (1 - rain) * 0.20 + n * 0.1
            heat2 = _heat * 0.70 + (1 - rain) * 0.15 + n * 0.15

            if heat2 < 0.33:
                if height <= 0.2:
                    return "arctic_deep_water"
                elif height <= 0.27:
                    return "arctic_shallow_water"
                elif height <= 0.32:
                    return "arctic coast"
                elif 0.78 < height2 < 0.82:
                    return "arctic mountain"
                elif 0.70 < height2 < 0.72:
                    return "arctic hill"
                # arctic
                return "arctic land"

            # heat = _heat * 0.65 + (1 - rain) * 0.25 + n * 0.1
            if height <= 0.22:
                return "deep_water"
            elif height <= 0.27:
                return "shallow_water"

            elif heat2 < 0.52:
                # temperate
                if height <= 0.31:
                    return "coast"
                elif (0.79 < height2 < 0.82) or 0.95 < height:
                    return "mountain"
                elif 0.70 < height2 < 0.72:
                    return "hill"
                elif rain < 0.25 and (0.44 < height2 < 0.5):
                    return "temperate desert"
                elif rain < 0.29:
                    return "boreal grassland"
                else:
                    return "boreal forest"

            elif heat2 < 0.77:
                # subtropical/temperate
                if height <= 0.31:
                    return "coast"
                elif (0.79 < height2 < 0.82) or 0.95 < height:
                    return "mountain"
                elif 0.70 < height2 < 0.72:
                    return "hill"
                elif rain < 0.32 and (0.44 < height2 < 0.5):
                    return "subtropical desert"
                elif rain < 0.38 and (height2 < 0.39):
                    return "woodland"
                elif rain < 0.45 and (height2 < 0.45):
                    return "temperate deciduous forest"
                elif rain >= 0.45 or (0.55 < height2 < 0.6):
                    return "temperate rain forest"
                # elif rain < 0.34 or (height2 < 0.37):
                else:
                    return "grassland"

            else:
                # tropical
                if height <= 0.32 and rain > 0.34:
                    return "coast"
                elif (0.79 < height2 < 0.82) or 0.90 < height:
                    return "mountain"
                elif 0.70 < height2 < 0.72:
                    return "hill"
                elif rain >= 0.49 and ((0.35 < height2 < 0.44) or
                                       height >= 0.55):
                    return "tropical rain forest"
                elif heat > 0.80 and (height2 > 0.76 or rain < 0.30):
                    return "tropical desert"
                # if rain < 0.51 or (height < 0.39):
                else:
                    return "savana"
                """
                if rain >= 0.51 and (0.45 < height < 0.55):
                    return "shallow_water"
                elif rain < 0.55:
                    return "tropical seasonal forest"
                """

        heighmap = interface._heightmap
        heat_map = interface._heat_map
        rainfall_map = interface._rainfall_map
        _get_pos = self._get_pos

        self.width = width
        self.height = height
        self.interface = interface
        self.grid = {
            pos: compose_biome(pos, h, heat(pos), rainfall(pos))
            for pos, h in heighmap.grid.items()
        }

if __name__ == '__main__':
    def graphic_map(mode):
        """..."""
        m = HeightmapInterface(mode=mode)
        m.test()

    # @profile
    def std_map(mode):
        """..."""
        cols = 136
        rows = 76
        _heightmap = mode(width=cols, height=rows, interface=None)
        _heightmap.make_map()

    # graphic_map(Creative02)
