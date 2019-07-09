''' Config Node Types '''

from .type_converters import to_bool, from_bool
from .type_converters import to_float, from_float
from .type_converters import to_int, from_int
from .type_converters import to_str, from_str


class QuickFigDataType(object):
    ''' Configuration Node Type '''

    def __init__(self, name, type_class, **kwargs):
        ''' Constructor '''
        self.type_name = name
        self.type_class = type_class
        self.to_converter = kwargs.get('to_converter', None)
        self.from_converter = kwargs.get('from_converter', None)
        self.default = kwargs.get('default', None)

    @property
    def is_dict(self):
        ''' Check if this is a dict '''
        return isinstance(self.type_class(), dict)

    @property
    def is_list(self):
        ''' Check if this is a list '''
        return isinstance(self.type_class(), list)

    def convert_to(self, value):
        ''' Convert to this type '''
        if self.to_converter:
            new_value = self.to_converter(value)
            return new_value
        return value

    def convert_from(self, value):
        ''' Convert to this type '''
        if self.from_converter:
            return self.from_converter(value)
        return value

    def __repr__(self):
        ''' Repesentation '''
        return "%s::%s" % (self.type_name, self.type_class)


DICT_DATA_TYPE = QuickFigDataType('dict', dict, default={})
STRING_DATA_TYPE = QuickFigDataType('str', str,
                                    to_converter=to_str,
                                    from_converter=from_str, default="")
LIST_DATA_TYPE = QuickFigDataType('list', list, default=[])
INT_DATA_TYPE = QuickFigDataType('int', int,
                                 to_converter=to_int,
                                 from_converter=from_int, default=0)
FLOAT_DATA_TYPE = QuickFigDataType('float', float,
                                   to_converter=to_float,
                                   from_converter=from_float, default=0.0)
BOOL_DATA_TYPE = QuickFigDataType('bool', bool,
                                  to_converter=to_bool,
                                  from_converter=from_bool, default=False)

DEFAULT_DATA_TYPE = STRING_DATA_TYPE
PARENT_DATA_TYPE = DICT_DATA_TYPE


class ConfDataTypeResolver(object):
    ''' Tool for tracking known ConfigNode Types '''

    def __init__(self, *types):
        ''' Constructor '''
        self._by_name = {}
        self._by_class = {}
        for node_type in types:
            self.add_node(node_type)

    def add_node(self, node_type):
        ''' Add Node Type '''
        self._by_name[node_type.type_name] = node_type
        self._by_class[node_type.type_class] = node_type

    def get(self, type_id, default=DEFAULT_DATA_TYPE):
        ''' Get node by type_id - type_id can be either a class or name '''
        node_type = self._by_name.get(type_id, None)
        if not node_type:
            node_type = self._by_class.get(type_id, None)
        if not node_type:
            return default
        return node_type

    def by_value(self, value):
        ''' get by value '''
        if value is None:
            return DEFAULT_DATA_TYPE
        return self.get(value.__class__, DEFAULT_DATA_TYPE)


DEFAULT_TYPE_RESOLVER = ConfDataTypeResolver(
    DICT_DATA_TYPE,
    LIST_DATA_TYPE,
    STRING_DATA_TYPE,
    INT_DATA_TYPE,
    FLOAT_DATA_TYPE,
    BOOL_DATA_TYPE
)

# Initialize Default Node Types
DEFAULT_TYPE_RESOLVER.add_node(PARENT_DATA_TYPE)
DEFAULT_TYPE_RESOLVER.add_node(DEFAULT_DATA_TYPE)
