"""Functions to populate levels with objects, creatures and features."""

import os
import sys
import random

WP = os.path.join(os.path.dirname(__file__), '..', '..')
if __name__ == '__main__':
    sys.path.insert(0, WP)
from data.constants import MAX_ROOM_MONSTERS
from dnf_main.map_entities import FeatureEntity, ItemEntity, NPCreature
from dnf_main.data_handler.bestiary import Bestiary
from util.rnd_utils import RoomItems, rnd_cr_per_level

"""
TEMPLATE_REQUIREMENTS = {
    'standard': None
}

TEMPLATE_DETAILS = {
    'standard': {
        'requirements': None,
        'base_template': None
    },
    'pillars': {
        'requirements':
    }
}
"""


def place_items():
    """..."""
    pass


def place_doors(*, scene, _map):
    """Place a door at a hall begginning and end.

    Chances of specific door features (locked, stuck, secret) or materials
    are base on a fixed chance and map modifiers.
    """
    def door_feature(pos, room):
        x, y = pos
        template = random.choice(["door_closed", "door_locked", "door_open"])
        FeatureEntity(name=template, scene=scene, pos=(0, 0))

    doors = _map.doors
    [door_feature(pos, room)
        for pos, room in doors.items()
        if _map[pos].feature.name == 'floor']

    return
    """
    for pos, room in doors.items():
        if _map[pos].feature.name == 'floor':
            template = random.choice(["door_closed", "door_locked",
                                      "door_open"])
            door = TileFeature(pos=pos, template=template, room=room)
            scene.add_obj(door, "objects", pos)
            # _map[pos].add_objects(door)
            print(_map[pos])
    """


def populate(*, scene, _map):
    """Place objects and creatures in a level instance."""
    level_n = _map.header.level
    rooms = list(_map.rooms)

    place_doors(scene=scene, _map=_map)

    for room_n, room in enumerate(rooms):

        if room_n > 2:
            num_items = RoomItems.random()
            items_placed = []
            for i in range(num_items):
                xy = room.random_point(_map, ignore=items_placed)
                if xy is not None:
                    items_placed.append(xy)
                    x, y = xy
                    # template = ItemTypes.random()
                    ItemEntity(name="healing potion", scene=scene, pos=(0, 0))

                    """
                    tmp = ItemEntity(name=template, scene=cls,
                                pos=(0, 0))
                    tmp.item.pick_up(getter=cls.player)
                    """

            num_monsters = random.randint(0, MAX_ROOM_MONSTERS)
            monsters_placed = []
            for i in range(num_monsters):
                xy = room.random_point(_map, ignore=monsters_placed)
                if xy is not None:
                    monsters_placed.append(xy)
                    x, y = xy
                    # template = MonsterTypes.random()
                    template = Bestiary.get_by_cr(rnd_cr_per_level(level_n))
                    NPCreature(name=template, scene=scene, pos=(0, 0))
            if room_n == len(rooms) - 1:
                pass

        elif room_n == 0:
            x, y = room.random_point(_map)
            FeatureEntity(name="stair_down", scene=scene, pos=(0, 0))
            # TODO: implement pre-creation of headers linking on map creation.
            scene.current_level._start = x, y

            x, y = room.random_point(_map=_map, ignore=(x, y))

            for item in [
                # random.choice(['falchion', 'aklys']),
                'scroll of fireball', 'scroll of confusion',
                "bastard's sting", "shortsword", "studded leather"
            ]:
                ItemEntity(name=item, scene=scene, pos=(0, 0))
