"""..."""

import pygame

import game


class TextLayer(game.Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        self.parent = parent

    def transition(self, msg):
        """..."""
        self.set_text(msg)
        self.on_update()

    def set_text(self, text):
        """..."""
        self.text = text

    def on_update(self):
        """..."""
        self.screen.fill((0, 0, 0))
        self.gfx.msg.draw(self.text)
        pygame.display.flip()


class ChoiceLayer(game.Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        self.parent = parent
        self.active = False

    def choice(self, title, items, callback):
        """..."""
        self.gfx.choice.set_list(title, items, callback)
        self.active = True

    def on_update(self):
        """..."""
        if self.active:
            self.gfx.choice.draw()

    def on_key_press(self, event):
        """..."""
        if self.active:
            if event.key == pygame.K_UP:
                self.gfx.choice.change_selection(-1)
            elif event.key == pygame.K_DOWN:
                self.gfx.choice.change_selection(+1)
            elif event.key == pygame.K_RETURN:
                self.gfx.choice.confirm()
                self.active = False
                self.gfx.choice.clear()

            return True


class InventoryLayer(game.Layer):
    """..."""

    def __init__(self, parent):
        """..."""
        self.parent = parent
        self.active = False

    def on_update(self):
        """..."""
        if self.active:
            self.gfx.inventory.draw()

    def on_key_press(self, event):
        """..."""
        parent = self.parent

        if not self.active:
            if event.key == pygame.K_i:
                self.gfx.inventory.set_inventory(parent.player)
                self.active = True
                return True
            elif event.key == pygame.K_d:
                self.gfx.inventory.set_inventory(
                    parent.player, mode="drop")
                self.active = True
                return True
        elif self.active:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.active = False
                self.gfx.inventory.clean_inventory()
                parent.on_update()
                return True

    def on_mouse_press(self, event):
        """Handle mouse press input."""
        parent = self.parent
        pos = event.pos
        level = parent.level_layer
        rel_pos = level.cursor_rel_pos(pos=pos)

        if not self.active and parent.player.active:
            if event.button == 3:  # right button
                target = level.cursor.move(pos, rel_pos)

                parent.gfx.inventory.set_inventory(
                    holder=level.player,
                    target=target)
                self.active = True
                return True
        elif self.active:
            result = parent.gfx.inventory.click_on(pos)
            if result in ['used', "dropped"]:
                self.active = False
                parent.gfx.inventory.clean_inventory()
                level.player.action()
                return True
            elif result in ['equipped', 'cancelled']:
                return True
