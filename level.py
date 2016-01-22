import sys
import random
import traceback
import threading

import pygame

from game import BaseScene

from constants import SCREEN_ROWS, MAP_ROWS, SCREEN_COLS, MAP_COLS, GameColor
from constants import MAX_ROOM_MONSTERS, EXPLORE_RADIUS, FOV_RADIUS, DEBUG
from constants import TILE_W, TILE_H
from rnd_utils import RoomItems, ItemTypes, MonsterTypes
import sprite
import gamemap
import fov
from game_types import Position
import main_menu


class LevelScene(BaseScene):
    """stores map info, and draws tiles.
    Map is stored as an array of int's which correspond to the tile id."""

    def __init__(self, game, new=True):
        self.alive = False
        self.game = game
        self.screen = game.screen
        self.scrolling = True
        self.game_state = 'loading'
        self.game.gfx.msg_log.clear()

        if new:
            self.new_game()
        else:
            self.load_game()

        self.alive = True

        if new:
            self.game.gfx.msg_log.add(
                (
                    'Welcome stranger! '
                    'Prepare to perish in the Tombs of the Ancient Kings.'),
                GameColor.purple
            )
        else:
            self.game.gfx.msg_log.add(
                ('Welcome back stranger! '
                 'This time you WILL perish in the Tombs of the Ancient'
                 ' Kings!'),
                GameColor.purple
            )
        self.game.gfx.msg_log.add(
            ('You are at level {} of the dungeon.'.format(
                self.map.level)),
            GameColor.orange
        )

    def new_level(self, level=0):
        self.game_state = 'loading'
        if hasattr(self, 'map'):
            # coming from a previous level
            current_level = self.map.level

            self.objects.remove(self.player)
            self.levels[current_level] = {
                'map': self.map,
                'objects': self.objects,
                'remains': self.remains,
                'player': self.player.pos
            }

        if level in self.levels:
            # going back to a level
            self.map = self.levels[level]['map']
            self.objects = self.levels[level]['objects']
            self.remains = self.levels[level]['remains']
            self.player.pos = self.levels[level]['player']
            self.objects.add(self.player)
            self.player.group = self.objects
        else:
            # going to a new level - or the first one
            self.objects = sprite.Group()
            self.remains = sprite.Group()
            self.map = gamemap.Map(
                width=MAP_COLS, height=MAP_ROWS,
                objects=self.objects, level=level)

            self.rooms, self.halls = self.map.rooms, self.map.halls
            self.tiles = self.map.grid

            self.place_objects()

            self.set_fov()

            self.pathing = []
            self.tile_fx_coord = []
            self.tile_fx_color = []

        self.game_state = 'playing'

    def new_game(self):
        self.turn = 0

        self.levels = {}

        self.max_y = max(SCREEN_ROWS, MAP_ROWS)
        self.max_x = max(SCREEN_COLS, MAP_COLS)

        self.new_level()

        self.cursor = sprite.Cursor(game=self.game, map=self)

    def load_game(self):
        import zshelve
        import os
        with zshelve.open(os.path.join('save', 'savegame'), 'r') as shelf_file:
            self.player = shelf_file['player']

            self.objects = shelf_file['objects']
            self.objects.add(self.player)

            self.remains = shelf_file['remains']

            for att, value in shelf_file['scene'].items():
                setattr(self, att, value)

            self.levels = shelf_file['levels']

            self.map = shelf_file['map']
            self.rooms, self.halls = self.map.rooms, self.map.halls
            self.tiles = self.map.grid

            for group in [self.objects, self.remains]:
                for obj in group:
                    obj.game = self.game
                    obj.map = self
                    obj.group = group

            self.set_fov()

            self.pathing = []
            self.tile_fx_coord = []
            self.tile_fx_color = []

            self.cursor = shelf_file['cursor']
            self.cursor.game = self.game
            self.cursor.map = self

            self.game_state = 'playing'

    def save_game(self):
        self.game_state = 'saving'
        import zshelve
        import os

        with zshelve.open(os.path.join('save', 'savegame'), 'n') as shelf_file:
            shelf_file['player'] = self.player

            self.objects.remove(self.player)
            shelf_file['objects'] = self.objects

            shelf_file['remains'] = self.remains

            scene = {}
            for att in ['turn', "max_y", "max_x", "offset"]:
                scene[att] = getattr(self, att)
            shelf_file['scene'] = scene

            shelf_file['map'] = self.map

            shelf_file['levels'] = self.levels

            self.tile_fx_coord = []
            self.tile_fx_color = []

            shelf_file['cursor'] = self.cursor

            if False:
                for key, value in shelf_file.items():
                    print("key: {}, value: {}".format(key, value))

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
                        template = MonsterTypes.random()
                        sprite.NPC(
                            template=template,
                            game=self.game, map=self, x=x, y=y,
                            group=self.objects)
                if room_n == len(self.map.rooms) - 1:
                    pass

            elif room_n == 0:
                x, y = room.random_point(map=self.tiles)
                if hasattr(self, 'player'):
                    self.player.pos = (x, y)
                    self.objects.add(self.player)
                    self.player.group = self.objects
                else:
                    self.player = sprite.Player(
                        name=None,
                        game=self.game, map=self, x=x, y=y,
                        group=self.objects)

                x, y = self.new_xy(room, [self.player.pos])
                template = "stair_down"
                sprite.DngFeature(
                    template=template,
                    game=self.game, map=self, x=x, y=y,
                    group=self.remains)

                x, y = self.new_xy(room, [self.player.pos, (x, y)])

                sprite.Item(
                    template=random.choice(['dagger', 'shield']),
                    game=self.game, map=self, x=x, y=y,
                    group=self.remains)

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
        x, y = object.pos // 2
        if x > SCREEN_COLS // 4 * 3:
            x += 2
        elif x < SCREEN_COLS // 4:
            x -= 2
        if y > SCREEN_ROWS // 4 * 3:
            y += 2
        elif y < SCREEN_ROWS // 4:
            y -= 2

        self.offset = self.validate_pos((x, y))

    def scroll(self, rel):
        """scroll map using relative coordinates"""
        if not self.scrolling:
            return

        x, y = [self.offset[0] + rel[0], self.offset[1] + rel[1]]

        self.offset = self.validate_pos((x, y))

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
        """
        if self.alive:
            if self.game_state == 'playing':
                self.pathing = []
                for object in self.objects:
                    if object.ai and object.active:
                        if hasattr(object.ai, "num_turns"):
                            # keep counting, under some effect (confused, etc.)
                            self.activate_monster
                        elif (object.next_to_vis or
                              self.tiles[object.pos].visible):
                            self.activate_monster

                    # make inactive for this turn, acting or not
                    if object is not self.player:
                        object.active = False

                if not self.player.active:
                    self.new_turn()
        """
        # thread_handle_turn
        if self.alive:
            self.pathing = []
            if self.game_state == 'playing':
                for object in self.objects:

                    if object.ai and object.active and (
                        object.next_to_vis or
                        self.tiles[object.pos].visible or
                        object.ai.effect
                    ):
                        threading.Thread(
                            target=object.ai.take_turn).start()
                    if object is not self.player:
                        object.active = False

                if not self.player.active:
                    self.new_turn()
            # time.sleep(0.1)

    def on_update(self):
        if self.alive:
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
                                path_len = len(self.pathing)
                                if path_len < 2:
                                    path_color = GameColor.red
                                elif path_len < 4:
                                    path_color = GameColor.orange
                                else:
                                    path_color = GameColor.yellow
                                self.game.gfx.draw(tile.id, (x, y),
                                                   color=path_color)
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
            elif self.game_state == 'choice':
                self.game.gfx.choice.draw()
            elif self.game_state == 'dead':
                self.game.gfx.msg.draw("The End?")
        elif self.game_state == 'saving':
            self.game.gfx.msg.draw("Saving your game (Don't panic!)")

    def on_key_press(self, event):
        if self.game_state == 'playing' and self.player.active:
            if event.key == pygame.K_ESCAPE:
                self.quit()

            elif event.key in [pygame.K_KP7]:
                self.player.action(-1, -1)
            elif event.key in [pygame.K_UP, pygame.K_KP8]:
                self.player.action(0, -1)
            elif event.key in [pygame.K_KP9]:
                self.player.action(1, -1)
            elif event.key in [pygame.K_RIGHT, pygame.K_KP6]:
                self.player.action(1, 0)
            elif event.key in [pygame.K_KP3]:
                self.player.action(1, 1)
            elif event.key in [pygame.K_DOWN, pygame.K_KP2]:
                self.player.action(0, 1)
            elif event.key in [pygame.K_KP1]:
                self.player.action(-1, 1)
            elif event.key in [pygame.K_LEFT, pygame.K_KP4]:
                self.player.action(-1, 0)

            elif event.key in [pygame.K_SPACE, pygame.K_KP5]:
                self.player.action()

            elif event.key == pygame.K_g:
                self.player.action(action='get')
            elif event.key == pygame.K_u:
                if self.player.action(action='use'):
                    return
            elif event.key == pygame.K_i:
                self.game.gfx.inventory.set_inventory(self.player)
                self.game_state = 'inventory'
            elif event.key == pygame.K_d:
                self.game.gfx.inventory.set_inventory(
                    self.player, mode="drop")
                self.game_state = 'inventory'

            elif event.key == pygame.K_k:
                self.player.fighter.take_damage(999999, "user")

            elif event.key == pygame.K_s:
                self.game.gfx.msg_log.add(
                    "Power {}, Defense {}".format(
                        self.player.fighter.power, self.player.fighter.defense
                    ), GameColor.azure)

        elif self.game_state == 'inventory':
            if event.key in [pygame.K_i, pygame.K_ESCAPE]:
                self.game_state = 'playing'
                self.game.gfx.inventory.clean_inventory()
                return
        elif self.game_state == 'choice':
            if event.key == pygame.K_ESCAPE:
                pass
                # self.game_state = 'playing'
                # self.game.gfx.choice.clear()
            elif event.key == pygame.K_UP:
                self.game.gfx.choice.change_selection(-1)
            elif event.key == pygame.K_DOWN:
                self.game.gfx.choice.change_selection(+1)
            elif event.key == pygame.K_RETURN:
                self.game.gfx.choice.confirm()
                self.game_state = 'playing'
                self.game.gfx.choice.clear()

        elif self.game_state == 'dead':
            self.quit(save=False)

        self.handle_turn()

    def choice(self, title, items, callback):
        self.game.gfx.choice.set_list(title, items, callback)
        self.game_state = 'choice'

    def on_mouse_scroll(self, event):
        if self.game_state == 'playing':
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
            result = self.game.gfx.inventory.click_on(pos)
            if result in ['used', "dropped"]:
                self.game_state = 'playing'
                self.game.gfx.inventory.clean_inventory()
                self.player.action()

        self.handle_turn()

    def quit(self, save=True):
        threading.Thread(target=self._quit, args=([save])).start()

    def _quit(self, save):
        self.alive = False
        if save:
            self.save_game()
        self.game.set_scene(scene=main_menu.MainMenu)

if __name__ == '__main__':
    from game import Game
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    game = Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
