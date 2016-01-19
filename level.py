import sys
import random
import threading
import time
import traceback

import pygame
from pygame.locals import *

from game import BaseScene

from constants import SCREEN_ROWS, MAP_ROWS, SCREEN_COLS, MAP_COLS, GameColor
from constants import MAX_ROOM_MONSTERS, EXPLORE_RADIUS, FOV_RADIUS, DEBUG
from constants import TILE_W, TILE_H
from rnd_utils import RoomItems, ItemTypes
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

        self.objects = sprite.Group()
        self.remains = sprite.Group()

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
        self.tile_fx_coord = []
        self.tile_fx_color = []

        self.cursor = sprite.Cursor(game=self.game, map=self)

        self.game.gfx.msg_log.add(
            (
                'Welcome stranger! '
                'Prepare to perish in the Tombs of the Ancient Kings.'),
            GameColor.red
        )

    def new_xy(self, room, objects=None):
        attempts = 0
        while True:
            if attempts > 10:
                return None
            xy = room.random_point(map=self.tiles)
            if xy not in objects:
                return xy
            attempts += 1

    def place_objects(self):
        for room_n, room in enumerate(self.map.rooms):

            if room_n > 1:
                num_items = RoomItems.random()
                items_placed = []
                for i in range(num_items):
                    xy = self.new_xy(room, items_placed)
                    if xy is not None:
                        items_placed.append(xy)
                        x, y = xy
                        template = ItemTypes.random()
                        sprite.Item(
                            template=template,
                            game=self.game, map=self, x=x, y=y,
                            group=self.remains)
                        tmp = sprite.Item(
                            template=template,
                            game=self.game, map=self, x=x, y=y,
                            group=self.remains)
                        tmp.item.pick_up(getter=self.player)

                num_monsters = random.randint(0, MAX_ROOM_MONSTERS)
                monsters_placed = []
                for i in range(num_monsters):
                    xy = self.new_xy(room, monsters_placed)
                    if xy is not None:
                        monsters_placed.append(xy)
                        x, y = xy
                        if random.randint(0, 100) < 80:
                            template = "orc"
                        else:
                            template = "troll"
                        sprite.NPC(
                            template=template,
                            game=self.game, map=self, x=x, y=y,
                            group=self.objects)
            elif room_n == 0:
                x, y = room.random_point(map=self.tiles)

                self.player = sprite.Player(
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

            y = max(0, y)
            y = min(self.max_y - SCREEN_ROWS, y)
            return Position((x, y))

    def set_offset(self, object):
        self.offset = object.pos // 2

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
        self.game.gfx.msg_log.add("Turn {}".format(self.turn))
        self.player.active = True
        for object in self.objects:
            object.active = True
        self.tile_fx_coord = []
        self.tile_fx_color = []

    def handle_turn(self):
        # thread_handle_turn
        while True:
            self.pathing = []
            if self.game_state == 'playing':
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
                    if not self.remains.contain_pos(pos):
                        if pos in self.pathing:
                            self.game.gfx.draw(tile.id, (x, y),
                                               color=GameColor.red)
                        elif pos in self.tile_fx_coord:
                            index = self.tile_fx_coord.index(pos)
                            color = self.tile_fx_color[index]
                            self.game.gfx.draw(tile.id, (x, y),
                                               color=color)
                        else:
                            self.game.gfx.draw(tile.id, (x, y))
                elif tile.explored:
                    self.game.gfx.draw(tile.id, (x, y),
                                       color=GameColor.darkest_grey)

        self.remains.update()
        self.objects.update()
        self.game.gfx.draw_hud()
        if self.game_state == 'inventory':
            self.game.gfx.inventory.draw()

    def on_key_press(self, event):
        if self.game_state == 'playing' and self.player.active:
            if event.key == pygame.K_ESCAPE:
                self.quit()
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
            elif event.key == pygame.K_g:
                self.player.action(action='get')
            elif event.key == pygame.K_i:
                self.game.gfx.inventory.set_inventory(self.player)
                self.game_state = 'inventory'
            elif event.key == pygame.K_d:
                self.game.gfx.inventory.set_inventory(
                    self.player, mode="drop")
                self.game_state = 'inventory'
        elif self.game_state == 'inventory':
            if event.key in [pygame.K_i, pygame.K_ESCAPE]:
                self.game_state = 'playing'
                self.game.gfx.inventory.clean_inventory()

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

    def on_mouse_press(self, event):
        pos = pygame.mouse.get_pos()
        if self.game_state == 'playing' and self.player.active:
            rel_pos = (
                (pos[0] // TILE_W) + self.offset[0],
                (pos[1] // TILE_H) + self.offset[1])

            if event.button == 1:  # left button
                target = self.cursor.move(pos, rel_pos)
                self.game.gfx.msg_log.add(
                    "Clicked on {}".format(target))
            elif event.button == 3:  # right button
                target = self.cursor.move(pos, rel_pos)
                self.game.gfx.inventory.set_inventory(
                    holder=self.player,
                    target=target)
                self.game_state = 'inventory'

        elif self.game_state == 'inventory':
            if self.game.gfx.inventory.click_on(pos) in [
                'used', "dropped"
            ]:
                self.game_state = 'playing'
                self.game.gfx.inventory.clean_inventory()

    def quit(self):
        super().quit()

if __name__ == '__main__':
    from game import Game
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    game = Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
