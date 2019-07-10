''' Config Item Definitions '''

import os

from .data_types import DEFAULT_TYPE_RESOLVER, DEFAULT_DATA_TYPE


DEFAULT_DEFINITION = {'type': 'str', 'default': '', 'desc': '', 'env': []}


class QuickFigDefinition(object):
    ''' Configuration Definition '''

    def __init__(self, definition, resolver=None):
        ''' Constructor '''
        self.definition = definition
        self._resolver = resolver or DEFAULT_TYPE_RESOLVER

    @property
    def data_type(self):
        ''' Get Data Type '''
        return self._resolver.get(self.type, DEFAULT_DATA_TYPE)

    @property
    def type(self):
        ''' Get Data Type Name'''
        return self.definition.get('type', DEFAULT_DATA_TYPE.type_name)

    @property
    def default(self):
        ''' Get Default Value '''
        dtype = self.data_type
        value = self.definition.get('default', dtype.default)
        return dtype.convert_to(value)

    @property
    def desc(self):
        ''' Get Default Value '''
        desc = self.definition.get('desc', None)
        if not desc:
            dtype = self.data_type
            desc = "%s parameter" % dtype.type_name
        return desc

    @property
    def env(self):
        ''' Get list of environment variables '''
        env_vars = self.definition.get('env', [])
        if isinstance(env_vars, str):
            return [env_vars]
        if isinstance(env_vars, list):
            return env_vars
        return []

    def from_env(self):
        ''' Get value from environment variable, if set, else return '''
        for env_variable in self.env:
            if env_variable in os.environ:
                return self.convert_to(os.environ[env_variable])
        return None

    def convert_to(self, value):
        ''' Convert to '''
        return self.data_type.convert_to(value)

    def convert_from(self, value):
        ''' Convert from '''
        return self.data_type.convert_from(value)

    def __repr__(self):
        ''' repr '''
        return "%s" % self.definition


DEFAULT_DEFINITIONS = {}


def get_default_definition(resolver=None, default_dtype=None):
    ''' Get default definition '''
    if resolver is None:
        resolver = DEFAULT_TYPE_RESOLVER
    if default_dtype is None:
        default_dtype = DEFAULT_DATA_TYPE
    if resolver not in DEFAULT_DEFINITIONS:
        DEFAULT_DEFINITIONS[resolver] = {}

    default_definition = {}
    default_definition.update(DEFAULT_DEFINITION)
    default_definition['type'] = default_dtype.type_name
    def_type = default_definition['type']
    if def_type not in DEFAULT_DEFINITIONS[resolver]:
        definition = QuickFigDefinition(default_definition, resolver)
        DEFAULT_DEFINITIONS[resolver][def_type] = definition
    return DEFAULT_DEFINITIONS[resolver][def_type]
