''' Type Conversion Utilities '''

BOOL_TRUE = ['true', '1', 'y', 'yes', 'on']


def to_bool(string, default=False):
    ''' Convert String to boolean '''
    return str(string if string is not None else default).lower() in BOOL_TRUE


def from_bool(value):
    ''' Convert boolean value to string '''
    return str(bool(value)).lower()


def to_int(string, default=0):
    ''' Convert String to integer '''
    try:
        return int(string)
    except Exception:  # pylint: disable=broad-except
        return default


def from_int(value):
    ''' Convert Integer to String'''
    if isinstance(value, bool):
        value = 1 if value else 0
    if not isinstance(value, int):
        try:
            value = int(value)
        except Exception:  # pylint: disable=broad-except
            value = 0
    return str(value)


def to_float(string, default=0.0):
    ''' Convert String to float '''
    try:
        return float(string)
    except Exception:  # pylint: disable=broad-except
        return default


def from_float(value):
    ''' Convert Float to String '''
    if isinstance(value, bool):
        value = 1.0 if value else 0.0
    if isinstance(value, int):
        value = float(value)
    try:
        value = float(value)
    except Exception:  # pylint: disable=broad-except
        value = 0.0
    if value == 0 or value is None:
        return "0.0"
    return str(value)


def to_str(string, default=''):
    ''' Convert String to String (ensure String) '''
    return str(string if string is not None else default)


def from_str(string):
    ''' Convert String to String (ensure String) '''
    return to_str(string)
