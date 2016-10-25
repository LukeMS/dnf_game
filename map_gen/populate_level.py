"""Functions to populate levels with objects, creatures and features."""

import os
import sys
import random

if not os.path.isdir('map_gen'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rnd_utils import RoomItems, rnd_cr_per_level
import sprite
from combat.bestiary import Bestiary
from constants import MAX_ROOM_MONSTERS

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
    pass

def populate(level_n, level_scene, grid, rooms):
    """Place objects and creatures in a level instance."""
    def new_xy(room, objects=None):
        attempts = 0
        while True:
            if attempts > 10:
                return None
            xy = room.random_point(_map=grid)
            if xy not in objects:
                return xy
            attempts += 1

    for room_n, room in enumerate(rooms):

        if room_n > 2:
            num_items = RoomItems.random()
            items_placed = []
            for i in range(num_items):
                xy = new_xy(room, items_placed)
                if xy is not None:
                    items_placed.append(xy)
                    x, y = xy
                    # template = ItemTypes.random()
                    sprite.Item(template="healing potion",
                                scene=level_scene,
                                x=x, y=y)

                    """
                    tmp = sprite.Item(template=template, scene=cls,
                                x=x, y=y)
                    tmp.item.pick_up(getter=cls.player)
                    """

            num_monsters = random.randint(0, MAX_ROOM_MONSTERS)
            monsters_placed = []
            for i in range(num_monsters):
                xy = new_xy(room, monsters_placed)
                if xy is not None:
                    monsters_placed.append(xy)
                    x, y = xy
                    # template = MonsterTypes.random()
                    template = Bestiary.get_by_cr(rnd_cr_per_level(level_n))
                    sprite.NPC(template=template,
                               scene=level_scene,
                               x=x, y=y)
            if room_n == len(rooms) - 1:
                pass

        elif room_n == 0:
            x, y = room.random_point(_map=grid)
            player = getattr(level_scene, 'player', None)
            if player:
                level_scene.rem_obj(player, 'creatures',
                                    player.pos)

                player.pos = (x, y)

                level_scene.add_obj(player, 'creatures',
                                    player.pos)
            else:
                if level_scene.create_char is not None:
                    level_scene.player = sprite.Player(
                        scene=level_scene, x=x, y=y,
                        combat=level_scene.create_char)
                else:
                    level_scene.player = sprite.Player(
                        scene=level_scene, x=x, y=y)

            x, y = new_xy(room, [level_scene.player.pos])
            template = "stair_down"
            sprite.DngFeature(template=template,
                              scene=level_scene,
                              x=x, y=y)

            x, y = new_xy(room, [level_scene.player.pos, (x, y)])

            for item in [
                # random.choice(['falchion', 'aklys']),
                'scroll of fireball', 'scroll of confusion',
                "bastard's sting", "shortsword", "studded leather"
            ]:
                sprite.Item(template=item, scene=level_scene,
                            x=x, y=y)
