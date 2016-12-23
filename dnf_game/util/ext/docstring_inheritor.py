"""DocStringInheritor.

Based on those implementations:

    http://stackoverflow.com/a/8101598/5496529
        by Raymond Hettinger

    http://stackoverflow.com/a/38602787/5496529
        by unutbu

Code from stackoverflow is considered to be under the MIT license:
    https://opensource.org/licenses/MIT
"""


CONDITIONS = ("""super__doc__.""")


def conditions(doc):
    """Check if the docstring is empty or fit any of the CONDITIONS.

    Returns:
        bool
    """
    return (not doc or
            any(doc == condition for condition in CONDITIONS))


class DocStringInheritor(type):
    """DocStringInheritor metaclass.

    1. It inherits a parent member's docstring if the child member's
    docstring is fits conditions.
    2. It inherits a parent class docstring if the child class docstring fits
    conditions.
    3. It can inherit the docstring from any class in any of the base
    classes's MROs, just like regular attribute inheritance.
    4. Unlike with a class decorator, the metaclass is inherited, so you only
    need to set the metaclass once in some top-level base class, and
    docstring inheritance will occur throughout your OOP hierarchy.
    """

    def __new__(cls, name, bases, clsdict):
        """..."""
        if not clsdict.get('__doc__', None):
            for mro_cls in (mro_cls for base in bases
                            for mro_cls in base.mro()):
                doc = mro_cls.__doc__
                if doc:
                    clsdict['__doc__'] = doc
                    break
        for attr, attribute in clsdict.items():
            if conditions(attribute.__doc__):
                for mro_cls in (mro_cls for base in bases
                                for mro_cls in base.mro()
                                if hasattr(mro_cls, attr)
                                ):
                    doc = getattr(getattr(mro_cls, attr), '__doc__')
                    if doc:
                        if isinstance(attribute, property):
                            clsdict[attr] = property(attribute.fget,
                                                     attribute.fset,
                                                     attribute.fdel, doc)
                        else:
                            attribute.__doc__ = doc
                        break
        return type.__new__(cls, name, bases, clsdict)


if __name__ == '__main__':
    import unittest
    import sys

    class Test(unittest.TestCase):

        def test_null(self):
            class Foo(object):

                def frobnicate(self): pass

            class Bar(Foo, metaclass=DocStringInheritor):
                pass

            self.assertEqual(Bar.__doc__, object.__doc__)
            self.assertEqual(Bar().__doc__, object.__doc__)
            self.assertEqual(Bar.frobnicate.__doc__, None)

        def test_inherit_from_parent(self):
            class Foo(object):
                'Foo'

                def frobnicate(self):
                    'Frobnicate this gonk.'
            class Bar(Foo, metaclass=DocStringInheritor):
                pass

                def frobnicate(self):
                    """super__doc__."""

            self.assertEqual(Foo.__doc__, 'Foo')
            self.assertEqual(Foo().__doc__, 'Foo')
            self.assertEqual(Bar.__doc__, 'Foo')
            self.assertEqual(Bar().__doc__, 'Foo')
            self.assertEqual(Bar.frobnicate.__doc__, 'Frobnicate this gonk.')

        def test_inherit_from_mro(self):
            class Foo(object):
                'Foo'

                def frobnicate(self):
                    'Frobnicate this gonk.'
            class Bar(Foo):
                pass

            class Baz(Bar, metaclass=DocStringInheritor):
                pass

            self.assertEqual(Baz.__doc__, 'Foo')
            self.assertEqual(Baz().__doc__, 'Foo')
            self.assertEqual(Baz.frobnicate.__doc__, 'Frobnicate this gonk.')

        def test_inherit_metaclass_(self):
            class Foo(object):
                'Foo'

                def frobnicate(self):
                    'Frobnicate this gonk.'
            class Bar(Foo, metaclass=DocStringInheritor):
                pass

            class Baz(Bar):
                pass
            self.assertEqual(Baz.__doc__, 'Foo')
            self.assertEqual(Baz().__doc__, 'Foo')
            self.assertEqual(Baz.frobnicate.__doc__, 'Frobnicate this gonk.')

        def test_property(self):
            class Foo(object):

                @property
                def frobnicate(self):
                    'Frobnicate this gonk.'
            class Bar(Foo, metaclass=DocStringInheritor):

                @property
                def frobnicate(self): pass

            self.assertEqual(Bar.frobnicate.__doc__, 'Frobnicate this gonk.')

    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
