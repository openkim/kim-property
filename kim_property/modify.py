"""Modify module."""

import re

import kim_edn

from .err import KIMPropertyError
from .numeric import shape, create_full_array, extend_full_array
from .definition import \
    get_optional_key_extent_ndimensions, \
    get_optional_key_extent_shape
from .instance import standard_keys, check_instance_id_format
from .create import get_properties

__all__ = [
    "kim_property_modify",
]


STANDARD_KEYS_WITH_EXTENT = (
    "source-value",
    "si-value",
    "source-std-uncert-value",
    "source-expand-uncert-value",
    "coverage-factor",
    "source-asym-std-uncert-neg",
    "source-asym-std-uncert-pos",
    "source-asym-expand-uncert-neg",
    "source-asym-expand-uncert-pos",
    "uncert-lev-of-confid",
    "digits",
)
"""tuple: KIM property standard keys which have the extent."""

# see https://github.com/openkim/kim-property/issues/3
STANDARD_KEYS_SCLAR_OR_WITH_EXTENT = (
    "source-std-uncert-value",
    "source-expand-uncert-value",
    "coverage-factor",
    "source-asym-std-uncert-neg",
    "source-asym-std-uncert-pos",
    "source-asym-expand-uncert-neg",
    "source-asym-expand-uncert-pos",
    "uncert-lev-of-confid",
    "digits",
)
"""tuple: KIM property standard keys values of the uncertainty and
          digits keys must be either arrays of the same extent, or
          scalars in which case they are taken to apply equally to
          all values in the source-value array."""


