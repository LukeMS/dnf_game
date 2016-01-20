# import traceback  # print(traceback.format_exc())
import math
import random
# import sys

import pygame
from constants import TILE_W, TILE_H, GameColor, LEVEL_UP_BASE, LEVEL_UP_FACTOR

from game_types import Position
from item_comp import ItemComponent, DngFeatComponent
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
        self, game, map, x, y, id, color, group,
        name=None, blocks=True, fighter=None, ai=None, item=None, active=True,
        dng_feat=None,
        **kwargs
    ):
        super().__init__()

        # some preliminar preparation
        self.rect = pygame.Rect(x, y, TILE_W, TILE_H)
        #

        # unpack the arguments and store them in the instance
        for arg in [
            "game", "map", "x", "y", "id", "color", "group", "name", "blocks",
            "fighter", "ai", "item", "dng_feat", "active"
        ]:
            setattr(self, arg, eval(arg))
        #

        # some extra required preparation
        if self.name is None:
            self.name = str(type(self)).lower()
            for trash in ["<class '", "'>", "sprite."]:
                self.name = self.name.replace(trash, "")
            self.name = self.name.capitalize()

        if self.fighter:  # let the fighter component know who owns it
            self.fighter.owner = self

        if self.ai:  # let the AI component know who owns it
            self.ai.owner = self

        if self.item:  # let the AI component know who owns it
            self.item.owner = self

        if self.dng_feat:
            self.dng_feat.owner = self

        if self.name != 'cursor':
            self.group.add(self)

        self.default_ai = self.ai
        self.default_color = self.color

        self.set_next_to_vis()

    def __getstate__(self):
        d = dict(self.__dict__)
        for key in ['game', 'map', 'group']:
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
                if self.map.tiles[n].visible:
                    self.next_to_vis = True
                    return
        self.next_to_vis = False

    @property
    def pos(self):
        return Position(self.rect.x, self.rect.y)

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

    def move(self, pos):
        blocked, obj = self.map.is_blocked(pos, self)

        if not blocked:
            # move by the given amount
            # print(self.name, "moving")
            self.pos = pos
            self.set_next_to_vis()

    def move_rnd(self):
        start_pos = self.pos
        next_step = random.choice(self.map.map.get_neighbors(start_pos))
        # print(self.name, "moves erratically")
        self.move(next_step)

    def move_towards(self, target):
        start_pos = self.pos
        end_pos = target.pos

        try:
            path = self.map.map.new_path(start_pos, end_pos)
            self.map.pathing = path[2:-1]
            next_step = Position(*path[1])
            self.move(next_step)
        except KeyError:
            # the path must be blocked
            self.move_rnd()

    def distance_to(self, other, another=None):
        if isinstance(other, tuple):
            x1, y1 = other
        else:
            x1, y1 = other.x, other.y

        if another is None:
            # return the distance to another object
            x2, y2 = self.x, self.y
        else:
            if isinstance(another, tuple):
                x2, y2 = another
            else:
                x2, y2 = another.x, another.y

        dx = x1 - x2
        dy = y2 - y1
        return math.sqrt(dx ** 2 + dy ** 2)

    def update(self):
        self.game.gfx.draw(
            self.id,
            (
                self.rect.x - self.map.offset[0],
                self.rect.y - self.map.offset[1]
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
            self.game.gfx.msg_log.add(
                'Your battle skills grow stronger! You reached level ' +
                str(self.fighter.level) + '!', GameColor.cyan)
            self.map.choice(
                title='Level up! Choose a stat to raise:',
                items=[
                    'Constitution, +20 HP (current: {})'.format(
                        self.fighter.max_hp),
                    'Strength, +1 attack (current: {})'.format(
                        self.fighter.power),
                    'Agility, +1 defense (current: {})'.format(
                        self.fighter.defense)
                ],
                callback=self.increase_stat
            )

    def increase_stat(self, choice):
        id, desc = choice

        if id == 0:
            # old_v = self.fighter.max_hp
            self.fighter.max_hp += 20
            self.fighter.hp += 20
            # new_v = self.fighter.max_hp
        elif id == 1:
            # old_v = self.fighter.power
            self.fighter.power += 1
            # new_v = self.fighter.power
        elif id == 2:
            # old_v = self.fighter.defense
            self.fighter.defense += 1
            # new_v = self.fighter.defense
        else:
            raise AttributeError
        self.game.gfx.msg_log.add(
            desc.replace("current", "previous"),
            GameColor.cyan)


class Death:

    @staticmethod
    def player(player):
        # the game ended!
        player.game.gfx.msg_log.add('You died!')
        player.game_state = 'dead'

        # for added effect, transform the player into a corpse!
        player.id = ord('%')
        player.color = GameColor.dark_red

    @staticmethod
    def monster(monster):
        # transform it into a nasty corpse! it doesn't block, can't be
        # attacked and doesn't move
        monster.game.gfx.msg_log.add('{} is dead! You gain {} xp'.format(
            monster.name.capitalize(), monster.fighter.xp_value))

        monster.id = ord('%')
        monster.color = GameColor.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.item = ItemComponent('remains')
        monster.item.owner = monster
        monster.name = 'remains of ' + monster.name

        monster.group = monster.map.remains
        monster.map.objects.remove(monster)
        monster.map.remains.add(monster)


class Player(GameObject):

    def __init__(
            self, id=ord('@'), color=GameColor.yellow, **kwargs):

        fighter = Fighter(template="player")

        super().__init__(
            id=id, color=color, fighter=fighter, **kwargs)
        self.game.gfx.hp_bar.set_value(self.fighter.hp, self.fighter.max_hp)
        self.inventory = []

    def update_hp(self):
        # max_hp
        self.game.gfx.hp_bar.set_value(self.fighter.hp, self.fighter.max_hp)

    def move(self, dxy):
        super().move(self.pos + dxy)
        self.map.set_fov()

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
                    self.move((dx, dy))
        elif action is 'get':
            for object in self.map.remains:
                if object.item and object.pos == self.pos:
                    object.item.pick_up(getter=self)
                    break
        elif action is 'use':
            for object in self.map.remains:
                if object.dng_feat and object.pos == self.pos:
                    if not object.dng_feat.use(who=self):
                        return

        self.active = False


class Fighter:
    # combat-related properties and methods (monster, player, NPC).
    templates = {
        "player": {
            "max_hp": 30,
            "defense": 2,
            "power": 5,
            "xp_value": None,
            "death_func": Death.player
        },
        "orc": {
            "max_hp": 10,
            "defense": 0,
            "power": 3,
            'xp_value': 35,
            "death_func": Death.monster
        },
        "troll": {
            "max_hp": 16,
            "defense": 1,
            "power": 4,
            'xp_value': 100,
            "death_func": Death.monster
        }
    }

    def __init__(self, template):
        # hp, defense, power, death_func=None):
        for key, value in self.templates[template].items():
            setattr(self, key, value)
        self.hp = self.templates[template]['max_hp']
        self.xp = 5000
        self.level = 1

    def take_damage(self, damage, atkr=None):
        # apply damage if possible
        if damage > 0:
            self.hp -= damage

        # check for death. if there's a death function, call it
        if self.hp <= 0:
            if self.death_func is not None:
                self.death_func(self.owner)
            atkr.gain_xp(self.xp_value)

        self.owner.update_hp()

    def heal(self, amount):
        # heal by the given amount, without going over the maximum
        self.hp += amount
        self.hp = min(self.hp, self.max_hp)
        self.owner.update_hp()

    def attack(self, target):
        # a simple formula for attack damage
        damage = self.power - target.fighter.defense

        if self.owner.ai:
            color = GameColor.red  # I'm a monster!
        else:
            color = None  # I'm the player

        if damage > 0:
            # make the target take some damage
            self.owner.game.gfx.msg_log.add(
                self.owner.name.capitalize() + ' attacks ' + target.name +
                ' for ' + str(damage) + ' hit points.', color)
            target.fighter.take_damage(damage=damage, atkr=self.owner)
        else:
            self.owner.game.gfx.msg_log.add(
                self.owner.name.capitalize() + ' attacks ' + target.name +
                ' but it has no effect!', color)

    def closest_monster(self, who, max_range):
        # find closest enemy, up to a maximum range, and in the player's FOV
        closest_enemy = None
        # start with (slightly more than) maximum range
        closest_dist = max_range + 1

        for object in self.owner.group:
            if object.fighter and not object == who and object.next_to_vis:
                # calculate distance between this object and the player
                dist = who.distance_to(object)
                if dist < closest_dist:  # it's closer, so remember it
                    closest_enemy = object
                    closest_dist = dist
        return closest_enemy


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
        if template in DngFeatComponent.templates:
            new_obj['dng_feat'] = DngFeatComponent(template)
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
        }
    }

    def __init__(self, template, **kwargs):
        new_obj = dict(self.templates[template])
        new_obj.update(kwargs)
        if template in ItemComponent.templates:
            new_obj['item'] = ItemComponent(template)
        super().__init__(
            **new_obj,
            blocks=False, name=str(template).capitalize())

    def update(self):
        if self.map.tiles[self.pos].visible:
            super().update()


