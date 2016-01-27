import pygame
import constants


"""
    on_key_press
    on_mouse_press
    on_mouse_scroll

Those are actual methods of the LevelScene class.
They should be properly splitted apart from it soon, possibly using an event
dispatcher.
For now, they're only phisically stored apart to keep things "organized".
"""


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
            if not self.player.action(action='get'):
                return
        elif event.key == pygame.K_u:
            if not self.player.action(action='use'):
                return
        elif event.key == pygame.K_i:
            self.gfx.inventory.set_inventory(self.player)
            self.game_state = 'inventory'
        elif event.key == pygame.K_d:
            self.gfx.inventory.set_inventory(
                self.player, mode="drop")
            self.game_state = 'inventory'

        elif event.key == pygame.K_k:
            self.player.fighter.take_damage(999999, "user")

        elif event.key == pygame.K_s:
            self.gfx.msg_log.add(
                "Power {}, Defense {}".format(
                    self.player.fighter.power, self.player.fighter.defense
                ), GameColor.azure)

    elif self.game_state == 'inventory':
        if event.key in [pygame.K_i, pygame.K_ESCAPE]:
            self.game_state = 'playing'
            self.gfx.inventory.clean_inventory()
            return
    elif self.game_state == 'choice':
        if event.key == pygame.K_ESCAPE:
            pass
            # self.game_state = 'playing'
            # self.gfx.choice.clear()
        elif event.key == pygame.K_UP:
            self.gfx.choice.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.gfx.choice.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            self.gfx.choice.confirm()
            self.game_state = 'playing'
            self.gfx.choice.clear()

    elif self.game_state == 'dead':
        if event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
            self.quit(save=False)

    self.handle_turn()


def on_mouse_press(self, event):
    pos = pygame.mouse.get_pos()
    if self.game_state == 'playing' and self.player.active:
        rel_pos = (
            (pos[0] // constants.TILE_W) + self.offset[0],
            (pos[1] // constants.TILE_H) + self.offset[1])

        if event.button == 1:  # left button
            target = self.cursor.move(pos, rel_pos)
            self.gfx.msg_log.add(
                "Clicked on {}".format(target))
        elif event.button == 3:  # right button
            target = self.cursor.move(pos, rel_pos)
            # area = self.map_mgr.get_line(target.pos, self.player.pos)
            area = self.map_mgr.get_octant(
                self.player.pos, 4,
                self.turn)
            self.tile_fx.add(area, constants.GameColor.blue, 1)
            self.player.action()
            """
            self.gfx.inventory.set_inventory(
                holder=self.player,
                target=target)
            self.game_state = 'inventory'
            """

    elif self.game_state == 'inventory':
        result = self.gfx.inventory.click_on(pos)
        if result in ['used', "dropped"]:
            self.game_state = 'playing'
            self.gfx.inventory.clean_inventory()
            self.player.action()

    self.handle_turn()


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
