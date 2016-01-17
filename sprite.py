# import traceback  # print(traceback.format_exc())
import math
import random
# import sys

import pygame
from constants import TILE_W, TILE_H, GameColor

from game_types import Position


class Death:

    @staticmethod
    def player(player):
        # the game ended!
        print('You died!')
        player.map.game_state = 'dead'

        # for added effect, transform the player into a corpse!
        player.id = ord('%')
        player.color = GameColor.dark_red

    @staticmethod
    def monster(monster):
        # transform it into a nasty corpse! it doesn't block, can't be
        # attacked and doesn't move
        print(monster.name.capitalize() + ' is dead!')
        monster.id = ord('%')
        monster.color = GameColor.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name

        monster.group = monster.map.remains
        monster.map.objects.remove(monster)
        monster.map.remains.add(monster)


class Fighter:
    # combat-related properties and methods (monster, player, NPC).

    def __init__(self, hp, defense, power, death_func=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

        self.death_func = death_func

    def take_damage(self, damage):
        # apply damage if possible
        if damage > 0:
            self.hp -= damage

        # check for death. if there's a death function, call it
        if self.hp <= 0:
            function = self.death_func
            if function is not None:
                function(self.owner)

    def attack(self, target):
        # a simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            # make the target take some damage
            print(
                self.owner.name.capitalize() + ' attacks ' + target.name +
                ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            print(
                self.owner.name.capitalize() + ' attacks ' + target.name +
                ' but it has no effect!')


class BasicMonsterAI:
    # AI for a basic monster.

    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if monster.map.tiles[monster.pos].visible:
            target = monster.map.player
            # move towards player if far away
            if monster.distance_to(monster.map.player) > 1:
                # print("{} moves".format(monster.name))
                monster.move_towards(target=target)

            # close enough, attack! (if the player is still alive.)
            elif target.fighter.hp > 0:
                monster.fighter.attack(target)

        monster.active = False


class GameObject(pygame.sprite.Sprite):
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.

    def __init__(
        self, game, map, x, y, id, color, name, group,
        blocks=True, fighter=None, ai=None
    ):
        super().__init__()
        self.game = game
        self.map = map
        self.rect = pygame.Rect(x, y, TILE_W, TILE_H)
        self.id = id
        self.color = color
        if name is None:
            self.name = str(type(self))
            for trash in ["<class '", "'>", "Sprite.", "sprite."]:
                self.name = self.name.replace(trash, "")
        else:
            self.name = name
        self.blocks = blocks

        self.active = True

        self.group = group
        group.add(self)

        self.fighter = fighter
        if self.fighter:  # let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai:  # let the AI component know who owns it
            self.ai.owner = self

    @property
    def pos(self):
        return Position(self.rect.x, self.rect.y)

    @pos.setter
    def pos(self, value):
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
            return (int(self.x // n[0]), int(self.y // n[1]))
        elif isinstance(n, (int, float)):
            return (int(self.x // n), int(self.y // n))

    def move(self, pos):
        blocked, obj = self.map.is_blocked(pos, self)

        if not blocked:
            # move by the given amount
            # print(self.name, "moving")
            self.pos = pos

    def move_towards(self, target):
        start_pos = self.pos
        end_pos = target.pos

        path = self.map.map.new_path(start_pos, end_pos)

        if len(path) >= 2:
            next_step = Position(*path[1])
        else:
            # the path must be blocked
            next_step = random.choice(self.map.map.get_neighbors(start_pos))
            # print(self.name, "moves erratically")

        self.move(next_step)

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


class Player(GameObject):

    def __init__(
            self, id=ord('@'), color=GameColor.yellow, **kwargs):

        fighter_component = Fighter(
            hp=30, defense=2, power=5, death_func=Death.player)

        super().__init__(
            id=id, color=color, fighter=fighter_component, **kwargs)

    def move(self, dxy):
        super().move(self.pos + dxy)
        self.map.set_fov()

    def action(self, dx, dy):
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

        self.active = False


class Npc(GameObject):

    def update(self):
        if self.map.tiles[self.pos].visible:
            super().update()


class Orc(Npc):

    def __init__(
        self,
        id=ord('o'), color=GameColor.desaturated_green,
        **kwargs
    ):
        fighter_component = Fighter(
            hp=10, defense=0, power=3, death_func=Death.monster
        )
        ai_component = BasicMonsterAI()
        super().__init__(
            id=id, color=color,
            fighter=fighter_component,
            ai=ai_component,
            **kwargs)


class Troll(Npc):

    def __init__(
        self,
        id=ord('T'), color=GameColor.darker_green,
        **kwargs
    ):
        fighter_component = Fighter(
            hp=16, defense=1, power=4, death_func=Death.monster
        )
        ai_component = BasicMonsterAI()
        super().__init__(
            id=id, color=color,
            fighter=fighter_component,
            ai=ai_component,
            **kwargs)