class NPC(GameObject):

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
        if template in Fighter.templates:
            new_obj['fighter'] = Fighter(template)
        else:
            new_obj['fighter'] = None
        if new_obj['ai'] is not None:
            new_obj['ai'] = new_obj['ai']()
        super().__init__(**new_obj)

        self.inventory = []

    def update(self):
        if self.map.tiles[self.pos].visible:
            super().update()

    def update_hp(self):
        pass


class Cursor(GameObject):

    def __init__(self, game, map):
        super().__init__(
            game=game, map=map, x=1, y=1, id=None, color=None,
            name='cursor', group=None)

    def move(self, pos, rel_pos):
        # self.pos = pos
        # self.rel_pos = rel_pos
        self.pos = rel_pos
        # print(pygame.sprite.spritecollide(self, self.map.objects, False))
        return self.cursor_collision()

    def cursor_collision(self):
        collision = None
        for object in self.map.objects:
            if object.pos == self.pos and object.next_to_vis:
                collision = object
                break
        if collision is None:
            for object in self.map.remains:
                if object.pos == self.pos and object.next_to_vis:
                    collision = object
                    break
        if collision is None:
            if self.pos in self.map.tiles:
                object = self.map.tiles[self.pos]
                if object.visible or object.explored:
                    collision = object
        return collision
