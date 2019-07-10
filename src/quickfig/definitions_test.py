''' Unit Tests For QuickFig Definitions '''
import logging
import os
import unittest

from .data_types import BOOL_DATA_TYPE
from .data_types import DEFAULT_TYPE_RESOLVER
from .definitions import QuickFigDefinition
from .definitions import get_default_definition


class TestQuickFigDefinitions(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        ''' Test SetUp '''

    def tearDown(self):
        ''' Test TearDown '''

    def test_repr(self):
        ''' Test __repr__() '''
        definition_dict = {'type': 'list', 'default': ['1']}
        definition = QuickFigDefinition(definition_dict)
        self.assertEqual("%s" % definition_dict, "%s" % definition)

    def test_convert_to(self):
        ''' Test get() '''
        definition_dict = {'type': 'int', 'default': 1}
        definition = QuickFigDefinition(definition_dict)
        actual = definition.convert_to("2")
        expected = 2
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

        actual = definition.convert_from(-1)
        expected = "-1"
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

    def test_get_default_definition(self):
        ''' Test get_default_definition() '''
        self.assertEqual(get_default_definition(None, None).type, "str")
        self.assertEqual(get_default_definition(
            DEFAULT_TYPE_RESOLVER, None).type, "str")
        self.assertEqual(get_default_definition(
            DEFAULT_TYPE_RESOLVER, BOOL_DATA_TYPE).type, "bool")

    def test_value_from_envs(self):
        ''' Test getting value from env variable '''
        definition_dict = {'type': 'int', 'default': 1,
                           'env': ['TEST_INT1', 'TEST_INT2']}
        definition = QuickFigDefinition(definition_dict)
        if 'TEST_INT1' in os.environ:
            del os.environ['TEST_INT1']
        if 'TEST_INT2' in os.environ:
            del os.environ['TEST_INT2']

        actual = definition.default
        expected = 1
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

        self.assertIsNone(definition.from_env())

        # Set one variable
        os.environ['TEST_INT2'] = "5"

        actual = definition.from_env()
        expected = 5
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

        del os.environ['TEST_INT2']

        # Set one variable
        os.environ['TEST_INT1'] = "8"

        actual = definition.from_env()
        expected = 8
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

        os.environ['TEST_INT2'] = "15"

        actual = definition.from_env()
        expected = 8
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

    def test_value_from_env(self):
        ''' Test getting value from env variable when set as a  string '''
        definition_dict = {'type': 'int', 'default': 1,
                           'env': 'TEST_INT1'}
        definition = QuickFigDefinition(definition_dict)
        if 'TEST_INT1' in os.environ:
            del os.environ['TEST_INT1']

        actual = definition.default
        expected = 1
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

        self.assertIsNone(definition.from_env())

        # Set one variable
        os.environ['TEST_INT1'] = "5"

        actual = definition.from_env()
        expected = 5
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

    def test_value_from_bad_env(self):
        ''' Test getting value from env variable when set as a  string '''
        definition_dict = {'type': 'int', 'default': 1,
                           'env': None}
        definition = QuickFigDefinition(definition_dict)
        if 'TEST_INT1' in os.environ:
            del os.environ['TEST_INT1']

        actual = definition.default
        expected = 1
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))

        self.assertIsNone(definition.from_env())

        # Set one variable
        os.environ['TEST_INT1'] = "5"

        actual = definition.from_env()
        expected = None
        self.assertEqual(actual, expected)
        self.assertEqual(type(actual), type(expected))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
