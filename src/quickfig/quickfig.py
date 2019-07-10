''' QuickFig Object '''
import logging
import os

import yaml

from .data_types import DEFAULT_TYPE_RESOLVER
from .definitions import QuickFigDefinition, get_default_definition


LOG = logging.getLogger(__name__)


class QuickFigNode(object):
    ''' QuickFig main object '''

    def __init__(self, root=None, path=None, resolver=None):
        ''' Construct QuickFig Object '''

        self._root = root
        self._path = path
        self._type_resolver = resolver if resolver else None

    @property
    def _resolver(self):
        ''' Get Type Resolver '''
        resolver = self._type_resolver
        if not resolver and self._root:
            resolver = self._root._resolver  # pylint: disable=W0212
        return resolver if resolver else DEFAULT_TYPE_RESOLVER

    @property
    def _data(self):
        ''' Get Root Data '''
        return self._root._data  # pylint: disable=W0212

    def _full_key(self, key):
        ''' Get full key name '''
        if self._path:
            return "%s.%s" % (self._path, key)
        return key

    def set(self, key, value):
        ''' Set Value using absolute key '''
        self._root.set(self._full_key(key), value)

    def get(self, key, default_value=None, use_definition_default=False):
        ''' Get using absolute key value '''
        return self._root.get(self._full_key(key),
                              default_value=default_value,
                              use_definition_default=use_definition_default)

    def section(self, section_name):
        ''' Get QuickFigNode for a section or sub-section '''
        if section_name:
            return QuickFigNode(root=self._root if self._root else self,
                                path=self._full_key(section_name))
        return self

    def get_definition(self, key, test_value="", default_dtype=None):
        ''' Get Definition for key '''

        path = self._full_key(key)
        if not default_dtype:
            default_dtype = self._resolver.by_value(test_value)
        definition = self.definitions.get(path, None)
        if not definition:
            definition = get_default_definition(self._resolver, default_dtype)
        return definition

    def __getattr__(self, key):
        ''' Attribute Getter '''
        param = self._full_key(key)
        data = self._data
        if param in data:
            return self.get(key, use_definition_default=True)
        return self.section(key)

    @property
    def definitions(self):
        ''' Return definitions '''
        if self._root:
            return self._root._defs
        if isinstance(self, QuickFig):
            return self._defs
        LOG.debug("Unable to find definitions..")
        return {}

    def __repr__(self):
        ''' Dump Config '''
        dump = "#QuickFig Config\n"
        if self._path:
            dump += "#\n# Path: %s\n#\n" % self._path
        for key in sorted(self._data.keys()):
            value = self._data[key]
            param = key
            if self._path:
                if not param.startswith("%s." % self._path):
                    LOG.debug("Skipping non-matching parameter")
                    continue
                param = key[len(self._path) + 1:]
            definition = self.get_definition(param, test_value=value)
            dump += "\n# %s (Default: '%s')\n" % (
                definition.desc.replace('\n', '\n#  '),
                definition.default)
            dump += "%s = %s\n" % (param, value)

        dump += "\n#End QuickFig Config\n"
        return dump


class QuickFig(QuickFigNode):
    ''' Root QuickFig Node '''

    def __init__(self, definitions=None, config=None, overrides=None,
                 resolver=None):
        ''' Construct QuickFig Object '''
        self._definitions = definitions
        self._overrides = overrides
        self._defs = {}
        self._root_data = {}
        self.quickfig_load(config)
        QuickFigNode.__init__(self, resolver=resolver)

    def _load_definitions(self, definitions):
        ''' Load Definitions '''
        if definitions:
            for param, def_dict in definitions.items():
                definition = QuickFigDefinition(def_dict)
                self._defs[param] = definition
                value = definition.from_env()
                if value is None:
                    value = definition.default
                self.set(param, value)

    def quickfig_load(self, config):
        ''' Load configuration'''
        self._defs = {}
        self._root_data = {}
        self._load_definitions(self._definitions)
        self._load_data(config)
        self._load_data(self._overrides)

    def quickfig_load_from_file(self, filename, warn=False):
        ''' Load from file '''
        level = logging.WARNING if warn else logging.DEBUG

        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as stream:
                    config = yaml.safe_load(stream)
                self.quickfig_load(config)
            except Exception as ex:  # pylint: disable=broad-except
                logging.log(
                    level, "Unable to load config from file: %s: %s",
                    filename, ex)
        else:
            logging.log(level, "Unable to load config from file: %s",
                        filename)

    def _load_data(self, data, prefix=None):
        ''' Load data from dictionary '''
        if data is not None:
            if isinstance(data, dict):
                for key, item in data.items():
                    new_prefix = key if prefix is None else "%s.%s" % (
                        prefix, key)
                    self._load_data(item, new_prefix)
            else:
                self.set(prefix, data)

    @property
    def _data(self):
        ''' Get Root Data '''
        return self._root_data

    def set(self, key, value):
        ''' Set Value using absolute key '''
        self._root_data[str(key)] = value

    def get_data_type(self, key, test_value=""):
        ''' Get Data Type '''
        default_def = get_default_definition(
            None, self._resolver.by_value(test_value))
        return self._defs.get(key, default_def).data_type

    def get(self, key, default_value=None, use_definition_default=False):
        ''' Get using absolute key value '''
        if use_definition_default:
            definition = self.get_definition(key, "")
            default_value = definition.default
        value = self._root_data.get(key, default_value)
        definition = self.get_definition(key, value)
        return definition.convert_to(value)
