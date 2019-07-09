''' Unit Tests For Config '''

import logging
import unittest

from .data_types import DEFAULT_DATA_TYPE, PARENT_DATA_TYPE
from .data_types import DEFAULT_TYPE_RESOLVER
from .data_types import INT_DATA_TYPE, FLOAT_DATA_TYPE
from .data_types import LIST_DATA_TYPE, DICT_DATA_TYPE
from .data_types import STRING_DATA_TYPE, BOOL_DATA_TYPE


TEST_BY_VALUE = [
    (None, DEFAULT_DATA_TYPE),
    ("", STRING_DATA_TYPE),
    ("true", STRING_DATA_TYPE),
    (True, BOOL_DATA_TYPE),
    (1, INT_DATA_TYPE),
    ("1", STRING_DATA_TYPE),
    (1.1, FLOAT_DATA_TYPE),
    ("1.1", STRING_DATA_TYPE)
]

TEST_BY_ID = [
    (None, DEFAULT_DATA_TYPE),
    ("str", STRING_DATA_TYPE),
    (str, STRING_DATA_TYPE),
    ("int", INT_DATA_TYPE),
    (int, INT_DATA_TYPE),
    ("float", FLOAT_DATA_TYPE),
    (float, FLOAT_DATA_TYPE),
    ("bool", BOOL_DATA_TYPE),
    (bool, BOOL_DATA_TYPE),
    ("list", LIST_DATA_TYPE),
    (list, LIST_DATA_TYPE),
    ("dict", DICT_DATA_TYPE),
    (dict, DICT_DATA_TYPE),
]


class TestConfyTypes(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parent_type(self):
        ''' Test for parent type to be dict '''
        self.assertEqual(PARENT_DATA_TYPE, DICT_DATA_TYPE)

    def test_dict(self):
        '''Test cases for dict'''
        dtype = DICT_DATA_TYPE

        self.assertTrue(dtype.is_dict)
        self.assertFalse(dtype.is_list)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get('dict'), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get({}.__class__), dtype)

    def test_list(self):
        '''Test cases for List'''
        dtype = LIST_DATA_TYPE
        self.assertFalse(dtype.is_dict)
        self.assertTrue(dtype.is_list)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get('list'), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get([].__class__), dtype)
        expected = ['1', 2]
        actual = dtype.convert_to(expected)
        self.assertListEqual(actual, expected)
        expected = "[ '1', 2 ]"
        actual = dtype.convert_to(expected)
        # This does not do what we expect at this time
        self.assertEqual(actual, expected)
        expected = ['1', 2]
        actual = dtype.convert_from(expected)
        self.assertListEqual(actual, expected)
        expected = "[ '1', 2 ]"
        actual = dtype.convert_from(expected)
        # This does not do what we expect at this time
        self.assertEqual(actual, expected)

    def test_bool(self):
        '''Test cases for Bool'''
        dtype = BOOL_DATA_TYPE
        self.assertFalse(dtype.is_dict)
        self.assertFalse(dtype.is_list)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get('bool'), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get(True.__class__), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.by_value(True), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get(False.__class__), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.by_value(False), dtype)

        expected = True
        actual = dtype.convert_to(expected)
        self.assertEqual(actual, expected)
        actual = dtype.convert_to("true")
        self.assertEqual(actual, expected)
        expected = 'true'
        actual = dtype.convert_from(expected)
        self.assertEqual(actual, expected)
        actual = dtype.convert_from(True)
        self.assertEqual(actual, expected)

    def test_float(self):
        '''Test cases for Float'''
        dtype = FLOAT_DATA_TYPE
        self.assertFalse(dtype.is_dict)
        self.assertFalse(dtype.is_list)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get('float'), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get((0.1).__class__), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.by_value(1.1), dtype)

        expected = 1.5
        actual = dtype.convert_to(expected)
        self.assertEqual(actual, expected)
        actual = dtype.convert_to("1.5")
        self.assertEqual(actual, expected)
        expected = '1.5'
        actual = dtype.convert_from(expected)
        self.assertEqual(actual, expected)
        actual = dtype.convert_from(1.5)
        self.assertEqual(actual, expected)

    def test_int(self):
        '''Test cases for Integer'''
        dtype = INT_DATA_TYPE
        self.assertFalse(dtype.is_dict)
        self.assertFalse(dtype.is_list)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get('int'), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.get((1).__class__), dtype)
        self.assertEqual(DEFAULT_TYPE_RESOLVER.by_value(1), dtype)

        expected = 2
        actual = dtype.convert_to(expected)
        self.assertEqual(actual, expected)
        actual = dtype.convert_to("2")
        self.assertEqual(actual, expected)
        expected = '2'
        actual = dtype.convert_from(expected)
        self.assertEqual(actual, expected)
        actual = dtype.convert_from(2)
        self.assertEqual(actual, expected)

    def test_resolver_by_value(self):
        ''' Test resolver getter by value '''
        for value, expected in TEST_BY_VALUE:
            actual = DEFAULT_TYPE_RESOLVER.by_value(value)
            self.assertEqual(actual, expected,
                             "%s %s(%s) - expected %s, got %s" % (
                                 "Failed while resolving", value, type(value),
                                 expected, actual))

    def test_resolver_by_id(self):
        ''' Test resolver getter by id '''
        for value, expected in TEST_BY_ID:
            actual = DEFAULT_TYPE_RESOLVER.get(value)
            self.assertEqual(actual, expected,
                             "%s %s(%s) - expected %s, got %s" % (
                                 "Failed while resolving", value, type(value),
                                 expected, actual))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
