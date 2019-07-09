''' Unit Tests For QuickFig Definitions '''

import logging
import unittest

from .data_types import BOOL_DATA_TYPE
from .data_types import DEFAULT_TYPE_RESOLVER
from .definitions import QuickFigDefinition
from .definitions import get_default_definition


class TestQuickFigDefinitions(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        ''' Test SetUp '''
        pass

    def tearDown(self):
        ''' Test TearDown '''
        pass

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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
