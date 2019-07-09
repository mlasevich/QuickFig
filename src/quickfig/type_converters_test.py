''' Unit Tests For Config '''

import logging
import unittest

from .type_converters import to_bool, from_bool
from .type_converters import to_float, from_float
from .type_converters import to_int, from_int
from .type_converters import to_str, from_str


TESTS = {
    'to_int': [
        (0, 0),
        ("0", 0),
        ("5", 5),
        ("-5", -5),
        (None, 0),
        (True, 1),
        (False, 0)
    ],
    'from_int': [
        (0, "0"),
        (0, "0"),
        (5, "5"),
        ("5", "5"),
        (-5, "-5"),
        (None, "0"),
        (True, "1"),
        (False, "0")
    ],
    'to_float': [
        (0, 0.0),
        ("0", 0.0),
        ("0.1", 0.1),
        (".99", 0.99),
        ("5", 5.0),
        ("-5", -5.0),
        ("-5.0", -5.0),
        (None, 0.0),
        (True, 1.0),
        (False, 0.0)
    ],
    'from_float': [
        (None, "0.0"),
        (True, "1.0"),
        (False, "0.0"),
        (0.1, "0.1"),
        (1, "1.0"),
        (-1.234, "-1.234"),
        ("0", "0.0"),
        ("5.1", "5.1"),
    ],
    "to_bool": [
        (1, True),
        (0, False),
        ("1", True),
        ("0", False),
        ("yes", True),
        ("no", False),
        (None, False),
        (False, False),
        (True, True),
        ("False", False),
        ("True", True),
        ("false", False),
        ("true", True)
    ],
    "from_bool": [
        (True, 'true'),
        (False, 'false'),
        (0, 'false'),
        (1, 'true')
    ],
    "to_str": [
        (None, ''),
        ('', ''),
        ('string', 'string'),
        (1, '1'),
        (1.1, '1.1')
    ],
    "from_str": [
        (None, ''),
        ('', ''),
        ('string', 'string'),
        (1, '1'),
        (1.1, '1.1')
    ]

}


class TestQuickFigTypeConverters(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_to_int(self):
        '''Test cases for to_int'''
        for test_value, expected in TESTS.get('to_int', []):
            self.assertEqual(to_int(test_value), expected)

    def test_from_int(self):
        '''Test cases for from_int'''
        for test_value, expected in TESTS.get('from_int', []):
            self.assertEqual(from_int(test_value), expected)

    def test_to_float(self):
        '''Test cases for to_floatt'''
        for test_value, expected in TESTS.get('to_float', []):
            self.assertAlmostEqual(to_float(test_value), expected, 3)

    def test_from_float(self):
        '''Test cases for from_float'''
        for test_value, expected in TESTS.get('from_float', []):
            actual = from_float(test_value)
            self.assertEqual(actual, expected,
                             "Expected %s(%s) from '%s', but got %s(%s)" % (
                                 expected, type(expected), test_value, actual,
                                 type(actual)))

    def test_to_bool(self):
        '''Test cases for to_bool'''
        for test_value, expected in TESTS.get('to_bool', []):
            self.assertEqual(to_bool(test_value), expected, 3)

    def test_from_bool(self):
        '''Test cases for from_bool'''
        for test_value, expected in TESTS.get('from_bool', []):
            self.assertEqual(from_bool(test_value), expected)

    def test_to_str(self):
        '''Test cases for to_str'''
        for test_value, expected in TESTS.get('to_str', []):
            self.assertEqual(to_str(test_value), expected, 3)

    def test_from_str(self):
        '''Test cases for from_str'''
        for test_value, expected in TESTS.get('from_str', []):
            self.assertEqual(from_str(test_value), expected)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