def kim_property_modify(property_instances, instance_id, *argv):  # noqa: C901
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
    >>> str = kim_property_modify(str, 1,
                "disclaimer", "This is an example disclaimer.")
    >>> str = kim_property_modify(str, 1,
                "key", "basis-atom-coordinates",
                "source-value", "3", "1:3", "0.5", "0.0", "0.5",
                "disclaimer", "This is an example disclaimer."
                "key", "basis-atom-coordinates",
                "source-value", "4", "2:3", "0.5", "0.5")

    Arguments:
        property_instances {string} -- A string containing the serialized
            KIM-EDN formatted property instances.
        instance_id {int} -- A positive integer identifying the property
            instance.

    Returns:
        string -- serialized KIM-EDN formatted property instances.

    """
    if property_instances in (None, 'None', '', '[]'):
        msg = 'there is no property instance to modify the content.'
        raise KIMPropertyError(msg)

    check_instance_id_format(instance_id)

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    a_property_instance = None

    for p in kim_property_instances:
        if "instance-id" not in p:
            msg = 'wrong input. The required "instance-id"-key is missing.'
            raise KIMPropertyError(msg)
        if p["instance-id"] == instance_id:
            a_property_instance = p
            break

    if a_property_instance is None:
        msg = f'the requested instance id :\n{instance_id}\n'
        msg += 'does not match any of the property instances ids.'
        raise KIMPropertyError(msg)

    if "property-id" not in a_property_instance:
        msg = 'wrong input. The required "property-id"-key is missing.\n'
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
    key = False

    # new keyword
    key_name = None
    key_name_map = {}

    i = 0
    while i < n_arguments:
        arg = argv[i]

        if arg == 'disclaimer':
            # key keyword
            key = False
            # new keyword
            key_name = None
            key_name_map = {}

            if i + 1 >= n_arguments:
                msg = f'there is not enough input arguments to use.\nProcessing '
                msg += 'the "disclaimer" optional key-value pair failed.'
                raise KIMPropertyError(msg)

            i += 1
            a_property_instance[arg] = argv[i]
            i += 1
            continue

        if arg == 'key':
            key = True
            i += 1
            continue

        if key:
            key = False

            # new keyword
            key_name = arg

            if key_name not in property_def:
                msg = f'wrong keyword. The input "{key_name}"-key '
                msg += 'is not defined in the property definition.\n'
                msg += f'({property_def["property-id"]})\n'
                msg += 'See the KIM Property Definitions at '
                msg += 'https://openkim.org/properties for more detailed '
                msg += 'information.'
                raise KIMPropertyError(msg)

            # Get the number of dimensions, shape and type of the key
            key_name_ndims = get_optional_key_extent_ndimensions(
                property_def[key_name]['extent'])
            key_name_shape = get_optional_key_extent_shape(
                property_def[key_name]['extent'])
            key_name_type = property_def[key_name]['type']

            if key_name in a_property_instance:
                key_name_map = a_property_instance[key_name]
            else:
                key_name_map = {}
                a_property_instance[key_name] = key_name_map

            i += 1
            continue

        if key_name is None:
            msg = f'"key name" is undefined. The input "{arg}" is a wrong '
            msg += 'input or the order needs to be corrected. First, the '
            msg += 'special keyword "key" should be given, followed by the '
            msg += 'property "key name".'
            raise KIMPropertyError(msg)

        key_name_key = arg
        i += 1

        if key_name_key not in standard_keys:
            msg = f'wrong key. The input "{key_name_key}"-key is '
            msg += 'not part of the standard key-value pairs definition.\n'
            msg += 'See KIM standard key-value pairs at '
            msg += 'https://openkim.org/doc/schema/properties-framework/ '
            msg += 'in section 3 for more detailed information.'
            raise KIMPropertyError(msg)

        if key_name_key == 'source-unit':
            if not property_def[key_name]['has-unit']:
                msg = 'wrong key. The unit is wrongly provided to a key '
                msg += 'that does not have a unit. The corresponding '
                msg += '"has-unit" key in the property definition has '
                msg += 'a `False` value.\n'
                msg += 'See the KIM Property Definitions at '
                msg += 'https://openkim.org/properties for more detailed '
                msg += 'information.'
                raise KIMPropertyError(msg)

        if key_name_key in STANDARD_KEYS_WITH_EXTENT:
            # Append
            if key_name_key in key_name_map:
                if key_name_ndims > 0:
                    if key_name_key in STANDARD_KEYS_SCLAR_OR_WITH_EXTENT:
                        key_name_value_is_scalar = False

                        if (i + 1) < n_arguments:
                            if argv[i + 1] == 'key' or \
                                    argv[i + 1] in standard_keys:
                                key_name_value_is_scalar = True
                        else:
                            try:
                                float(argv[i])
                                key_name_value_is_scalar = True
                            except (ValueError, TypeError, IndexError):
                                pass

                        if key_name_value_is_scalar:
                            if key_name_key == 'digits':
                                key_name_value = int(argv[i])
                                if key_name_value != float(argv[i]):
                                    msg = '"digits"-key is provided with a '
                                    msg += '`float` value. "digits"-key has '
                                    msg += 'an `int` type, and must be set '
                                    msg += 'to the number of reported digits.'
                                    raise KIMPropertyError(msg)
                            else:
                                key_name_value = float(argv[i])

                            i += 1

                            key_name_map[key_name_key] = key_name_value
                            continue
                        else:
                            # Convert a scalar value to an array with extent
                            key_name_value = key_name_map[key_name_key]
                            if isinstance(key_name_value, int) or \
                                    isinstance(key_name_value, float):
                                key_name_map[key_name_key] = [key_name_value]

                    key_name_value = key_name_map[key_name_key]
                    key_name_shape_new = shape(key_name_value)
                    key_name_index = []
                    _n = -1
                    _l = 0
                    _u = 0
                    for n in range(key_name_ndims):
                        if i >= n_arguments:
                            msg = 'there is not enough input '
                            msg += 'arguments to use.\nProcessing the {"'
                            msg += f'{key_name}"}}:{{"{key_name_key}'
                            msg += '"} input arguments failed.\nThe '
                            if n == 0:
                                msg += 'first '
                            elif n == 1:
                                msg += 'second '
                            elif n == 2:
                                msg += 'third '
                            else:
                                msg += f'{n + 1}th '
                            msg += 'index is missing from the input '
                            msg += 'arguments.'
                            raise KIMPropertyError(msg)

                        arg = str(argv[i])
                        if re.match(r'^[1-9][0-9]*$', arg) is None:
                            if re.match(r'^[1-9][:0-9]*$', arg) is None:
                                msg = 'requested index '
                                msg += f'"{arg}" doesn\'t meet the format '
                                msg += 'specification. An integer equal to '
                                msg += 'or greater than 1 or integer '
                                msg += 'indices range of "start:stop".'
                                raise KIMPropertyError(msg)
                            else:
                                if _n > -1:
                                    msg = 'for multidimensional '
                                    msg += 'arrays, only one '
                                    msg += 'colon-separated range is '
                                    msg += 'allowed in the index listing.'
                                    raise KIMPropertyError(msg)
                                _n = n
                                if arg.count(':') > 1:
                                    msg = 'use of indices range as '
                                    msg += f'"{arg}" is not accepted.\n'
                                    msg += 'The only supported indices '
                                    msg += 'range format is "start:stop".'
                                    raise KIMPropertyError(msg)
                                l, u = arg.split(':')
                                _l = int(l)
                                _u = int(u)
                                if _u < _l:
                                    msg = 'use of indices range as '
                                    msg += f'"{arg}" is not accepted.\n'
                                    msg += 'The only supported indices '
                                    msg += 'range format is "start:stop", '
                                    msg += 'where start is less or equal '
                                    msg += 'than stop.'
                                    raise KIMPropertyError(msg)
                                if key_name_shape[n] > 1 and \
                                        key_name_shape[n] < _u:
                                    msg = 'this dimension has a fixed '
                                    msg += f'length = {key_name_shape[n]}'
                                    msg += f', while, wrong index = {_u} '
                                    msg += 'is requested.\nProcessing the {"'
                                    msg += f'{key_name}"}}:{{"{key_name_key}'
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += f'at the {n + 1}th '
                                    msg += 'dimension is requested.'
                                    raise KIMPropertyError(msg)
                                if key_name_shape[n] == 1 and _u > 1:
                                    if property_def[key_name]["extent"][n] == ':':
                                        if key_name_shape_new[n] < _u:
                                            key_name_shape_new[n] = _u

                                _l -= 1
                                key_name_index.append(-1)
                        else:
                            if key_name_shape[n] > 1 and \
                                    key_name_shape[n] < int(arg):
                                msg = 'this dimension has a fixed '
                                msg += f'length = {key_name_shape[n]}'
                                msg += f', while, wrong index = {arg} '
                                msg += 'is requested.\nProcessing the {"'
                                msg += f'{key_name}"}}:{{"{key_name_key}'
                                msg += '"} input arguments, wrong index '
                                if n == 0:
                                    msg += 'at the first '
                                elif n == 1:
                                    msg += 'at the second '
                                elif n == 2:
                                    msg += 'at the third '
                                else:
                                    msg += f'at the {n + 1}th '
                                msg += 'dimension is requested.'
                                raise KIMPropertyError(msg)
                            if key_name_shape[n] == 1 and int(arg) > 1:
                                if property_def[key_name]["extent"][n] == ':':
                                    if key_name_shape_new[n] < int(arg):
                                        key_name_shape_new[n] = int(arg)
                                else:
                                    msg = 'this dimension has a '
                                    msg += 'fixed length = 1, while, wrong '
                                    msg += f'index = {arg} is requested.\n'
                                    msg += f'Processing the {{"{key_name}"}}'
                                    msg += f':{{"{key_name_key}"}} input '
                                    msg += 'arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += f'at the {n + 1}th '
                                    msg += 'dimension is requested.'

                                    raise KIMPropertyError(msg)
                            key_name_index.append(int(arg) - 1)
                        i += 1

                    digits_key_name_type = key_name_type
                    if key_name_key == 'digits':
                        key_name_type = 'int'

                    if key_name_type == 'int':
                        key_name_value = extend_full_array(
                            key_name_value, key_name_shape_new, 0)
                    elif key_name_type == 'float':
                        key_name_value = extend_full_array(
                            key_name_value, key_name_shape_new, 0.0)
                    elif key_name_type == 'bool':
                        key_name_value = extend_full_array(
                            key_name_value, key_name_shape_new, False)
                    elif key_name_type == 'string':
                        key_name_value = extend_full_array(
                            key_name_value, key_name_shape_new, '')
                    elif key_name_type == 'file':
                        key_name_value = extend_full_array(
                            key_name_value, key_name_shape_new, '')

                    del key_name_shape_new

                    if _n > -1:
                        if i - 1 + _u - _l >= n_arguments:
                            msg = 'there is not enough input '
                            msg += 'arguments to use.\nProcessing the {"'
                            msg += f'{key_name}"}}:{{"{key_name_key}'
                            msg += '"} input arguments failed.\n'
                            msg += f'We have {n_arguments - i + 1} '
                            msg += 'more input arguments while at least '
                            msg += f'{_u - _l} arguments are required.'
                            raise KIMPropertyError(msg)

                        if key_name_ndims == 1:
                            if key_name_type == 'int':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = int(argv[i])
                                    i += 1
                            elif key_name_type == 'float':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = float(argv[i])
                                    i += 1
                            elif key_name_type == 'bool':
                                for d0 in range(_l, _u):
                                    if argv[i] == 'true' or \
                                            argv[i] == 'True' or argv[i]:
                                        key_name_value[d0] = True
                                    i += 1
                            elif key_name_type == 'string':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = argv[i]
                                    i += 1
                            elif key_name_type == 'file':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = argv[i]
                                    i += 1
                        elif key_name_ndims == 2:
                            d0, d1 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                        elif key_name_ndims == 3:
                            d0, d1, d2 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                        elif key_name_ndims == 4:
                            d0, d1, d2, d3 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                        elif key_name_ndims == 5:
                            d0, d1, d2, d3, d4 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if key_name_type == 'int':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                        elif key_name_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if key_name_type == 'int':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 4:
                                if key_name_type == 'int':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d5 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                    else:
                        if i >= n_arguments:
                            msg = 'there is not enough input '
                            msg += 'arguments to use.\nProcessing the {"'
                            msg += f'{key_name}"}}:{{"{key_name_key}'
                            msg += '"} input arguments failed.\n'
                            msg += 'At least we need one further input.'
                            raise KIMPropertyError(msg)

                        if key_name_ndims == 1:
                            d0 = key_name_index[0]
                            if key_name_type == 'int':
                                key_name_value[d0] = int(argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0] = float(argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0] = True
                            elif key_name_type == 'string':
                                key_name_value[d0] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0] = argv[i]
                        elif key_name_ndims == 2:
                            d0, d1 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1] = int(argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1] = float(argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1] = argv[i]
                        elif key_name_ndims == 3:
                            d0, d1, d2 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2] = int(argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2] = float(argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2] = argv[i]
                        elif key_name_ndims == 4:
                            d0, d1, d2, d3 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2][d3] = int(
                                    argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2][d3] = float(
                                    argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2][d3] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2][d3] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2][d3] = argv[i]
                        elif key_name_ndims == 5:
                            d0, d1, d2, d3, d4 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2][d3][d4] = int(
                                    argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2][d3][d4] = float(
                                    argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2][d3][d4] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2][d3][d4] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2][d3][d4] = argv[i]
                        elif key_name_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                    argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                    argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2][d3][d4][d5] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                        i += 1

                    if key_name_key == 'digits':
                        key_name_type = digits_key_name_type
                else:
                    if key_name_key in STANDARD_KEYS_SCLAR_OR_WITH_EXTENT:
                        if key_name_key == 'digits':
                            key_name_value = int(argv[i])
                            if key_name_value != float(argv[i]):
                                msg = '"digits"-key is provided with a `float` value. '
                                msg += '"digits"-key has an `int` type, and must be '
                                msg += 'set to the number of reported digits.'
                                raise KIMPropertyError(msg)
                        else:
                            key_name_value = float(argv[i])
                    else:
                        if key_name_type == 'int':
                            key_name_value = int(argv[i])
                        elif key_name_type == 'float':
                            key_name_value = float(argv[i])
                        elif key_name_type == 'bool':
                            if argv[i] == 'true' or \
                                    argv[i] == 'True' or argv[i]:
                                key_name_value = True
                            else:
                                key_name_value = False
                        elif key_name_type == 'string':
                            key_name_value = argv[i]
                        elif key_name_type == 'file':
                            key_name_value = argv[i]
                    i += 1

                    # Extra check for the scalar values
                    # see https://github.com/openkim/kim-property/issues/1
                    if i < n_arguments:
                        arg = argv[i]
                        if arg != 'key' and arg not in standard_keys:
                            msg = 'two arguments are provided for a scalar '
                            msg += f'key. For "{key_name}" in property-'
                            msg += f'definition, the "{key_name_key}"-key '
                            msg += 'is scalar, but is provided with two '
                            msg += f'arguments: "{argv[i - 1]}", "{arg}" (Note'
                            msg += ': one can not use index for scalar keys.)'
                            raise KIMPropertyError(msg)
            # Set
            else:
                if key_name_ndims > 0:
                    if key_name_key in STANDARD_KEYS_SCLAR_OR_WITH_EXTENT:
                        key_name_value_is_scalar = False

                        if (i + 1) < n_arguments:
                            if argv[i + 1] == 'key' or \
                                    argv[i + 1] in standard_keys:
                                key_name_value_is_scalar = True
                        else:
                            try:
                                float(argv[i])
                                key_name_value_is_scalar = True
                            except (ValueError, TypeError, IndexError):
                                pass

                        if key_name_value_is_scalar:
                            if key_name_key == 'digits':
                                key_name_value = int(argv[i])
                                if key_name_value != float(argv[i]):
                                    msg = '"digits"-key is provided with a '
                                    msg += '`float` value. "digits"-key has '
                                    msg += 'an `int` type, and must be set '
                                    msg += 'to the number of reported digits.'
                                    raise KIMPropertyError(msg)
                            else:
                                key_name_value = float(argv[i])
                            i += 1

                            key_name_map[key_name_key] = key_name_value
                            continue

                    key_name_shape_new = []
                    for s in key_name_shape:
                        key_name_shape_new.append(s)
                    key_name_index = []
                    _n = -1
                    _l = 0
                    _u = 0
                    for n in range(key_name_ndims):
                        if i >= n_arguments:
                            msg = 'there is not enough input '
                            msg += 'arguments to use.\nProcessing the {"'
                            msg += f'{key_name}"}}:{{"{key_name_key}"}} '
                            msg += 'input arguments failed.\nThe '
                            if n == 0:
                                msg += 'first '
                            elif n == 1:
                                msg += 'second '
                            elif n == 2:
                                msg += 'third '
                            else:
                                msg += f'{n + 1}th '
                            msg += 'index is missing from the input arguments.'
                            raise KIMPropertyError(msg)

                        arg = str(argv[i])
                        if re.match(r'^[1-9][0-9]*$', arg) is None:
                            if re.match(r'^[1-9][:0-9]*$', arg) is None:
                                msg = f'input value "{arg}" doesn\'t meet '
                                msg += 'the format specification. An integer '
                                msg += 'equal to or greater than 1 or integer '
                                msg += 'indices range of "start:stop".'
                                raise KIMPropertyError(msg)
                            else:
                                if _n > -1:
                                    msg = 'for multidimensional arrays, only '
                                    msg += 'one colon-separated range is '
                                    msg += 'allowed in the index listing.'
                                    raise KIMPropertyError(msg)
                                _n = n
                                if arg.count(':') > 1:
                                    msg = 'use of indices range as '
                                    msg += f'"{arg}" is not accepted.\nThe '
                                    msg += 'only supported indices range '
                                    msg += 'format is "start:stop".'
                                    raise KIMPropertyError(msg)
                                l, u = arg.split(':')
                                _l = int(l)
                                _u = int(u)
                                if _u < _l:
                                    msg = 'use of indices range as '
                                    msg += f'"{arg}" is not accepted.\nThe '
                                    msg += 'only supported indices range '
                                    msg += 'fomrat is "start:stop", where '
                                    msg += 'start is less or equal than stop.'
                                    raise KIMPropertyError(msg)
                                if key_name_shape[n] > 1 and \
                                        key_name_shape[n] < _u:
                                    msg = 'this dimension has a fixed '
                                    msg += f'length = {key_name_shape[n]}'
                                    msg += f', while, wrong index = {_u} is '
                                    msg += 'requested.\nProcessing the {"'
                                    msg += f'{key_name}"}}:{{"{key_name_key}'
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += f'at the {n + 1}th '
                                    msg += 'dimension is requested.'
                                    raise KIMPropertyError(msg)
                                if key_name_shape[n] == 1 and _u > 1:
                                    if property_def[key_name]["extent"][n] == ':':
                                        key_name_shape_new[n] = _u

                                _l -= 1
                                key_name_index.append(-1)
                        else:
                            if key_name_shape[n] > 1 and \
                                    key_name_shape[n] < int(arg):
                                msg = 'this dimension has a fixed '
                                msg += f'length = {key_name_shape[n]}, while, '
                                msg += f'wrong index = {arg} is requested.\n'
                                msg += f'Processing the {{"{key_name}"}}:{{"'
                                msg += f'{key_name_key}"}} input arguments, '
                                msg += 'wrong index at '
                                if n == 0:
                                    msg += 'the first '
                                elif n == 1:
                                    msg += 'the second '
                                elif n == 2:
                                    msg += 'the third '
                                else:
                                    msg += f'the {n + 1}th '
                                msg += 'dimension is requested.'
                                raise KIMPropertyError(msg)
                            if key_name_shape[n] == 1 and int(arg) > 1:
                                if property_def[key_name]["extent"][n] == ':':
                                    key_name_shape_new[n] = int(arg)
                                else:
                                    msg = 'this dimension has a fixed length '
                                    msg += f'= 1, while, wrong index = {arg} '
                                    msg += 'is requested.\nProcessing the {"'
                                    msg += f'{key_name}"}}:{{"{key_name_key}'
                                    msg += '"} input arguments, wrong index '
                                    if n == 0:
                                        msg += 'at the first '
                                    elif n == 1:
                                        msg += 'at the second '
                                    elif n == 2:
                                        msg += 'at the third '
                                    else:
                                        msg += f'at the {n + 1}th '
                                    msg += 'dimension is requested.'
                                    raise KIMPropertyError(msg)
                            key_name_index.append(int(arg) - 1)
                        i += 1

                    digits_key_name_type = key_name_type
                    if key_name_key == 'digits':
                        key_name_type = 'int'

                    if key_name_type == 'int':
                        key_name_value = create_full_array(
                            key_name_shape_new, 0)
                    elif key_name_type == 'float':
                        key_name_value = create_full_array(
                            key_name_shape_new, 0.0)
                    elif key_name_type == 'bool':
                        key_name_value = create_full_array(
                            key_name_shape_new, False)
                    elif key_name_type == 'string':
                        key_name_value = create_full_array(
                            key_name_shape_new, '')
                    elif key_name_type == 'file':
                        key_name_value = create_full_array(
                            key_name_shape_new, '')

                    del key_name_shape_new

                    if _n > -1:
                        if i - 1 + _u - _l >= n_arguments:
                            msg = 'there is not enough input arguments'
                            msg += f'to use.\nProcessing the {{"{key_name}"}}'
                            msg += f':{{"{key_name_key}"}} input arguments '
                            msg += f'failed.\nWe have {n_arguments - i + 1} '
                            msg += 'more input arguments while at least '
                            msg += f'{_u - _l} arguments are required.'
                            raise KIMPropertyError(msg)

                        if key_name_ndims == 1:
                            if key_name_type == 'int':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = int(argv[i])
                                    i += 1
                            elif key_name_type == 'float':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = float(argv[i])
                                    i += 1
                            elif key_name_type == 'bool':
                                for d0 in range(_l, _u):
                                    if argv[i] == 'true' or \
                                            argv[i] == 'True' or argv[i]:
                                        key_name_value[d0] = True
                                    i += 1
                            elif key_name_type == 'string':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = argv[i]
                                    i += 1
                            elif key_name_type == 'file':
                                for d0 in range(_l, _u):
                                    key_name_value[d0] = argv[i]
                                    i += 1
                        elif key_name_ndims == 2:
                            d0, d1 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1] = argv[i]
                                        i += 1
                        elif key_name_ndims == 3:
                            d0, d1, d2 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2] = argv[i]
                                        i += 1
                        elif key_name_ndims == 4:
                            d0, d1, d2, d3 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3] = argv[i]
                                        i += 1
                        elif key_name_ndims == 5:
                            d0, d1, d2, d3, d4 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if key_name_type == 'int':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4] = argv[i]
                                        i += 1
                        elif key_name_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = key_name_index
                            if _n == 0:
                                if key_name_type == 'int':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d0 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d0 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 1:
                                if key_name_type == 'int':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d1 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d1 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 2:
                                if key_name_type == 'int':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d2 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d2 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 3:
                                if key_name_type == 'int':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d3 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d3 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            elif _n == 4:
                                if key_name_type == 'int':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d4 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d4 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                            else:
                                if key_name_type == 'int':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'float':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                            argv[i])
                                        i += 1
                                elif key_name_type == 'bool':
                                    for d5 in range(_l, _u):
                                        if argv[i] == 'true' or \
                                                argv[i] == 'True' or argv[i]:
                                            key_name_value[d0][d1][d2][d3][d4][d5] = True
                                        i += 1
                                elif key_name_type == 'string':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                                elif key_name_type == 'file':
                                    for d5 in range(_l, _u):
                                        key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                                        i += 1
                    else:
                        if i >= n_arguments:
                            msg = 'there is not enough input arguments to use.'
                            msg += f'\nProcessing the {{{key_name}}}:{{'
                            msg += f'{key_name_key}}} input arguments failed.'
                            msg += '\nAt least we need one further input.'
                            raise KIMPropertyError(msg)

                        if key_name_ndims == 1:
                            d0 = key_name_index[0]
                            if key_name_type == 'int':
                                key_name_value[d0] = int(argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0] = float(argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0] = True
                            elif key_name_type == 'string':
                                key_name_value[d0] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0] = argv[i]
                        elif key_name_ndims == 2:
                            d0, d1 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1] = int(argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1] = float(argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1] = argv[i]
                        elif key_name_ndims == 3:
                            d0, d1, d2 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2] = int(argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2] = float(argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2] = argv[i]
                        elif key_name_ndims == 4:
                            d0, d1, d2, d3 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2][d3] = int(
                                    argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2][d3] = float(
                                    argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2][d3] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2][d3] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2][d3] = argv[i]
                        elif key_name_ndims == 5:
                            d0, d1, d2, d3, d4 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2][d3][d4] = int(
                                    argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2][d3][d4] = float(
                                    argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2][d3][d4] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2][d3][d4] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2][d3][d4] = argv[i]
                        elif key_name_ndims == 6:
                            d0, d1, d2, d3, d4, d5 = key_name_index
                            if key_name_type == 'int':
                                key_name_value[d0][d1][d2][d3][d4][d5] = int(
                                    argv[i])
                            elif key_name_type == 'float':
                                key_name_value[d0][d1][d2][d3][d4][d5] = float(
                                    argv[i])
                            elif key_name_type == 'bool':
                                if argv[i] == 'true' or \
                                        argv[i] == 'True' or argv[i]:
                                    key_name_value[d0][d1][d2][d3][d4][d5] = True
                            elif key_name_type == 'string':
                                key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                            elif key_name_type == 'file':
                                key_name_value[d0][d1][d2][d3][d4][d5] = argv[i]
                        i += 1

                    if key_name_key == 'digits':
                        key_name_type = digits_key_name_type
                else:
                    if key_name_key in STANDARD_KEYS_SCLAR_OR_WITH_EXTENT:
                        if key_name_key == 'digits':
                            key_name_value = int(argv[i])
                            if key_name_value != float(argv[i]):
                                msg = '"digits"-key is provided with a `float` value. '
                                msg += '"digits"-key has an `int` type, and must be '
                                msg += 'set to the number of reported digits.'
                                raise KIMPropertyError(msg)
                        else:
                            key_name_value = float(argv[i])
                    else:
                        if key_name_type == 'int':
                            key_name_value = int(argv[i])
                        elif key_name_type == 'float':
                            key_name_value = float(argv[i])
                        elif key_name_type == 'bool':
                            if argv[i] == 'true' or \
                                    argv[i] == 'True' or argv[i]:
                                key_name_value = True
                            else:
                                key_name_value = False
                        elif key_name_type == 'string':
                            key_name_value = argv[i]
                        elif key_name_type == 'file':
                            key_name_value = argv[i]
                    i += 1

                    # Extra check for the scalar values
                    # see https://github.com/openkim/kim-property/issues/1
                    if i < n_arguments:
                        arg = argv[i]
                        if arg != 'key' and arg not in standard_keys:
                            msg = 'two arguments are provided for a scalar key'
                            msg += f'. For "{key_name}" in property-definition'
                            msg += f', the "{key_name_key}"-key is scalar, but'
                            msg += ' is provided with two arguments: "'
                            msg += f'{argv[i - 1]}", "{arg}" (Note: one can '
                            msg += 'not use index for scalar keys.)'
                            raise KIMPropertyError(msg)
        else:
            if i >= n_arguments:
                msg = 'there is not enough input arguments to use.\nProcessing'
                msg += f' the {{"{key_name}"}}:{{"{key_name_key}"}} input '
                msg += 'arguments failed.\nAt least we need one further input.'
                raise KIMPropertyError(msg)

            if key_name_key == 'source-unit':
                key_name_value = argv[i]
            elif key_name_key == 'si-unit':
                key_name_value = argv[i]
            i += 1

            # Extra check for the scalar values
            # see https://github.com/openkim/kim-property/issues/1
            if i < n_arguments:
                arg = argv[i]
                if arg != 'key' and arg not in standard_keys:
                    msg = 'two arguments are provided for a key with no '
                    msg += f'extent. For "{key_name}" in property-definition, '
                    msg += f'the "{key_name_key}"-key has no extent, but is '
                    msg += f'provided with two arguments: "{argv[i - 1]}", '
                    msg += f'"{arg}" (Note: one can not use index for keys '
                    msg += 'with no extent.)'
                    raise KIMPropertyError(msg)

        key_name_map[key_name_key] = key_name_value
        continue

    return kim_edn.dumps(kim_property_instances)
