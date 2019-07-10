''' Unit Tests For Config '''

import logging
import os
import tempfile
import unittest

from backports.tempfile import TemporaryDirectory
import yaml

from . import QuickFig, QuickFigNode
from .data_types import INT_DATA_TYPE, BOOL_DATA_TYPE, STRING_DATA_TYPE


CONFIG_YAML = '''
test:
  string: value
  int: 1
  float: 1.1
  float2: 2.2
  bool: yes
  dict:
    item1: one
    item2: two
'''
CONFIG = yaml.safe_load(CONFIG_YAML)

CONF_TOP_REPR = '''
#QuickFig Config

# my
#  multiline
#  description
#   (Default: 'False')
test.bool = True

# str parameter (Default: '')
test.dict.item1 = one

# str parameter (Default: '')
test.dict.item2 = two

# float parameter (Default: '-1.0')
test.float = 1.1

# float parameter (Default: '0.0')
test.float2 = 2.2

# My Integer Parameter (Default: '-1')
test.int = 1

# int parameter (Default: '2')
test.int2 = 2

# String Parameter (Default: 'first test string')
test.string = value

# str parameter (Default: 'test2string')
test2 = test2string

#End QuickFig Config
'''

CONF_TEST_DICT_REPR = '''
#QuickFig Config
#
# Path: test
#

# my
#  multiline
#  description
#   (Default: 'False')
bool = True

# str parameter (Default: '')
dict.item1 = one

# str parameter (Default: '')
dict.item2 = two

# float parameter (Default: '-1.0')
float = 1.1

# float parameter (Default: '0.0')
float2 = 2.2

# My Integer Parameter (Default: '-1')
int = 1

# int parameter (Default: '2')
int2 = 2

# String Parameter (Default: 'first test string')
string = value

#End QuickFig Config
'''

CONFIG_DEF_YAML = '''
test2:
  type: str
  default: test2string

test.string:
  type: str
  default: first test string
  desc: "String Parameter"

test.int:
  type: int
  default: -1
  desc: My Integer Parameter

test.float:
  type: float
  default: -1.0

test.bool:
  type: bool
  default: false
  desc: |
    my
    multiline
    description

test.int2:
  type: int
  default: 2

'''

CONFIG_DEF = yaml.safe_load(CONFIG_DEF_YAML)


class TestQuickFig(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        self.config = QuickFig(definitions=CONFIG_DEF, config=CONFIG)

    def tearDown(self):
        self.config = None

    def test_repr(self):
        ''' Test __repr___() '''
        actual = "%s" % self.config
        expected = CONF_TOP_REPR
        self.assertEqual(actual.strip(), expected.strip())

    def test_get_definition(self):
        ''' Test get_definition() '''
        self.assertEqual(self.config.get_definition(
            "test.bool", None, None).type, "bool")
        self.assertEqual(self.config.get_definition(
            "test.unset", None, INT_DATA_TYPE).type, "int")

    def test_get_data_type(self):
        ''' Test get_data_type() '''
        self.assertEqual(self.config.get_data_type(
            "test.bool", 'str'), BOOL_DATA_TYPE)
        self.assertEqual(self.config.get_data_type(
            "test.unset", 'str'), STRING_DATA_TYPE)

    def test_repr_node(self):
        ''' Test __repr___() on node '''
        section = self.config.section('test')
        actual = "%s" % section
        print("---\n\n%s\n\n---" % actual)
        expected = CONF_TEST_DICT_REPR
        self.assertEqual(actual.strip(), expected.strip())

    def test_get(self):
        ''' Test get() '''
        self.assertEqual(self.config.get('test.bool', False), True)
        self.assertEqual(self.config.get('test.int2', 0), 2)

    def test_no_definition(self):
        ''' Test if no definition '''
        self.config = QuickFig(config=CONFIG)
        self.assertEqual(self.config.get('test.bool', False), True)
        self.assertEqual(self.config.get('test.int2', 0), 0)

    def test_no_data(self):
        ''' Test if no definition '''
        self.config = QuickFig(definitions=CONFIG_DEF)
        self.assertEqual(self.config.get('test.bool', False), False)
        self.assertEqual(self.config.get('test.int2', 0), 2)

    def test_set(self):
        ''' Test set() '''
        self.assertEqual(self.config.get('test.bool', False), True)
        self.config.set('test.bool', False)
        self.assertEqual(self.config.get('test.bool', False), False)
        self.config.set('test.bool', 1)
        self.assertEqual(self.config.get('test.bool', False), True)

    def test_set_section(self):
        ''' Test set() '''
        # print("Config: \n\n%s\n\n" % self.config)
        section = self.config.section('test.dict')
        self.assertEqual(section.get('item1', "wrong"), "one")
        section.set('item1', "TWO")
        self.assertEqual(section.get('item1', "wrong"), "TWO")
        self.assertEqual(self.config.get('test.dict.item1', "wrong"), "TWO")

    def test_section(self):
        ''' Test section() '''
        section = self.config.section('test')
        self.assertEqual(section.get('bool', False), True)
        self.assertEqual(section.get('int2', 0), 2)

    def test_attribute_getter(self):
        ''' Test getting by attribute() '''
        section = self.config.test
        self.assertEqual(section.get('bool', False), True)
        self.assertEqual(section.get('int2', 0), 2)

        self.assertEqual(section.bool, True)
        self.assertEqual(section.int2, 2)

        self.assertEqual(self.config.test2, "test2string")

    def test_section_invalid(self):
        ''' Test section() '''
        section = self.config.section('')
        self.assertEqual(section, self.config)
        section = self.config.section(None)
        self.assertEqual(section, self.config)
        section = self.config.section('unknown')
        self.assertTrue(isinstance(section, QuickFigNode))

    def test_load_from_file(self):
        ''' Testing loading from file '''
        config = QuickFig(definitions=CONFIG_DEF)
        with tempfile.NamedTemporaryFile(mode="w") as conffile:
            conffile.write(CONFIG_YAML)
            conffile.flush()

            config.quickfig_load_from_file(conffile.name)

            # Perform some test
            section = config.test
            self.assertEqual(section.get('bool', False), True)
            self.assertEqual(section.get('int2', 0), 2)

            self.assertEqual(section.bool, True)
            self.assertEqual(section.int2, 2)

            self.assertEqual(config.test2, "test2string")

    def test_load_from_non_existent_file(self):
        ''' Testing loading from file '''
        config = QuickFig(definitions=CONFIG_DEF)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "non-existing.conf")
            config.quickfig_load_from_file(filename)

            # Perform some test
            section = config.test
            self.assertEqual(section.get('bool', False), False)
            self.assertEqual(section.get('int2', 0), 2)

            self.assertEqual(section.bool, False)
            self.assertEqual(section.int2, 2)

            self.assertEqual(config.test2, "test2string")

    def test_load_from_unreadable_file(self):
        ''' Testing loading from file '''
        config = QuickFig(definitions=CONFIG_DEF)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "non-existing.conf")
            with open(filename, "w") as stream:
                stream.write(" sdds: sdss : ")
            config.quickfig_load_from_file(filename)

            # Perform some test
            section = config.test
            self.assertEqual(section.get('bool', False), False)
            self.assertEqual(section.get('int2', 0), 2)

            self.assertEqual(section.bool, False)
            self.assertEqual(section.int2, 2)

            self.assertEqual(config.test2, "test2string")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
