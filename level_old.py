import pygame

from game import BaseScene

from game_types import Position
import main_menu

import game_input
import sessionmgr
import sprite

from constants import SCREEN_ROWS, SCREEN_COLS, GAME_COLORS


class LevelScene(BaseScene):

    def __init__(self, game, new=True):
        self.alive = False
        self.game = game
        self.offset = Position((0, 0))
        self.scrolling = True
        self.game_state = 'loading'
        self.gfx.msg_log.clear()

        if new:
            self.new_game()
        else:
            self.load_game()

        self.alive = True
        self.game.schedule(self.scheculed_update)

        if new:
            self.gfx.msg_log.add(
                (
                    'Welcome stranger! '
                    'Prepare to perish in the Tombs of the Ancient Kings.'),
                GAME_COLORS["purple"]
            )
        else:
            self.gfx.msg_log.add(
                ('Welcome back stranger! '
                 'This time you WILL perish in the Tombs of the Ancient'
                 ' Kings!'),
                GAME_COLORS["purple"]
            )
        self.gfx.msg_log.add(
            ('You are at level {} of the dungeon.'.format(
                self.current_level)),
            GAME_COLORS["orange"]
        )
        self.game.disable_fps()
        self.on_update()

    # split input from drawing/logic
    on_key_press = game_input.on_key_press
    on_mouse_press = game_input.on_mouse_press
    on_mouse_scroll = game_input.on_mouse_scroll

    # split sessions management from drawing/logic
    new_game = sessionmgr.new_game
    new_level = sessionmgr.new_level
    load_game = sessionmgr.load_game
    set_groups = sessionmgr.set_groups
    save_game = sessionmgr.save_game

    @property
    def gfx(self):
        return self.game.gfx

    @property
    def rooms(self):
        return self.levels[self.current_level]['groups']['rooms']

    @property
    def halls(self):
        return self.levels[self.current_level]['groups']['halls']

    def rem_obj(self, obj, _type, pos):
        level_dict = self.levels[self.current_level]
        if obj in level_dict['grid'][pos][_type]:
            level_dict['grid'][pos][_type].remove(obj)
        if obj in level_dict['groups'][_type]:
            level_dict['groups'][_type].remove(obj)

    def add_obj(self, obj, _type, pos):
        level_dict = self.levels[self.current_level]
        if obj not in level_dict['grid'][pos][_type]:
            level_dict['grid'][pos][_type].append(obj)
        if obj not in level_dict['groups'][_type]:
            level_dict['groups'][_type].append(obj)

    def get_obj(self, _type, pos):
        grid = self.levels[self.current_level]['grid']

        if _type == "feature":
            return grid[pos][_type]

        for obj in grid[pos][_type]:
            return obj

        return None

    def get_all_at_pos(self, pos,
                       _types=["creatures", "objects", "feature"]):
        grid = self.levels[self.current_level]['grid']

        objects = []

        for _type in _types:
            if _type == "feature":
                objects.append(grid[pos][_type])

            for obj in grid[pos][_type]:
                objects.append(obj)

        return objects

    def get_nearest_obj(self, _type, pos, max_range=None, visible_only=True,
                        val_callback=None):
        grid = self.levels[self.current_level]['grid']
        target = None
        target_dist = None
        if visible_only:
            for y in range(SCREEN_ROWS):
                for x in range(SCREEN_COLS):
                    for obj in grid[x, y][_type]:
                        if not grid[x, y]['feature'].visible:
                            continue

                        if val_callback and not val_callback(obj):
                            continue

                        distance = self.map_mgr.distance(pos, (x, y))
                        if max_range and distance > max_range:
                            continue
                        elif target is None:
                            target = obj
                        else:
                            if distance < target_dist:
                                target = obj
        return target

    def validate_pos(self, pos):
        """Assures that the *relative* position is valid."""
        x, y = pos
        x = max(0, x)
        x = min(self.max_x - SCREEN_COLS, x)

        y = max(0, y)
        y = min(self.max_y - SCREEN_ROWS, y)

        return Position((x, y))

    def set_offset(self, object):
        """Centers the view around an object, with minor adjustments to better
        show map edges."""
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

    def new_turn(self):
        self.turn += 1
        print("Turn {}".format(self.turn))

        self.tile_fx.update()

        self.player.active = True

        level_dict = self.levels[self.current_level]
        for creature in level_dict['groups']['creatures']:
            creature.active = True

    def handle_turn(self):
        if self.alive:
            level_dict = self.levels[self.current_level]
            if self.game_state == 'playing':
                for creature in level_dict['groups']['creatures']:
                    if creature.ai and creature.active:
                        if creature.visible or creature.ai.effect:
                            old_pos = creature.get_rect
                            creature.ai.take_turn()
                            new_pos = creature.get_rect

                            self.gfx.draw(
                                creature.id,
                                (creature.x, creature.y),
                                color=creature.color)

                            pygame.display.update([old_pos, new_pos])

                        else:
                            # IDLE STEP, RANDOM CHANCE, ETC.?
                            pass
                    if creature is not self.player:
                        creature.active = False

                if not self.player.active:
                    self.on_update()
                    self.new_turn()

    def on_update(self):
        self.game.screen.fill((0, 0, 0))

        grid = self.levels[self.current_level]['grid']
        draw = self.gfx.draw
        if self.alive:
            # loop all tiles, and draw
            for y in range(SCREEN_ROWS):
                for x in range(SCREEN_COLS):
                    # draw tile at (x,y)
                    pos = self.offset + (x, y)
                    tile = grid[pos]
                    if tile["feature"].visible or tile["feature"].explored:
                        color = (self.tile_fx.get(coord=pos) or
                                 tile["feature"].color)
                        draw(tile["feature"].id, (x, y),
                             color=color,
                             tiling_index=tile["feature"].tiling_index,
                             tile_variation=tile["feature"].tile_variation)

                        mult = False
                        if len(tile["objects"]) > 1:
                            mult = True

                        for obj in tile["objects"]:
                            if isinstance(obj, sprite.DngFeature):
                                draw(obj.id, (x, y), obj.color)

                        if not tile["feature"].visible:
                            self.gfx.draw_fog((x, y))
                        else:
                            if mult:
                                draw(ord("&"), (x, y), (168, 168, 0))
                            else:
                                if tile["objects"]:
                                    obj = tile["objects"][0]
                                    draw(obj.id, (x, y), obj.color)

                            for creature in tile['creatures']:
                                draw(creature.id, (x, y),
                                     color=creature.color)

            self.gfx.draw_hud()

            if self.game_state == 'inventory':
                self.gfx.inventory.draw()
            elif self.game_state == 'choice':
                self.gfx.choice.draw()
            elif self.game_state == 'dead':
                self.gfx.msg.draw("The End?")
        elif self.game_state == 'saving':
            self.gfx.msg.draw("Saving your game (Don't panic!)")

        pygame.display.flip()

    def scheculed_update(self):
        if self.game_state not in ['playing', 'loading']:
            self.on_update()

    def choice(self, title, items, callback):
        self.gfx.choice.set_list(title, items, callback)
        self.game_state = 'choice'

    def quit(self, save=True):
        self.alive = False
        if save:
            self.save_game()
        self.game.unschedule(self.scheculed_update)
        self.game.enable_fps()
        self.game.set_scene(scene=main_menu.MainMenu)


if __name__ == '__main__':
    from game import Game
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT
    Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
