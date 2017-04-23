import unittest

import cachedir


class TestMatches(unittest.TestCase):
    def test_positive(self):
        a = any
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

        a = {}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

        a = {'a': any, 'b': 2}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

        a = {'a': any, 'b': any, 'c': any, 'd': any}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

        a = {'c': {}}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

        a = {'c': {'x': any}}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

        a = {'d': any}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertTrue(cachedir.matches_structure(a, b))

    def test_negative(self):
        a = {'d': {}}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertFalse(cachedir.matches_structure(a, b))

        a = {'e': any}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertFalse(cachedir.matches_structure(a, b))

        a = {'a': 1, 'b': 2, 'c': {'z': any}, 'd': any}
        b = {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}
        self.assertFalse(cachedir.matches_structure(a, b))
