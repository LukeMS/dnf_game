"""..."""
import pygame

from manager import Game
from manager.scenes import base_scenes
from manager.windows import base_windows


class TestMenuLayer(base_windows.Menu):

    def on_update(self):
        """..."""
        # print(self.__class__.__name__ + '.on_update called')
        super().on_update()


class TestMenuScene(base_scenes.SceneMultiLayer):

    def __init__(self):
        """..."""
        super().__init__()
        self.insert_layer(TestMenuLayer(
            parent=self, title="Test Menu",
            items=["Test Item"]))

    def on_update(self):
        """..."""
        # print(self.__class__.__name__ + '.on_update called')
        super().on_update()

    def on_key_press(self, event):
        """..."""
        if event.key == pygame.K_ESCAPE:
            self.quit()
        if event.key == pygame.K_UP:
            self.change_selection(-1)
        elif event.key == pygame.K_DOWN:
            self.change_selection(+1)
        elif event.key == pygame.K_RETURN:
            self.game.set_scene(**self._menu[self.selection]['kwargs'])

if __name__ == '__main__':

    g = Game(scene=TestMenuScene)
    """
    exit()
    g.set_scene(base_scenes.SceneMultiLayer)
    scene = g._scene
    print(scene)
    g._scene.insert_layer(base_windows.Menu(
        parent=g._scene, title="Test Menu",
        items=["Test Item"]))
    msg = base_windows.Msg(parent=g._scene)
    g.execute()
    """
