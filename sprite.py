# import traceback  # print(traceback.format_exc())
import math
import random
# import sys

import pygame
from constants import TILE_W, TILE_H, GameColor, LEVEL_UP_BASE, LEVEL_UP_FACTOR

from game_types import Position
import obj_components
import ai_comp


class Group(pygame.sprite.Group):

    def contain_pos(self, pos):
        for sprite in self.__iter__():
            xy = (sprite.rect.x, sprite.rect.y)
            if pos == xy:
                return True
        return False


class GameObject(pygame.sprite.Sprite):
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.

    def __init__(
        self, scene, x, y, id, color, group,
        name=None, blocks=True, fighter=None, ai=None, item=None, active=True,
        dng_feat=None, equipment=None,
        **kwargs
    ):
        super().__init__()

        # some preliminar preparation
        self.rect = pygame.Rect(x, y, TILE_W, TILE_H)
        #

        # unpack the arguments and store them in the instance
        for arg in [
            "scene", "x", "y", "id", "color", "group", "name", "blocks",
            "fighter", "ai", "item", "equipment", "dng_feat", "active"
        ]:
            value = eval(arg)

            # component initialization
            if hasattr(value, 'owner'):  # if it is a component
                value.owner = self  # set its owner

            setattr(self, arg, value)
        #

        # some extra required preparation
        if self.name is None:
            self.name = str(type(self)).lower()
            for trash in ["<class '", "'>", "sprite."]:
                self.name = self.name.replace(trash, "")
            self.name = self.name.capitalize()

        if self.name != 'cursor':
            self.group.add(self)

        self.default_ai = self.ai
        self.default_color = self.color

        self.set_next_to_vis()

    def __getstate__(self):
        d = dict(self.__dict__)
        for key in ['scene', 'group']:
            if key in d:
                del d[key]
        return d

    def is_clicked(self):
        return (
            pygame.mouse.get_pressed()[0]
            and self.rect.collidepoint(pygame.mouse.get_pos()))

    # next to a visible tile
    def set_next_to_vis(self):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                n = self.pos + (x, y)
                if self.scene.grid[n].visible:
                    self.next_to_vis = True
                    return
        self.next_to_vis = False

    @property
    def pos(self):
        return Position((self.rect.x, self.rect.y))

    @pos.setter
    def pos(self, value):
        if isinstance(value, tuple):
            self.rect.x, self.rect.y = value
        else:
            self.rect.x, self.rect.y = value.x, value.y

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    def __floordiv__(self, n):
        if isinstance(n, tuple):
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        elif isinstance(n, (int, float)):
            return Position(int(self.x // n), int(self.y // n))

    def move(self, pos=None):
        if pos is None:
            return None
        blocked, obj = self.scene.map_mgr.is_blocked(pos, self)

        if not blocked:
            self.pos = pos
            self.set_next_to_vis()
            return True
        return None

    def move_rnd(self):
        start_pos = self.pos
        next_step = random.choice(self.scene.map_mgr.get_neighbors(start_pos))
        return self.move(next_step)

    def move_towards(self, target):
        start_pos = self.pos
        end_pos = target.pos

        try:
            path = self.scene.map_mgr.a_path(start_pos, end_pos)
            if len(path) < 10:
                next_step = Position(path[1])
                if self.move(next_step):
                    return path
                else:
                    return None
            else:
                return self.move_rnd()
        except KeyError:
            # the path must be blocked
            return self.move_rnd()

    def distance_to(self, pos1, pos2=None):
        if pos2 is None:
            pos2 = self.pos
        return self.scene.map_mgr.distance(pos1.pos, pos2)

    def update(self):
        self.scene.gfx.draw(
            self.id,
            (
                self.rect.x - self.scene.offset[0],
                self.rect.y - self.scene.offset[1]
            ),
            color=self.color)

    def gain_xp(self, value):
        self.fighter.xp += value

        # see if the creature's experience is enough to level-up
        level_up_xp = LEVEL_UP_BASE + self.fighter.level * LEVEL_UP_FACTOR
        if self.fighter.xp >= level_up_xp:
            # it is! level up
            self.fighter.level += 1
            self.fighter.xp -= level_up_xp
            self.scene.gfx.msg_log.add(
                'Your battle skills grow stronger! You reached level ' +
                str(self.fighter.level) + '!', GameColor.cyan)
            self.scene.choice(
                title='Level up! Choose a stat to raise:',
                items=[
                    'Constitution, +10 HP (current: {})'.format(
                        self.fighter.max_hp),
                    'Strength, +1 attack (current: {})'.format(
                        self.fighter.base_power),
                    'Agility, +1 defense (current: {})'.format(
                        self.fighter.base_defense)
                ],
                callback=self.increase_stat
            )

    def increase_stat(self, choice):
        id, desc = choice

        if id == 0:
            self.fighter.base_max_hp += 10
            self.update_hp()

        elif id == 1:
            self.fighter.base_power += 1

        elif id == 2:
            self.fighter.base_defense += 1

        else:
            raise AttributeError
        self.scene.gfx.msg_log.add(
            desc.replace("current", "previous"),
            GameColor.cyan)


class Player(GameObject):

    def __init__(
            self, id=ord('@'), color=GameColor.yellow, **kwargs):

        fighter = obj_components.Fighter(template="player")

        super().__init__(
            id=id, color=color, fighter=fighter, **kwargs)
        self.inventory = []
        self.scene.gfx.hp_bar.set_value(self.fighter.hp, self.fighter.max_hp)

    def update_hp(self):
        # max_hp
        self.scene.gfx.hp_bar.set_value(self.fighter.hp, self.fighter.max_hp)

    def action(self, dx=0, dy=0, action='std', key=None):
        if action is 'std':
            if not (dx == 0 == dy):
                # the coordinates the player is moving to/attacking
                pos = self.pos + (dx, dy)

                # try to find an attackable object there
                target = None
                for object in self.group:
                    if object.fighter and object.pos == pos:
                        target = object
                        break

                if target is not None:
                    self.fighter.attack(target)
                else:
                    self.move(pos)
        elif action is 'get':
            for object in self.scene.remains:
                if object.item and object.pos == self.pos:
                    if object.item.pick_up(getter=self):
                        self.active = False
                        return True
            return False
        elif action is 'use':
            for object in self.scene.remains:
                if object.dng_feat and object.pos == self.pos:
                    if object.dng_feat.use(who=self):
                        self.active = False
                        return True
            return False

        self.active = False
        return True


class DngFeature(GameObject):
    templates = {
        'stair_up': {
            'id': "<",
            'color': GameColor.gray,
            'blocks': False
        },
        'stair_down': {
            'id': "<",
            'color': GameColor.gray,
            'blocks': False
        }
    }

    def __init__(self, template, **kwargs):
        new_obj = dict(self.templates[template])
        new_obj.update(kwargs)
        if template in obj_components.DngFeat.templates:
            new_obj['dng_feat'] = obj_components.DngFeat(template)
        super().__init__(
            **new_obj, name=str(template).capitalize())


class Item(GameObject):

    templates = {
        'healing potion': {
            'id': "!",
            'color': GameColor.violet,
            '_rarity': 30
        },
        'scroll of lightning bolt': {
            'id': "#",
            'color': GameColor.yellow,
            '_rarity': 90
        },
        'scroll of confusion': {
            'id': "#",
            'color': GameColor.yellow,
            '_rarity': 1
        },
        'scroll of fireball': {
            'id': "#",
            'color': GameColor.yellow,
            '_rarity': 90
        },
        'dagger': {
            'id': '-',
            'color': GameColor.sky,
            '_rarity': 85
        },
        'short sword': {
            'id': '´',
            'color': GameColor.sky,
            '_rarity': 90
        },
        'sword': {
            'id': '/',
            'color': GameColor.sky,
            '_rarity': 95
        },
        'shield': {
            'id': '[',
            'color': GameColor.darker_orange,
            '_rarity': 90
        }
    }

    def __init__(self, template, **kwargs):
        new_obj = dict(self.templates[template])
        new_obj.update(kwargs)

        if template in obj_components.Item.templates:
            new_obj['item'] = obj_components.Item(template)

        if template in obj_components.Equipment.templates:
            new_obj['equipment'] = obj_components.Equipment(template)

        super().__init__(
            **new_obj,
            blocks=False, name=str(template).capitalize())

    def update(self):
        if self.scene.grid[self.pos].visible:
            super().update()


class NPC(GameObject):

    path = None

    templates = {
        'orc': {
            "id": ord('o'),
            "color": GameColor.desaturated_green,
            "ai": ai_comp.Basic,
            "_rarity": 20
        },
        'troll': {
            "id": ord('T'),
            "color": GameColor.darker_green,
            "ai": ai_comp.Basic,
            "_rarity": 80
        }
    }

    def __init__(self, template, **kwargs):
        new_obj = dict(self.templates[template])
        new_obj.update(kwargs)
        new_obj.update({'name': str(template).capitalize()})
        if template in obj_components.Fighter.templates:
            new_obj['fighter'] = obj_components.Fighter(template)
        else:
            new_obj['fighter'] = None
        if new_obj['ai'] is not None:
            new_obj['ai'] = new_obj['ai']()
        super().__init__(**new_obj)

        self.inventory = []

    def update(self):
        if self.scene.grid[self.pos].visible:
            super().update()

    def update_hp(self):
        pass


class Cursor(GameObject):

    def __init__(self, scene):
        super().__init__(
            scene=scene, x=1, y=1, id=None, color=None,
            name='cursor', group=None)

    def move(self, pos, rel_pos):
        self.pos = rel_pos
        return self.cursor_collision()

    def cursor_collision(self):
        for object in self.scene.objects:
            if object.pos == self.pos and object.next_to_vis:
                return object

        for object in self.scene.remains:
            if object.pos == self.pos and object.next_to_vis:
                return object

        if self.pos in self.scene.grid:
            object = self.scene.grid[self.pos]
            if object.visible or object.explored:
                return object
