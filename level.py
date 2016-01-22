import threading

from game import BaseScene

from game_types import Position
import main_menu

import game_input
import sessionmgr

from constants import SCREEN_ROWS, SCREEN_COLS, GameColor


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

        if new:
            self.gfx.msg_log.add(
                (
                    'Welcome stranger! '
                    'Prepare to perish in the Tombs of the Ancient Kings.'),
                GameColor.purple
            )
        else:
            self.gfx.msg_log.add(
                ('Welcome back stranger! '
                 'This time you WILL perish in the Tombs of the Ancient'
                 ' Kings!'),
                GameColor.purple
            )
        self.gfx.msg_log.add(
            ('You are at level {} of the dungeon.'.format(
                self.current_level)),
            GameColor.orange
        )

    # split input from drawing/logic
    on_key_press = game_input.on_key_press
    on_mouse_press = game_input.on_mouse_press
    on_mouse_scroll = game_input.on_mouse_scroll

    # split sessions management from drawing/logic
    new_game = sessionmgr.new_game
    new_level = sessionmgr.new_level
    load_game = sessionmgr.load_game
    save_game = sessionmgr.save_game

    @property
    def gfx(self):
        return self.game.gfx

    @property
    def objects(self):
        return self.levels[self.current_level]['objects']

    @property
    def remains(self):
        return self.levels[self.current_level]['remains']

    @property
    def grid(self):
        return self.levels[self.current_level]['grid']

    @property
    def rooms(self):
        return self.levels[self.current_level]['rooms']

    @property
    def halls(self):
        return self.levels[self.current_level]['halls']

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
        self.gfx.msg_log.add("Turn {}".format(self.turn))

        self.tile_fx.update()

        self.player.active = True
        for object in self.objects:
            object.active = True

    def handle_turn(self):
        if self.alive:
            if self.game_state == 'playing':
                for object in self.objects:
                    if object.ai and object.active and (
                        object.next_to_vis or
                        self.grid[object.pos].visible or
                        object.ai.effect
                    ):
                        threading.Thread(
                            target=object.ai.take_turn).start()

                    if object is not self.player:
                        object.active = False

                if not self.player.active:
                    self.new_turn()

    def on_update(self):
        if self.alive:
            # loop all tiles, and draw
            for y in range(SCREEN_ROWS):
                for x in range(SCREEN_COLS):
                    # draw tile at (x,y)
                    pos = self.offset + (x, y)
                    tile = self.grid[pos]
                    if tile.visible:
                        if not self.remains.contain_pos(pos):
                            self.gfx.draw(
                                tile.id, (x, y),
                                color=self.tile_fx.get(coord=pos))
                    elif tile.explored:
                        self.gfx.draw(
                            tile.id, (x, y),
                            color=GameColor.darkest_grey)

            self.remains.update()
            self.objects.update()
            self.gfx.draw_hud()

            if self.game_state == 'inventory':
                self.gfx.inventory.draw()
            elif self.game_state == 'choice':
                self.gfx.choice.draw()
            elif self.game_state == 'dead':
                self.gfx.msg.draw("The End?")
        elif self.game_state == 'saving':
            self.gfx.msg.draw("Saving your game (Don't panic!)")

    def choice(self, title, items, callback):
        self.gfx.choice.set_list(title, items, callback)
        self.game_state = 'choice'

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
    Game(
        scene=LevelScene, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
