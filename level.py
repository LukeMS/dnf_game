import sys
import random
import threading
import time
import traceback

import pygame
from pygame.locals import *

from game import Game, BaseScene

from constants import SCREEN_ROWS, MAP_ROWS, SCREEN_COLS, MAP_COLS, GameColor
from constants import MAX_ROOM_MONSTERS, EXPLORE_RADIUS, FOV_RADIUS, DEBUG
import sprite
# import rnd_gen
import gamemap
import fov
from game_types import Position


class LevelScene(BaseScene):
    """stores map info, and draws tiles.
    Map is stored as an array of int's which correspond to the tile id."""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.scrolling = True
        self.game_state = 'playing'
        self.turn = 0
        self.player_acted = False

        self.objects = pygame.sprite.Group()
        self.remains = pygame.sprite.Group()

        self.max_y = max(SCREEN_ROWS, MAP_ROWS)
        self.max_x = max(SCREEN_COLS, MAP_COLS)
        self.map = gamemap.Map(
            width=MAP_COLS, height=MAP_ROWS,
            objects=self.objects)
        self.rooms, self.halls = self.map.rooms, self.map.halls
        self.tiles = self.map.grid

        self.place_objects()

        self.set_offset(self.player)
        # print(self.player.pos, self.offset)

        self.set_fov()

        self.thread_handle_turn = threading.Thread(
            target=self.handle_turn, daemon=True)
        self.thread_handle_turn.start()

        self.pathing = []

    def place_objects(self):
        x, y = self.map.rooms[0].random_point(map=self.tiles)

        self.player = sprite.Player(
            name=None,
            game=self.game, map=self, x=x, y=y,
            group=self.objects)

        for room in self.map.rooms[2:]:
            # choose random number of monsters
            num_monsters = random.randint(0, MAX_ROOM_MONSTERS)

            for i in range(num_monsters):
                # choose random spot for this monster
                x, y = room.random_point(map=self.tiles)
                attempts = 1
                while self.is_blocked((x, y)):
                    x, y = room.random_point(map=self.tiles)
                    attempts += 1
                    if attempts > 3:
                        break

                # 80% chance of getting an orc
                if random.randint(0, 100) < 80:
                    # create an orc
                    sprite.Orc(
                        name=None,
                        game=self.game, map=self, x=x, y=y,
                        group=self.objects)
                else:
                    # create a troll
                    sprite.Troll(
                        name=None,
                        game=self.game, map=self, x=x, y=y,
                        group=self.objects)

    def is_blocked(self, pos, sprite=None):
        # first test the map tile
        try:
            if self.tiles[pos].block_mov:
                return True, self.tiles[pos]
        except KeyError:
            return True, None

        # now check for any blocking objects
        for object in self.objects:
            if object == sprite:
                continue
            elif object.blocks and object.pos == pos:
                return True, object

        return False, None

    def validate_pos(self, pos, mode='screen'):
        if mode == 'screen':
            x, y = pos
            x = max(0, x)
            x = min(self.max_x - SCREEN_COLS, x)

            x = max(0, y)
            x = min(self.max_y - SCREEN_ROWS, y)
            return Position((x, y))

    def set_offset(self, object):
        self.offset = object // 2

    def scroll(self, rel):
        """scroll map using relative coordinates"""
        if not self.scrolling:
            return

        x, y = [self.offset[0] + rel[0], self.offset[1] + rel[1]]

        x = max(0, x)
        x = min(self.max_x - SCREEN_COLS, x)

        y = max(0, y)
        y = min(self.max_y - SCREEN_ROWS, y)

        self.offset = Position(x, y)

        if DEBUG:
            print((self.offset))

    def set_fov(self):
        self.set_offset(self.player)
        for y in range(SCREEN_ROWS):
            for x in range(SCREEN_COLS):
                # draw tile at (x,y)
                tile = self.tiles[self.offset + (x, y)]
                tile.visible = False

        fov.fieldOfView(self.player.x, self.player.y,
                        MAP_COLS, MAP_ROWS, EXPLORE_RADIUS,
                        self.func_explored, self.blocks_sight)

        fov.fieldOfView(self.player.x, self.player.y,
                        MAP_COLS, MAP_ROWS, FOV_RADIUS,
                        self.func_visible, self.blocks_sight)

    def func_explored(self, x, y):
        self.tiles[x, y].explored = True

    def func_visible(self, x, y):
        self.tiles[x, y].visible = True

    def blocks_sight(self, x, y):
        return self.tiles[x, y].block_sight

    def new_turn(self):
        self.turn += 1
        print("Turn {}".format(self.turn))
        self.player.active = True
        for object in self.objects:
                object.active = True

    def handle_turn(self):
        # thread_handle_turn
        while True:
            if self.game_state == 'playing':
                self.pathing = []
                for object in self.objects:
                    if (
                        object.ai and object.active and
                        (object.next_to_vis or self.tiles[object.pos].visible)
                    ):
                        object.ai.take_turn()
                        time.sleep(0.1)
                    if object is not self.player:
                        object.active = False

                if not self.player.active:
                    self.new_turn()
            time.sleep(0.2)

    def on_update(self):
        # loop all tiles, and draw
        for y in range(SCREEN_ROWS):
            for x in range(SCREEN_COLS):
                # draw tile at (x,y)
                try:
                    pos = self.offset + (x, y)
                    tile = self.tiles[pos]
                except KeyError:
                    print("(x, y)", (x, y))
                    print("self.offset", self.offset)
                    print("pos", pos)
                    print(traceback.format_exc())
                    sys.exit(-1)
                if tile.visible:
                    if pos not in self.remains:
                        if pos in self.pathing:
                            self.game.gfx.draw(tile.id, (x, y),
                                               color=GameColor.red)
                        else:
                            self.game.gfx.draw(tile.id, (x, y))
                elif tile.explored:
                    self.game.gfx.draw(tile.id, (x, y),
                                       color=GameColor.darkest_grey)

        self.remains.update()
        self.objects.update()
        # self.handle_turn()
        self.game.gfx.hud.text = "HP: {}".format(self.player.fighter.hp)
        self.game.gfx.hud.draw()

    def on_key_press(self, event):
        if self.game_state == 'playing' and self.player.active:
            if event.key == pygame.K_UP:
                self.player.action(0, -1)
            elif event.key == pygame.K_DOWN:
                self.player.action(0, 1)
            elif event.key == pygame.K_LEFT:
                self.player.action(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.player.action(1, 0)
            elif event.key == pygame.K_SPACE:
                self.player.action()

    def on_mouse_scroll(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            ctrl = True
        else:
            ctrl = False
        if event.button == 4:
            if ctrl:
                self.scroll((-1, 0))
            else:
                self.scroll((0, -1))
        elif event.button == 5:
            if ctrl:
                self.scroll((1, 0))
            else:
                self.scroll((0, 1))

    def quit(self):
        # threading.Thread.
        # self.thread_handle_turn
        pass

if __name__ == '__main__':
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    game = Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
        show_fps=False)
