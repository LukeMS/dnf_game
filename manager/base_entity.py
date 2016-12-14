"""..."""

from abc import ABCMeta, abstractmethod


class EntityBase(metaclass=ABCMeta):
    """Abstract entity inherited from both SceneBase an WindowBase."""

    @abstractmethod
    def __init__(self, **kwargs):
        """..."""
        pass
