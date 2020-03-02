"""Modify module."""

import re

from .numeric import \
    shape, \
    create_full_array, \
    extend_full_array

from .definition import \
    KIMPropertyError, \
    get_optional_key_extent_ndimensions, \
    get_optional_key_extent_shape

from .instance import standard_keys

from .create import get_properties

try:
    import kim_edn
except:
    msg = '\nERROR: Failed to import the `kim_edn` utility module.'
    raise KIMPropertyError(msg)

__all__ = [
    "kim_property_modify",
]


STANDARD_KEYS_WITH_EXTENT = (
    "source-value",
    "si-value",
    "source-std-uncert-value",
    "source-expand-uncert-value",
)
"""tuple: KIM property standard keys which have the extent."""


def kim_property_modify(property_instances, instance_id, *argv):
    """Build the property instance by receiving keys with associated arguments.

    Incrementally builds the property instance by receiving keys with
    associated arguments. It can be called multiple times and append values
    to a given key.

    For example::

    >>> str = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> str = kim_property_modify(str, 1,
                "key", "short-name",
                "source-value", "1", "fcc",
                "key", "species",
                "source-value", "1:4", "Al", "Al", "Al", "Al",
                "key", "a",
                "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                "source-unit", "angstrom", "digits", "5")
    >>> str = kim_property_modify(str, 1,
                "key", "basis-atom-coordinates",
                "source-value", "2", "1:2", "0.5", "0.5")
    >>> str = kim_property_modify(str, 1,
                "key", "basis-atom-coordinates",
                "source-value", "3", "1:3", "0.5", "0.0", "0.5",
                "key", "basis-atom-coordinates",
                "source-value", "4", "2:3", "0.5", "0.5")
    >>> str = kim_property_modify(str, 1,
                "key", "cohesive-potential-energy",
                "source-value", "1:5", "3.324", "3.3576", "3.3600", "3.3550", "3.3260",
                "source-std-uncert-value", "1:5", "0.002", "0.0001", "0.00001", "0.0012", "0.00015",
                "source-unit", "eV",
                "digits", "5")

    Arguments:
        property_instances {string} -- A string containing the serialized
        KIM-EDN formatted property instances.
        instance_id {int} -- A positive integer identifying the property
        instance.

    Returns:
        string -- serialized KIM-EDN formatted property instances.

    """
    if property_instances is None or \
            property_instances == 'None' or \
            property_instances == '' or \
            property_instances == '[]':
        msg = '\nERROR: There is no property instance to modify the content.'
        raise KIMPropertyError(msg)

    if not isinstance(instance_id, int):
        msg = '\nERROR: the "instance_id" is not an `int`.'
        raise KIMPropertyError(msg)

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    a_property_instance = None

    for p in kim_property_instances:
        if "instance-id" not in p:
            msg = '\nERROR: wrong input. The required "instance-id"-key is '
            msg += 'missing.'
            raise KIMPropertyError(msg)
        if p["instance-id"] == instance_id:
            a_property_instance = p
            break

    if a_property_instance is None:
        msg = '\nERROR: The requested instance id :\n'
        msg += '{}\n '.format(instance_id)
        msg += 'does not match any of the property instances ids.'
        raise KIMPropertyError(msg)

    if "property-id" not in a_property_instance:
        msg = '\nERROR: wrong input. The required "property-id"-key is '
        msg += 'missing.\n '
        msg += 'See KIM property instances at '
        msg += 'https://openkim.org/doc/schema/properties-framework/ '
        msg += 'in section 3 for more detailed information.'
        raise KIMPropertyError(msg)

    # Get the property definition id
    property_id = a_property_instance["property-id"]

    # Get KIM properties
    kim_properties = get_properties()

    # property definition
    property_def = kim_properties[property_id]

    # Number of arguments
    n_arguments = len(argv)

    # key keyword
    k_keyword = False

    # new keyword
    new_keyword = None
    new_keyword_map = {}

    i = 0
    while i < n_arguments:
        try:
            arg = argv[i]
        except IndexError:
            break

        if arg == 'key':
            k_keyword = True
            i += 1
            continue

        if k_keyword:
            k_keyword = False

            # new keyword
            new_keyword = arg

            if new_keyword not in property_def:
                msg = '\nERROR: wrong keyword. The input '
                msg += '"{}"-key is not defined in '.format(new_keyword)
                msg += 'the property definition \n'
                msg += '({})\n '.format(property_def['property-id'])
                msg += 'See the KIM Property Definitions at '
                msg += 'https://openkim.org/properties for more detailed '
                msg += 'information.'
                raise KIMPropertyError(msg)

            # Get the number of dimensions, shape and type of the key
            new_keyword_ndims = get_optional_key_extent_ndimensions(
                property_def[new_keyword]['extent'])
            new_keyword_shape = get_optional_key_extent_shape(
                property_def[new_keyword]['extent'])
            new_keyword_type = property_def[new_keyword]['type']

            if new_keyword in a_property_instance:
                new_keyword_map = a_property_instance[new_keyword]
            else:
                new_keyword_map = {}
                a_property_instance[new_keyword] = new_keyword_map

            i += 1
            continue

        new_keyword_key = arg
        i += 1

        if not new_keyword_key in standard_keys:
            msg = '\nERROR: wrong key. The input '
            msg += '"{}"-key is not part of '.format(new_keyword_key)
            msg += 'the standard key-value pairs definition.\n '
            msg += 'See KIM standard key-value pairs at '
            msg += 'https://openkim.org/doc/schema/properties-framework/ '
            msg += 'in section 3 for more detailed information.'
            raise KIMPropertyError(msg)

        if new_keyword_key == 'source-unit':
            if not property_def[new_keyword]['has-unit']:
                msg = '\nERROR: wrong key. The unit is wrongly provided '
                msg += 'to a key that does not have a unit. '
                msg += 'The corresponding "has-unit" key in the property '
                msg += 'definition has a `False` value.\n '
                msg += 'See the KIM Property Definitions at '
                msg += 'https://openkim.org/properties for more detailed '
                msg += 'information.'
                raise KIMPropertyError(msg)

        if new_keyword_key in STANDARD_KEYS_WITH_EXTENT:
            # Append
            if new_keyword_key in new_keyword_map:
                if new_keyword_ndims > 0:
                    new_keyword_value = new_keyword_map[new_keyword_key]
                    new_keyword_shape_new = shape(new_keyword_value)
                    new_keyword_index = []
                    _n = -1
                    _l = 0
                    _u = 0
                    for n in range(new_keyword_ndims):
                        if i >= n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use.\n Processing the {"'
                            msg += '{}'.format(new_keyword)
                            msg += '"}:{"'
                            msg += '{}'.format(new_keyword_key)
                            msg += '"} input arguments failed.\n The '
                            if n == 0:
                                msg += 'first '
                            elif n == 1:
                                msg += 'second '
                            elif n == 2:
                                msg += 'third '
                            else:
                                msg += '{}th '.format(n + 1)
                            msg += 'index is missing from the input '
                            msg += 'arguments.'
                            raise KIMPropertyError(msg)

                        arg = str(argv[i])
                        if re.match(r'^[1-9][0-9]*$', arg) is None:
                            if re.match(r'^[1-9][:0-9]*$', arg) is None:
                                msg = '\nERROR: requested index '
                                msg += '"{}" '.format(arg)
                                msg += 'doesn\'t meet the format '
                                msg += 'specification (an integer equal to '
                                msg += 'or greater than 1 or integer '
                                msg += 'indices range of "start:stop").'
                                raise KIMPropertyError(msg)
                            else:
                                if _n > -1:
                                    msg = '\nERROR: use of indices range is '
                                    msg += 'only accepted in one direction.'
                                    raise KIMPropertyError(msg)
                                _n = n
                                if arg.count(':') > 1:
                                    msg = '\nERROR: use of indices range as '
                                    msg += '"{}" '.format(arg)
                                    msg += 'is not accepted.\n'
                                    msg += 'The only supported indices '
                                    msg += 'range format is "start:stop".'
                                    raise KIMPropertyError(msg)
                                l, u = arg.split(':')
                                _l = int(l)
                                _u = int(u)
                                if _u < _l:
                                    msg = '\nERROR: use of indices range as '
                                    msg += '"{}" '.format(arg)
                                    msg += 'is not accepted.\n'
                                    msg += 'The only supported indices '
                                    msg += 'range format is "start:stop", '
                                    msg += 'where start is less or equal '
                                    msg += 'than stop.'
                                    raise KIMPropertyError(msg)
                                if new_keyword_shape[n] > 1 and \
                                        new_keyword_shape[n] < _u:
                                    msg = '\nERROR: this dimension has a '
                                    msg += 'fixed length = '
                                    msg += '{}'.format(new_keyword_shape[n])
                                    msg += ', while, wrong index = '
                                    msg += '{} '.format(_u)
                                    msg += 'is requested.\n Processing the '
                                    msg += '{"'
                                    msg += '{}'.format(new_keyword)
                                    msg += '"}:{"'
                                    msg += '{}'.format(new_keyword_key)
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += 'at the {}th '.format(n + 1)
                                    msg += 'dimension is requested.'
                                    raise KIMPropertyError(msg)
                                if new_keyword_shape[n] == 1 and _u > 1:
                                    if property_def[new_keyword]["extent"][n] == ':':
                                        if new_keyword_shape_new[n] < _u:
                                            new_keyword_shape_new[n] = _u

                                _l -= 1
                                new_keyword_index.append(-1)
                        else:
                            if new_keyword_shape[n] > 1 and \
                                    new_keyword_shape[n] < int(arg):
                                msg = '\nERROR: this dimension has a fixed '
                                msg += 'length = {}'.format(new_keyword_shape[n])
                                msg += ', while, wrong index = {} '.format(arg)
                                msg += 'is requested.\n Processing the {"'
                                msg += '{}'.format(new_keyword)
                                msg += '"}:{"'
                                msg += '{}'.format(new_keyword_key)
                                msg += '"} input arguments, wrong index '
                                if n == 0:
                                    msg += 'at the first '
                                elif n == 1:
                                    msg += 'at the second '
                                elif n == 2:
                                    msg += 'at the third '
                                else:
                                    msg += 'at the {}th '.format(n + 1)
                                msg += 'dimension is requested.'
                                raise KIMPropertyError(msg)
                            if new_keyword_shape[n] == 1 and int(arg) > 1:
                                if property_def[new_keyword]["extent"][n] == ':':
                                    if new_keyword_shape_new[n] < int(arg):
                                        new_keyword_shape_new[n] = int(arg)
                                else:
                                    msg = '\nERROR: this dimension has a '
                                    msg += 'fixed length = 1, while, wrong '
                                    msg += 'index = {} '.format(arg)
                                    msg += 'is requested.\n Processing the '
                                    msg += '{"'
                                    msg += '{}'.format(new_keyword)
                                    msg += '"}:{"'
                                    msg += '{}'.format(new_keyword_key)
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += 'at the {}th '.format(n + 1)
                                    msg += 'dimension is requested.'

                                    raise KIMPropertyError(msg)
                            new_keyword_index.append(int(arg) - 1)
                        i += 1

                    if new_keyword_type == 'int':
                        new_keyword_value = extend_full_array(
                            new_keyword_value, new_keyword_shape_new, 0)
                    elif new_keyword_type == 'float':
                        new_keyword_value = extend_full_array(
                            new_keyword_value, new_keyword_shape_new, 0.0)
                    elif new_keyword_type == 'bool':
                        new_keyword_value = extend_full_array(
                            new_keyword_value, new_keyword_shape_new, False)
                    elif new_keyword_type == 'string':
                        new_keyword_value = extend_full_array(
                            new_keyword_value, new_keyword_shape_new, '')
                    elif new_keyword_type == 'file':
                        new_keyword_value = extend_full_array(
                            new_keyword_value, new_keyword_shape_new, '')

                    del(new_keyword_shape_new)

                    if _n > -1:
                        if i - 1 + _u - _l >= n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use.\n Processing the {"'
                            msg += '{}'.format(new_keyword)
                            msg += '"}:{"'
                            msg += '{}'.format(new_keyword_key)
                            msg += '"} input arguments failed.\n '
                            msg += 'We have {} '.format(n_arguments - i + 1)
                            msg += 'more input arguments while '
                            msg += 'at least {} arguments '.format(_u - _l)
                            msg += 'are required.'
                            raise KIMPropertyError(msg)

                        if new_keyword_ndims == 1:
                            if new_keyword_type == 'int':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = int(argv[i])
                                    i += 1
                            elif new_keyword_type == 'float':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = float(argv[i])
                                    i += 1
                            elif new_keyword_type == 'bool':
                                for d0 in range(_l, _u):
                                    if argv[i] == 'true' or \
                                            argv[i] == 'True' or argv[i]:
                                        new_keyword_value[d0] = True
                                    i += 1
                            elif new_keyword_type == 'string':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = argv[i]
                                    i += 1
                            elif new_keyword_type == 'file':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = argv[i]
                                    i += 1
                        elif new_keyword_ndims == 2:
                            d0, d1 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = int(argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = float(argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = int(argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = float(argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 3:
                            d0, d1, d2 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 4:
                            d0, d1, d2, d3 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 5:
                            d0, d1, d2, d3, d4 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if new_keyword_type == 'int':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if new_keyword_type == 'int':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 4:
                                if new_keyword_type == 'int':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d5 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                    else:
                        if i >= n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use.\n Processing the {"'
                            msg += '{}'.format(new_keyword)
                            msg += '"}:{"'
                            msg += '{}'.format(new_keyword_key)
                            msg += '"} input arguments failed.\n '
                            msg += 'At least we need one further input.'
                            raise KIMPropertyError(msg)

                        if new_keyword_ndims == 1:
                            d0 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0] = argv[i]
                        elif new_keyword_ndims == 2:
                            d0, d1 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1] = argv[i]
                        elif new_keyword_ndims == 3:
                            d0, d1, d2 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2] = argv[i]
                        elif new_keyword_ndims == 4:
                            d0, d1, d2, d3 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2][d3] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2][d3] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2][d3] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2][d3] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2][d3] = argv[i]
                        elif new_keyword_ndims == 5:
                            d0, d1, d2, d3, d4 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2][d3][d4] = int(
                                    argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2][d3][d4] = float(
                                    argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2][d3][d4] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                        elif new_keyword_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                    argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                    argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                        i += 1
                else:
                    if new_keyword_type == 'int':
                        new_keyword_value = int(argv[i])
                    elif new_keyword_type == 'float':
                        new_keyword_value = float(argv[i])
                    elif new_keyword_type == 'bool':
                        if argv[i] == 'true' or \
                                argv[i] == 'True' or argv[i]:
                            new_keyword_value = True
                        else:
                            new_keyword_value = False
                    elif new_keyword_type == 'string':
                        new_keyword_value = argv[i]
                    elif new_keyword_type == 'file':
                        new_keyword_value = argv[i]
                    i += 1
            # Set
            else:
                if new_keyword_ndims > 0:
                    new_keyword_shape_new = []
                    for s in new_keyword_shape:
                        new_keyword_shape_new.append(s)
                    new_keyword_index = []
                    _n = -1
                    _l = 0
                    _u = 0
                    for n in range(new_keyword_ndims):
                        if i >= n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use.\n Processing the {"'
                            msg += '{}'.format(new_keyword)
                            msg += '"}:{"'
                            msg += '{}'.format(new_keyword_key)
                            msg += '"} input arguments failed.\n The '
                            if n == 0:
                                msg += 'first '
                            elif n == 1:
                                msg += 'second '
                            elif n == 2:
                                msg += 'third '
                            else:
                                msg += '{}th '.format(n + 1)
                            msg += 'index is missing from the input arguments.'
                            raise KIMPropertyError(msg)

                        arg = str(argv[i])
                        if re.match(r'^[1-9][0-9]*$', arg) is None:
                            if re.match(r'^[1-9][:0-9]*$', arg) is None:
                                msg = '\nERROR: input value '
                                msg += '"{}" doesn\'t meet '.format(arg)
                                msg += 'the format specification (an '
                                msg += 'integer equal to or greater than 1 '
                                msg += 'or integer indices range of '
                                msg += '"start:stop").'
                                raise KIMPropertyError(msg)
                            else:
                                if _n > -1:
                                    msg = '\nERROR: use of indices range is '
                                    msg += 'only accepted in one direction.'
                                    raise KIMPropertyError(msg)
                                _n = n
                                if arg.count(':') > 1:
                                    msg = '\nERROR: use of indices range as '
                                    msg += '"{}" '.format(arg)
                                    msg += 'is not accepted.\n'
                                    msg += 'The only supported indices range '
                                    msg += 'format is "start:stop".'
                                    raise KIMPropertyError(msg)
                                l, u = arg.split(':')
                                _l = int(l)
                                _u = int(u)
                                if _u < _l:
                                    msg = '\nERROR: use of indices range as '
                                    msg += '"{}" '.format(arg)
                                    msg += 'is not accepted.\n'
                                    msg += 'The only supported indices range '
                                    msg += 'format is "start:stop", where start '
                                    msg += 'is less or equal than stop.'
                                    raise KIMPropertyError(msg)
                                if new_keyword_shape[n] > 1 and \
                                        new_keyword_shape[n] < _u:
                                    msg = '\nERROR: this dimension has a '
                                    msg += 'fixed length = '
                                    msg += '{}'.format(new_keyword_shape[n])
                                    msg += ', while, wrong index = '
                                    msg += '{} is requested.\n '.format(_u)
                                    msg += 'Processing the {"'
                                    msg += '{}'.format(new_keyword)
                                    msg += '"}:{"'
                                    msg += '{}'.format(new_keyword_key)
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += 'at the {}th '.format(n + 1)
                                    msg += 'dimension is requested.'
                                    raise KIMPropertyError(msg)
                                if new_keyword_shape[n] == 1 and _u > 1:
                                    if property_def[new_keyword]["extent"][n] == ':':
                                        new_keyword_shape_new[n] = _u

                                _l -= 1
                                new_keyword_index.append(-1)
                        else:
                            if new_keyword_shape[n] > 1 and \
                                    new_keyword_shape[n] < int(arg):
                                msg = '\nERROR: this dimension has a fixed '
                                msg += 'length = '
                                msg += '{}, '.format(new_keyword_shape[n])
                                msg += 'while, wrong index = '
                                msg += '{} is requested.\n '.format(arg)
                                msg += 'Processing the {"'
                                msg += '{}'.format(new_keyword)
                                msg += '"}:{"'
                                msg += '{}'.format(new_keyword_key)
                                msg += '"} input arguments, wrong index at '
                                if n == 0:
                                    msg += 'the first '
                                elif n == 1:
                                    msg += 'the second '
                                elif n == 2:
                                    msg += 'the third '
                                else:
                                    msg += 'the {}th '.format(n + 1)
                                msg += 'dimension is requested.'
                                raise KIMPropertyError(msg)
                            if new_keyword_shape[n] == 1 and int(arg) > 1:
                                if property_def[new_keyword]["extent"][n] == ':':
                                    new_keyword_shape_new[n] = int(arg)
                                else:
                                    msg = '\nERROR: this dimension has a '
                                    msg += 'fixed length = 1, while, wrong '
                                    msg += 'index = {} '.format(arg)
                                    msg += 'is requested.\n '
                                    msg += 'Processing the {"'
                                    msg += '{}'.format(new_keyword)
                                    msg += '"}:{"'
                                    msg += '{}'.format(new_keyword_key)
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += 'at the {}th '.format(n + 1)
                                    msg += 'dimension is requested.'
                                    raise KIMPropertyError(msg)
                            new_keyword_index.append(int(arg) - 1)
                        i += 1

                    if new_keyword_type == 'int':
                        new_keyword_value = create_full_array(
                            new_keyword_shape_new, 0)
                    elif new_keyword_type == 'float':
                        new_keyword_value = create_full_array(
                            new_keyword_shape_new, 0.0)
                    elif new_keyword_type == 'bool':
                        new_keyword_value = create_full_array(
                            new_keyword_shape_new, False)
                    elif new_keyword_type == 'string':
                        new_keyword_value = create_full_array(
                            new_keyword_shape_new, '')
                    elif new_keyword_type == 'file':
                        new_keyword_value = create_full_array(
                            new_keyword_shape_new, '')

                    del(new_keyword_shape_new)

                    if _n > -1:
                        if i - 1 + _u - _l >= n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use.\n Processing the {"'
                            msg += '{}'.format(new_keyword)
                            msg += '"}:{"'
                            msg += '{}'.format(new_keyword_key)
                            msg += '"} input arguments failed.\n '
                            msg += 'We have {} '.format(n_arguments - i + 1)
                            msg += 'more input arguments while '
                            msg += 'at least {} arguments '.format(_u - _l)
                            msg += 'are required.'
                            raise KIMPropertyError(msg)

                        if new_keyword_ndims == 1:
                            if new_keyword_type == 'int':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = int(argv[i])
                                    i += 1
                            elif new_keyword_type == 'float':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = float(argv[i])
                                    i += 1
                            elif new_keyword_type == 'bool':
                                for d0 in range(_l, _u):
                                    if argv[i] == 'true' or \
                                            argv[i] == 'True' or argv[i]:
                                        new_keyword_value[d0] = True
                                    i += 1
                            elif new_keyword_type == 'string':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = argv[i]
                                    i += 1
                            elif new_keyword_type == 'file':
                                for d0 in range(_l, _u):
                                    new_keyword_value[d0] = argv[i]
                                    i += 1
                        elif new_keyword_ndims == 2:
                            d0, d1 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 3:
                            d0, d1, d2 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 4:
                            d0, d1, d2, d3 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 5:
                            d0, d1, d2, d3, d4 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if new_keyword_type == 'int':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                        elif new_keyword_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = new_keyword_index
                            if _n == 0:
                                if new_keyword_type == 'int':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d0 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if new_keyword_type == 'int':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d1 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if new_keyword_type == 'int':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d2 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if new_keyword_type == 'int':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d3 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 4:
                                if new_keyword_type == 'int':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d4 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            else:
                                if new_keyword_type == 'int':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'float':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif new_keyword_type == 'bool':
                                    for d5 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif new_keyword_type == 'string':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif new_keyword_type == 'file':
                                    for d5 in range(_l, _u):
                                        new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                    else:
                        if i >= n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use.\n Processing the {'
                            msg += '{}'.format(new_keyword)
                            msg += '}:{'
                            msg += '{}'.format(new_keyword_key)
                            msg += '} input arguments failed.\n '
                            msg += 'At least we need one further input.'
                            raise KIMPropertyError(msg)

                        if new_keyword_ndims == 1:
                            d0 = new_keyword_index[0]
                            if new_keyword_type == 'int':
                                new_keyword_value[d0] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0] = argv[i]
                        elif new_keyword_ndims == 2:
                            d0, d1 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1] = argv[i]
                        elif new_keyword_ndims == 3:
                            d0, d1, d2 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2] = int(argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2] = float(argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2] = argv[i]
                        elif new_keyword_ndims == 4:
                            d0, d1, d2, d3 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2][d3] = int(
                                    argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2][d3] = float(
                                    argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2][d3] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2][d3] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2][d3] = argv[i]
                        elif new_keyword_ndims == 5:
                            d0, d1, d2, d3, d4 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2][d3][d4] = int(
                                    argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2][d3][d4] = float(
                                    argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2][d3][d4] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2][d3][d4] = argv[i]
                        elif new_keyword_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = new_keyword_index
                            if new_keyword_type == 'int':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = int(
                                    argv[i])
                            elif new_keyword_type == 'float':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = float(
                                    argv[i])
                            elif new_keyword_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    new_keyword_value[d0][d1][d2][d3][d4][d5] = True
                            elif new_keyword_type == 'string':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                            elif new_keyword_type == 'file':
                                new_keyword_value[d0][d1][d2][d3][d4][d5] = argv[i]
                        i += 1
                else:
                    if new_keyword_type == 'int':
                        new_keyword_value = int(argv[i])
                    elif new_keyword_type == 'float':
                        new_keyword_value = float(argv[i])
                    elif new_keyword_type == 'bool':
                        if argv[i] == 'true' or \
                                argv[i] == 'True' or argv[i]:
                            new_keyword_value = True
                        else:
                            new_keyword_value = False
                    elif new_keyword_type == 'string':
                        new_keyword_value = argv[i]
                    elif new_keyword_type == 'file':
                        new_keyword_value = argv[i]
                    i += 1
        else:
            if new_keyword_key in new_keyword_map:
                msg = '\nERROR: the key {} '.format(new_keyword_key)
                msg += 'doesn\'t have any existing array argument. One can '
                msg += 'not append new data to keys with no extent.'
                raise KIMPropertyError(msg)

            if i >= n_arguments:
                msg = '\nERROR: there is not enough input arguments '
                msg += 'to use.\n Processing the {"'
                msg += '{}'.format(new_keyword)
                msg += '"}:{"'
                msg += '{}'.format(new_keyword_key)
                msg += '"} input arguments failed.\n '
                msg += 'At least we need one further input.'
                raise KIMPropertyError(msg)

            if new_keyword_key == 'source-unit':
                new_keyword_value = argv[i]
            elif new_keyword_key == 'si-unit':
                new_keyword_value = argv[i]
            elif new_keyword_key == 'coverage-factor':
                new_keyword_value = float(argv[i])
            elif new_keyword_key == 'source-asym-std-uncert-neg':
                new_keyword_value = float(argv[i])
            elif new_keyword_key == 'source-asym-std-uncert-pos':
                new_keyword_value = float(argv[i])
            elif new_keyword_key == 'source-asym-expand-uncert-neg':
                new_keyword_value = float(argv[i])
            elif new_keyword_key == 'source-asym-expand-uncert-pos':
                new_keyword_value = float(argv[i])
            elif new_keyword_key == 'uncert-lev-of-confid':
                new_keyword_value = float(argv[i])
            elif new_keyword_key == 'digits':
                new_keyword_value = int(argv[i])
            i += 1

        new_keyword_map[new_keyword_key] = new_keyword_value
        continue

    return kim_edn.dumps(kim_property_instances)
