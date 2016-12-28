"""Querying interface from tinydb.

Original available at:
    https://github.com/msiemens/tinydb/blob/master/tinydb/queries.py

Altered source mark:
    --------------------------------------------------------------------------
               _ _                    _                                  _
         /\   | | |                  | |                                | |
        /  \  | | |_ ___ _ __ ___  __| |    ___  ___  _   _ _ __ ___ ___| |
       / /\ \ | | __/ _ \ '__/ _ \/ _` |   / __|/ _ \| | | | '__/ __/ _ \ |
      / ____ \| | ||  __/ | |  __/ (_| |   \__ \ (_) | |_| | | | (_|  __/_|
     /_/    \_\_|\__\___|_|  \___|\__,_|   |___/\___/ \__,_|_|  \___\___(_)

    --------------------------------------------------------------------------

tinydb Notice:
----------------------------------------------------------------------------
# Copyright (C) 2013 Markus Siemens <markus@m-siemens.de>
#  Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
----------------------------------------------------------------------------
"""

import re

__all__ = ('Query', 'where', 'freeze')


def is_sequence(obj):
    return hasattr(obj, '__iter__')


class QueryImpl(object):
    """A query implementation.

    This query implementation wraps a test function which is run when the
    query is evaluated by calling the object.

    Queries can be combined with logical and/or and modified with logical not.
    """

    __slots__ = ('test', 'hashval')

    def __init__(self, test, hashval):
        self.test = test
        self.hashval = hashval

    def __call__(self, value):
        return self.test(value)

    def __hash__(self):
        return hash(self.hashval)

    def __repr__(self):
        return 'QueryImpl{0}'.format(self.hashval)

    def __eq__(self, other):
        return self.hashval == other.hashval

    # --- Query modifiers -----------------------------------------------------

    def __and__(self, other):
        # We use a frozenset for the hash as the AND operation is commutative
        # (a | b == b | a)
        return QueryImpl(lambda value: self(value) and other(value),
                         ('and', frozenset([self.hashval, other.hashval])))

    def __or__(self, other):
        # We use a frozenset for the hash as the OR operation is commutative
        # (a & b == b & a)
        return QueryImpl(lambda value: self(value) or other(value),
                         ('or', frozenset([self.hashval, other.hashval])))

    def __invert__(self):
        return QueryImpl(lambda value: not self(value),
                         ('not', self.hashval))


