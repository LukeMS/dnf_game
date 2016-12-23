"""..."""

from dnf_game.data.templates import get_templates


class TemplateableObject:
    """..."""

    cache = {}

    @classmethod
    def get_templates(cls, name):
        """..."""
        try:
            templates = cls.cache[name]
        except KeyError:
            templates = TemplateHandler().get(name)
            cls.cache[name] = templates
        return templates.copy()


class TemplateHandler:
    """..."""

    cache = None

    def __new__(cls, **kwargs):
        """Create a new instance TemplateHandler.

        Before the first instance is created the templates are cached to avoid
        expensive future redundant calls.
        """
        th = super().__new__(cls)
        if cls.cache is None:
            print("(%s: caching templates...)" % cls.__name__)
            cls.cache = get_templates()
        return th

    @classmethod
    def get(cls, name):
        """..."""
        all_templates = cls.cache

        templates = {}
        for group_k, group_v in all_templates.items():
            for temp_k, temp_v in group_v.items():
                if temp_k == name:
                    template = group_v["_default"]
                    if "base_item" in temp_v:
                        base_name = temp_v["base_item"]
                        base_item = group_v[base_name]
                        template = {**template, **base_item}
                    template = {**template, **temp_v}
                    templates[group_k] = template
                    break
        return templates
