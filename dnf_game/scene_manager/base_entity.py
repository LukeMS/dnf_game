"""..."""

from dnf_game.util import SingletonMeta
from dnf_game.util.ext.docstring_inheritor import DocStringInheritor


class ManagerObjectMeta(metaclass=DocStringInheritor):
    """The most abstract object in the game.

    Both EntityBase and the Manager (indirectly) itself share this metaclass
    """

    def __init__(self, **kwargs):
        """Initialization."""

    @property
    def fonts(self):
        """Reference to FontsManager instance.

        dnf_game.scene_manager.resources.FontsManager
        """
        pass

    @property
    def factory(self):
        """Reference to SpriteFactory instance.

        dnf_game.scene_manager.SpriteFactory
        """
        pass

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        pass

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        pass

    def on_mouse_drag(self, x, y, dx, dy, button):
        """Called when mouse buttons are pressed and the mouse is dragged."""
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved."""
        pass

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed."""
        pass

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        pass

    def on_update(self):
        """Graphical logic."""
        pass


class ManagerSingletonMeta(SingletonMeta, ManagerObjectMeta):
    """Singleton Meta."""


class EntityBase(ManagerObjectMeta):
    """Abstract entity inherited from both SceneBase an WindowBase."""

    @property
    def fonts(self):
        """super__doc__."""
        return self.manager.fonts

    @property
    def factory(self):
        """super__doc__."""
        return self.manager.factory

    @property
    def renderer(self):
        """super__doc__."""
        return self.manager.renderer

    @property
    def sdlrenderer(self):
        """super__doc__."""
        return self.manager.renderer.sdlrenderer

    def clear(self):
        """Clear the entity."""
        pass

    def post_update(self):
        """PendingDeprecation: post update update?."""
        raise PendingDeprecationWarning("%s.post_update" %
                                        self.__class__.__name__)

    def start(self):
        """PendingDeprecation: post __init__ init?."""
        raise PendingDeprecationWarning("%s.start" %
                                        self.__class__.__name__)

    def __repr__(self):
        """Official string representation of the object."""
        return "%s()" % self.__class__.__name__

    def __getstate__(self):
        """Prevent pickling by returning None."""
        return None


class MultiLayeredEntityBase(EntityBase):
    """Abstract for entities with their own child entities (e.g.:layers)."""

    def __init__(self, *, draw_all=False, **kwargs):
        """super__doc__."""
        self.draw_all = draw_all
        self.layers = []

    def clear(self):
        """Clear the entity and its children."""
        [layer.clear() for layer in self.layers]

    def insert_layer(self, *args):
        """Insert one or more layers in the entity layers container."""
        self.layers.extend(args)

    def remove_layer(self, obj):
        """Remove a layer from entity layers container."""
        self.layers.remove(obj)

    def dispatch_event(
        self, event_name, validator, *, iterator=None, interrupt=True,
        **kwargs
    ):
        """Dispatch the event to the entities on the iterator.

        Args:
            event_name (str): the name of the method that handles those events
            (e.g. event_name="on_update").
            validator (attribute): the event will only be dispatched to the
            entities on which this evaluates to True.
            iterator (iterable): a iterable or container with entities that
            should receive the event. Defaults to self.layers (the container
            that hold this entity's children.
            kwargs: additional keyword arguments that should be passed down to
            the entities.
        """
        iterator = iterator or self.layers
        for obj in iterator:
            if getattr(obj, validator, None):
                fb = getattr(obj, event_name)(**kwargs)
                try:
                    if interrupt and fb.handled:
                        return fb
                except AttributeError:
                    # without a clear sign to halt, the iteration goes on
                    continue

    def on_key_press(self, **kwargs):
        """super__doc__."""
        return self.dispatch_event("on_key_press", "active", **kwargs)

    def on_key_release(self, **kwargs):
        """super__doc__."""
        return self.dispatch_event("on_key_release", "active", **kwargs)

    def on_mouse_drag(self, **kwargs):
        """super__doc__."""
        return self.dispatch_event("on_mouse_drag", "active", **kwargs)

    def on_mouse_motion(self, **kwargs):
        """super__doc__."""
        return self.dispatch_event("on_mouse_motion", "active", **kwargs)

    def on_mouse_press(self, **kwargs):
        """super__doc__."""
        return self.dispatch_event("on_mouse_press", "active", **kwargs)

    def on_mouse_scroll(self, **kwargs):
        """super__doc__."""
        return self.dispatch_event("on_mouse_scroll", "active", **kwargs)

    def on_update(self):
        """super__doc__."""
        if not getattr(self, "draw_all", None):
            return self.dispatch_event("on_update", "visible",
                                       iterator=(self.layers[-1:]))
        else:
            return self.dispatch_event("on_update", "visible",
                                       interrupt=False)

    def post_update(self):
        """super__doc__."""
        if not getattr(self, "draw_all", None):
            return self.dispatch_event("post_update", "visible",
                                       iterator=(self.layers[-1:]))
        else:
            return self.dispatch_event("post_update", "visible",
                                       interrupt=False)