class Query(object):
    """
    TinyDB Queries.

    Allows to build queries for TinyDB databases. There are two main ways of
    using queries:

    1) ORM-like usage:

    >>> User = Query('user')
    >>> db.find(User.name == 'John Doe')
    >>> db.find(User['logged-in'] == True)

    2) Classical usage:

    >>> db.find(where('value') == True)

    Note that ``where(...)`` is a shorthand for ``Query(...)`` allowing for
    a more fluent syntax.

    Besides the methods documented here you can combine queries using the
    binary AND and OR operators:

    >>> db.find(where('field1').exists() & where('field2') == 5)  # Binary AND
    >>> db.find(where('field1').exists() | where('field2') == 5)  # Binary OR

    Queries are executed by calling the resulting object. They expect to get
    the element to test as the first argument and return ``True`` or ``False``
    depending on whether the elements matches the query or not.
    """

    __slots__ = ('_path')

    def __init__(self, path=None):
        """..."""
        if path is None:
            self._path = []
        else:
            self._path = path

    def __getattr__(self, item):
        """..."""
        return Query(self._path + [item])

    __getitem__ = __getattr__

    def _generate_test(self, test, hashval):
        """
        Generate a query based on a test function.

        :param test: The test the query executes.
        :param hashval: The hash of the query.
        :return: A :class:`~tinydb.queries.QueryImpl` object
        """
        if not self._path:
            raise ValueError('Query has no path')

        def impl(value):
            try:
                # Resolve the path
                for part in self._path:
                    value = value[part]
            except (KeyError, TypeError):
                return False
            else:
                return test(value)

        return QueryImpl(impl, hashval)

    def __eq__(self, rhs):
        """
        Test a dict value for equality.

        >>> Query('f1') == 42

        :param rhs: The value to compare against
        """
        def test(value):
            return value == rhs

        return self._generate_test(lambda value: test(value),
                                   ('==', tuple(self._path), freeze(rhs)))

    def __ne__(self, rhs):
        """
        Test a dict value for inequality.

        >>> Query('f1') != 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value != rhs,
                                   ('!=', tuple(self._path), freeze(rhs)))

    def __lt__(self, rhs):
        """
        Test a dict value for being lower than another value.

        >>> Query('f1') < 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value < rhs,
                                   ('<', tuple(self._path), rhs))

    def __le__(self, rhs):
        """
        Test a dict value for being lower than or equal to another value.

        >>> where('f1') <= 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value <= rhs,
                                   ('<=', tuple(self._path), rhs))

    def __gt__(self, rhs):
        """
        Test a dict value for being greater than another value.

        >>> Query('f1') > 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value > rhs,
                                   ('>', tuple(self._path), rhs))

    def __ge__(self, rhs):
        """
        Test a dict value for being greater than or equal to another value.

        >>> Query('f1') >= 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value >= rhs,
                                   ('>=', tuple(self._path), rhs))

    def exists(self):
        """
        Test for a dict where a provided key exists.

        >>> Query('f1').exists() >= 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda _: True,
                                   ('exists', tuple(self._path)))

    def matches(self, regex):
        """
        Run a regex test against a dict value (whole string has to match).

        >>> Query('f1').matches(r'^\w+$')

        :param regex: The regular expression to use for matching
        """
        return self._generate_test(lambda value: re.match(regex, value),
                                   ('matches', tuple(self._path), regex))

    def search(self, regex):
        """
        Run a regex test against a dict value.

        Only substring string has to match).

        >>> Query('f1').search(r'^\w+$')

        :param regex: The regular expression to use for matching
        """
        return self._generate_test(lambda value: re.search(regex, value),
                                   ('search', tuple(self._path), regex))

    def test(self, func, *args):
        """
        Run a user-defined test function against a dict value.

        >>> def test_func(val):
        ...     return val == 42
        ...
        >>> Query('f1').test(test_func)

        :param func: The function to call, passing the dict as the first
                     argument
        :param args: Additional arguments to pass to the test function
        """
        return self._generate_test(lambda value: func(value, *args),
                                   ('test', tuple(self._path), func, args))

    def any(self, cond):
        """Check if a condition is met by any element in a list.

        A condition can also be a sequence (e.g. list).

        >>> Query('f1').any(Query('f2') == 1)

        Matches::

            {'f1': [{'f2': 1}, {'f2': 0}]}

        >>> Query('f1').any([1, 2, 3])
        # Match f1 that contains any element from [1, 2, 3]

        Matches::

            {'f1': [1, 2]}
            {'f1': [3, 4, 5]}

        :param cond: Either a query that at least one element has to match or
                     a list of which at least one element has to be contained
                     in the tested element.
        """
        if callable(cond):
            def _cmp(value):
                return is_sequence(value) and any(cond(e) for e in value)

        else:
            def _cmp(value):
                return is_sequence(value) and any(e in cond for e in value)

        return self._generate_test(lambda value: _cmp(value),
                                   ('any', tuple(self._path), freeze(cond)))

    def all(self, cond):
        """Check if a condition is met by any element in a list.

        A condition can also be a sequence (e.g. list).

        >>> Query('f1').all(Query('f2') == 1)

        Matches::

            {'f1': [{'f2': 1}, {'f2': 1}]}

        >>> Query('f1').all([1, 2, 3])
        # Match f1 that contains any element from [1, 2, 3]

        Matches::

            {'f1': [1, 2, 3, 4, 5]}

        :param cond: Either a query that all elements have to match or a list
                     which has to be contained in the tested element.
        """
        if callable(cond):
            def _cmp(value):
                return is_sequence(value) and all(cond(e) for e in value)

        else:
            def _cmp(value):
                return is_sequence(value) and all(e in value for e in cond)

        return self._generate_test(lambda value: _cmp(value),
                                   ('all', tuple(self._path), freeze(cond)))

    def none(self, cond):
        """Check if conditions evaluate to False."""
        if callable(cond):
            def _cmp(value):
                return is_sequence(value) and all(
                    not cond(e) for e in value)

        else:
            def _cmp(value):
                return is_sequence(value) and all(
                    e != value for e in cond)

        return self._generate_test(lambda value: _cmp(value),
                                   ('none', tuple(self._path), freeze(cond)))


def where(key):
    """..."""
    return Query()[key]


class FrozenDict(dict):
    """..."""

    __slots__ = ('data')

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


def freeze(obj):
    """..."""
    if isinstance(obj, dict):
        return FrozenDict((k, freeze(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return tuple(freeze(el) for el in obj)
    elif isinstance(obj, set):
        return frozenset(obj)
    else:
        return obj

if __name__ == '__main__':
    import os
    from pprint import pprint

    from dnf_game.util import packer, dnf_path

    PATH = os.path.join(dnf_path(), 'data', 'bestiary_optimized.bzp')

    def search(db, cond):
        """Search for all elements matching a 'where' cond.

        :param cond: the condition to check against
        :type cond: Query

        :returns: list of matching elements
        :rtype: list[Element]
        """
        elements = [element for element in db if cond(element)]

        return elements

    cdb = list(packer.unpack_json(PATH).values())
    # cdb = [v for v in packer.unpack_json(PATH).values()]

    creature = Query()
    pprint(search(cdb, (creature.cr >= 30) & (creature.hp >= 774)),
           indent=4)
