"""Input handling for the level scene."""
import pygame
import constants
from common import debug_status


def on_key_press(level, event):
    """Handle key presses input for the level scene."""
    if level.game_state == 'playing' and level.player.active:
        if event.key == pygame.K_ESCAPE:
            level.quit()

        elif event.key in [pygame.K_KP7]:
            level.player.action(-1, -1)
        elif event.key in [pygame.K_UP, pygame.K_KP8]:
            level.player.action(0, -1)
        elif event.key in [pygame.K_KP9]:
            level.player.action(1, -1)
        elif event.key in [pygame.K_RIGHT, pygame.K_KP6]:
            level.player.action(1, 0)
        elif event.key in [pygame.K_KP3]:
            level.player.action(1, 1)
        elif event.key in [pygame.K_DOWN, pygame.K_KP2]:
            level.player.action(0, 1)
        elif event.key in [pygame.K_KP1]:
            level.player.action(-1, 1)
        elif event.key in [pygame.K_LEFT, pygame.K_KP4]:
            level.player.action(-1, 0)

        # skip a turn
        elif event.key in [pygame.K_SPACE, pygame.K_KP5]:
            level.player.action()

        elif event.key == pygame.K_g:
            if not level.player.action(action='get'):
                pos = level.player.pos
                scr_pos = level.player.pos - level.offset
                level.update_pos(pos, scr_pos)
                level.on_update()
                return
        elif event.key == pygame.K_u:
            if not level.player.action(action='use'):
                pos = level.player.pos
                scr_pos = level.player.pos - level.offset
                level.update_pos(pos, scr_pos)
                return
        elif event.key == pygame.K_i:
            level.gfx.inventory.set_inventory(level.player)
            level.game_state = 'inventory'
        elif event.key == pygame.K_d:
            level.gfx.inventory.set_inventory(
                level.player, mode="drop")
            level.game_state = 'inventory'

        elif event.key == pygame.K_k:
            level.player.combat.receive_dmg(999999, "user")
        elif event.key == pygame.K_s:
            # TODO: use in-game ui
            debug_status.view(creature=level.player.combat)
            return

    elif level.game_state == 'inventory':
        if event.key in [pygame.K_i, pygame.K_ESCAPE]:
            level.game_state = 'playing'
            level.gfx.inventory.clean_inventory()
            level.on_update()
            return
    elif level.game_state == 'choice':
        if event.key == pygame.K_ESCAPE:
            pass
            # level.game_state = 'playing'
            # level.gfx.choice.clear()
        elif event.key == pygame.K_UP:
            level.gfx.choice.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            level.gfx.choice.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            level.gfx.choice.confirm()
            level.game_state = 'playing'
            level.gfx.choice.clear()

    elif level.game_state == 'dead':
        if event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
            level.quit(save=False)

    level.handle_turn()


def on_mouse_press(level, event):
    """Handle mouse press input for the level scene."""
    pos = pygame.mouse.get_pos()
    rel_pos = (
        (pos[0] // constants.TILE_W) + level.offset[0],
        (pos[1] // constants.TILE_H) + level.offset[1])

    if level.game_state == 'playing' or level.game_state == 'dead':
        if event.button == 1:  # left button
            target = level.cursor.move(pos, rel_pos)
            combat = getattr(target, 'combat', None)
            debug_status.view(creature=combat or target)
            return

    if level.game_state == 'playing' and level.player.active:
        if event.button == 3:  # right button
            target = level.cursor.move(pos, rel_pos)

            """
            # area = level.map_mgr.get_line(target.pos, level.player.pos)
            area = level.map_mgr.get_octant(
                level.player.pos, 4,
                level.turn)
            level.tile_fx.add(area, constants.GAME_COLORS["blue"], 1)
            level.player.action()
            """
            level.gfx.inventory.set_inventory(
                holder=level.player,
                target=target)
            level.game_state = 'inventory'

    elif level.game_state == 'inventory':
        result = level.gfx.inventory.click_on(pos)
        if result in ['used', "dropped"]:
            level.game_state = 'playing'
            level.gfx.inventory.clean_inventory()
            level.player.action()

    level.handle_turn()


def on_mouse_scroll(level, event):
    """Handle mouse scroll input for the level scene."""
    if level.game_state == 'playing':
        keys = pygame.key.get_pressed()

        ctrl = keys[pygame.K_LCTRL]

        if event.button == 4:
            if ctrl:
                level.scroll((-1, 0))
            else:
                level.scroll((0, -1))
        elif event.button == 5:
            if ctrl:
                level.scroll((1, 0))
            else:
                level.scroll((0, 1))
    level.on_update()
