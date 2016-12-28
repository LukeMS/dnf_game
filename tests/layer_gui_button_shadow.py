"""Button example use.

SDL_Texture* target_tex =SDL_CreateTexture(.....); //Add arg according to you
SDL_SetRenderTarget(my_renderer, target_tex);

SDL_Texture* t1 = SDL_CreateTextureFromSurface(my_renderer, someSurface);
SDL_Texture* t2 = SDL_CreateTextureFromSurface(my_renderer, someOtherSurface);
.
.
.
.
SDL_RenderCopy(my_renderer, t1, NULL, NULL);
SDL_RenderCopy(my_renderer, t2, NULL, NULL);
SDL_RenderCopy(my_renderer, t3, NULL, NULL);
.
.
.
SDL_SetRenderTarget(my_renderer, NULL);
SDL_RendererPresent(my_renderer);


SDL_RenderClear(my_renderer);
SDL_RenderCopy(my_renderer, target_tex, NULL, NULL);
SDL_RendererPresent(my_renderer);
"""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.scene_manager.layers import base_layers
from dnf_game.scene_manager.layers import gui_layer


class LayerGuiButtonTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneLayerGuiButtonTest, test=False).execute()


class SceneLayerGuiButtonTest(base_scenes.SceneMultiLayer):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        frame = base_layers.Layer(parent=self, rect=(0, 0, 205, 125))
        frame.create_gradient_surface()
        gui = gui_layer.GUILayer(parent=self)
        gui.create_button(rect=(50, 50, 105, 25),
                          command=self.quit,
                          radius=10,
                          regular_text='Quit')
        self.insert_layer(frame, gui)


if __name__ == '__main__':
    unittest.main(verbosity=2)
