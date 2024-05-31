
"""Instance validator."""

from os.path import abspath, isabs, join, isdir, isfile
import re

import kim_edn

from .err import KIMPropertyError
from .definition import required_keys as def_required_keys
from .definition import \
    check_property_id_format, \
    check_required_keys_present, \
    check_key_format, \
    check_optional_key_extent_scalar, \
    get_optional_key_extent_ndimensions
from .numeric import shape

__all__ = [
    "required_keys",
    "optional_keys",
    "standard_keys",
    "get_property_id_path",
    "check_instance_id_format",
    "check_optional_key_source_value_scalar",
    "get_optional_key_source_value_ndimensions",
    "check_instance_optional_key_standard_pairs_format",
    "check_instance_optional_key_map",
    "check_instance_optional_key_marked_required_are_present",
    "check_property_instances",
]


# A Property Instance must contain the following required key-value pairs:
required_keys = ("property-id", "instance-id")

# A Property Instance may contain the following optional key-value pairs:
optional_keys = (
    # A string containing an optional statement of applicability of the data
    # contained in this Property Instance. For a Prediction, this can be
    # provided by the Test, while for an item of Reference Data, this can be
    # provided by the contributor.
    "disclaimer",
)

# The required fields list above are followed by an unordered set of
# key-map pairs. Each key is associated with a map which must contain
# the following standard keys-value pairs:
standard_keys = (
    # A string, float, integer, boolean, or file name string (depending on
    # the specification in Property Definition) providing the contents
    # (value) of the variable. This variable will either be a scalar or an
    # array of specified extent as defined in the Property Definition. Note
    # that file names should be given relative to the Test Result,
    # Verification Result, or Error parent directory rather than as
    # absolute paths.
    "source-value",
    # A string defining the physical units of the variable in notation
    # conforming to the GNU units command. (This key is only required if
    # the corresponding has-unit key in the Property Definition has value
    # true.)
    "source-unit",
    # For numerical values, a machine-generated translation of the
    # source-value to SI units. A Test should not provide this information.
    "si-value",
    # For numerical values,the standard SI unit corresponding to
    # source-unit. A Test should not provide this information.
    "si-unit",
    # A float set to the numerical standard uncertainty value u. (u
    # represents one standard deviation.)
    "source-std-uncert-value",
    # A float set to the expanded uncertainty value U defined as the
    # “interval about the result of a measurement that may be expected to
    # encompass a large fraction of the distribution of values that could
    # reasonably be attributed to the measurand”.
    "source-expand-uncert-value",
    # A float set to the coverage factor k. The coverage factor k is a
    # numerical factor which is the multiplier of the standard uncertainty
    # in order to obtain an expanded uncertainty (i.e. U = ku).
    "coverage-factor",
    # A float set to the variable u− associated with a standard uncertainty
    # that is asymmetric about the key value y, with a range
    # [y − u−, y + u+].
    "source-asym-std-uncert-neg",
    # A float set to the variable u+ associated with a standard uncertainty
    # that is asymmetric about the key value yp, with a range
    # [y − u−, y + u+].
    "source-asym-std-uncert-pos",
    # A float set to the variable U− associated with an expanded
    # uncertainty that is asymmetric about the key value y, with a range
    # [y − U−,y + U+].
    "source-asym-expand-uncert-neg",
    # A float set to the variable U+ associated with an expanded
    # uncertainty that is asymmetric about the key value y, with a range
    # [y − U−,y + U+].
    "source-asym-expand-uncert-pos",
    # A float set to the level of confidence L associated with the expanded
    # uncertainty U. The level of confidence is expressed as a percentage.
    "uncert-lev-of-confid",
    # An integer set to the number of reported digits.
    "digits"
)

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL


def get_property_id_path(property_id):
    """Get the property id relative path.

    Arguments:
        property_id {string} -- A string containing the unique ID of the
            property.

    Returns:
        {string} -- relative path, email, date, and property name

    """
    check_property_id_format(property_id)

    _email = re.sub(r',$', '', re.sub(
        r'tag:', '', re.findall(r'^tag:[^+^A-Z]*@[^+^A-Z]*,', property_id)[0]))
    _date = re.sub(r':property$', '', re.sub(
        r'^,', '', re.findall(r',\d{4}-\d{2}-\d{2}:property', property_id)[0]))
    _property_name = re.sub(
        r'^property/', '',
        re.findall(r'property/[a-z0-9\-]*$', property_id)[0])

    _path = join(_property_name, _date + '-' + _email, _property_name + '.edn')

    return _path, _email, _date, _property_name


INSTANCE_ID = re.compile(r'^[1-9][0-9]*$')


def check_instance_id_format(instance_id, _m=INSTANCE_ID.match):
    """Check the instance id format.

    Check the instance-id is a positive integer.

    Arguments:
        instance_id {int} -- A positive integer identifying the instance.

    """
    if isinstance(instance_id, int):
        if _m(str(instance_id)) is None:
            msg = f'the "instance-id" = {instance_id}, doesn\'t meet the '
            msg += 'format specification (an integer equal to or '
            msg += 'greater than 1).'
            raise KIMPropertyError(msg)
        return

    msg = 'the "instance-id" value is not an `int` and doesn\'t meet the '
    msg += 'format specification.'
    raise KIMPropertyError(msg)


# checks for optional keys

def check_optional_key_source_value_scalar(source_value_key, value_type):
    """Check optional key "source-value" specifies a single item value.

    Arguments:
        source_value_key {list or any of value_type type} -- input
            "source-value"-key value
        value_type {string} -- value type, one of "string", "float", "int",
            "bool", "file"

    Returns:
        bool -- True if the optional key "source_value" has scalar value

    """
    if isinstance(source_value_key, list):
        return False

    if isinstance(source_value_key, str):
        return value_type in ("string", "file")

    if isinstance(source_value_key, bool):
        return value_type == "bool"

    if isinstance(source_value_key, float):
        return value_type == "float"

    if isinstance(source_value_key, int):
        # 0 and 1 are special cases
        if source_value_key in (0, 1):
            return value_type in ("int", "float", 'bool')
        return value_type in ("int", "float")

    msg = 'input to the function doesn\'t comply with '
    msg += 'the defined variable type.\n'
    msg += 'The variable type can be one of ::\n'
    msg += '`string`, `float`, `int`, `bool`, or `file`.'
    raise KIMPropertyError(msg)


def get_optional_key_source_value_ndimensions(source_value_key, _shape=shape):
    """Get the number of dimensions specified by optional key "source-value".

    Arguments:
        source_value_key {list or str or int or float or bool} -- input
            "source_value"-key value

    Returns:
        int -- Number of dimensions

    """
    if isinstance(source_value_key, list):
        return len(_shape(source_value_key))

    if isinstance(source_value_key, (str, bool, float, int)):
        return 0

    msg = 'input to the function is not any of:: \n'
    msg += '`list`, `str`, `float`, `int`, `bool` types.'
    raise KIMPropertyError(msg)


def check_instance_optional_key_standard_pairs_format(property_instance_map,
                                                      property_definition_map):
    """Check the standard key-map pairs correctness and format.

    The required fields are followed by an unordered set of key-map pairs.
    Each key is associated with a map which must contain the following
    standard keys-value pairs:
    "source-value", "source-unit", "si-value", "si-unit",
    "source-std-uncert-value", "source-expand-uncert-value",
    "coverage-factor", "source-asym-std-uncert-neg",
    "source-asym-std-uncert-pos", "source-asym-expand-uncert-neg",
    "source-asym-expand-uncert-pos", "uncert-lev-of-confid", "digits"

    Arguments:
        property_instance_map {dict} -- property instance map
            (key-value pairs)
        property_definition_map {dict} -- property definition map
            (key-value pairs)

    """
    if not isinstance(property_instance_map, dict):
        msg = 'property instance input to the function is not a `dict`.'
        raise KIMPropertyError(msg)

    for k in property_instance_map:
        if k not in standard_keys:
            msg = f'wrong key.\nThe input "{k}"-key is not part of '
            msg += 'the standard key-value pairs definition.\n'
            msg += 'See KIM standard key-value pairs at '
            msg += 'https://openkim.org/doc/schema/properties-framework/ '
            msg += 'in section 3 for more detailed information.'
            raise KIMPropertyError(msg)

    # Check the required fields in the instance property optional field
    # key-value pairs
    if "source-value" not in property_instance_map:
        msg = '"source-value" is required, but it is not included in the '
        msg += 'current input property instance.'
        raise KIMPropertyError(msg)

    if property_definition_map is not None:
        if not isinstance(property_definition_map, dict):
            msg = 'property map input to the function is not a `dict`.'
            raise KIMPropertyError(msg)

        l_i = property_instance_map["source-value"]
        l_p = property_definition_map["extent"]
        t_p = property_definition_map["type"]

        if check_optional_key_extent_scalar(l_p):
            if not check_optional_key_source_value_scalar(l_i, t_p):
                msg = '"extent" specifies single item, but "source-value" '
                msg += 'in the property instance is an array of values.'
                raise KIMPropertyError(msg)
        else:
            instance_ndims = get_optional_key_source_value_ndimensions(l_i)
            property_ndims = get_optional_key_extent_ndimensions(l_p)

            if instance_ndims != property_ndims:
                msg = '"source-value"-value number of dimensions = '
                msg += f'{instance_ndims}, doesn\'t match '
                msg += 'the "extent"-value number of dimensions = '
                msg += f'{property_ndims}.'
                raise KIMPropertyError(msg)

        del l_i
        del l_p
        del t_p

        if property_definition_map["has-unit"]:
            if "source-unit" not in property_instance_map:
                msg = '"source-unit" is required, but it is not in the '
                msg += 'property instance optional field "key-value" pairs.'
                raise KIMPropertyError(msg)
        else:
            if "source-unit" in property_instance_map:
                msg = '"source-unit" is wrongly provided.\nThe corresponding '
                msg += '"has-unit" key in the property definition has '
                msg += 'a `False` value.'
                raise KIMPropertyError(msg)


# A key is a string. Key names can only include lower-case alphanumeric
# characters and dashes. The names are arbitrary and set by the developer
# to reflect the meaning of the key.
KEY_FORMAT = re.compile(r'^[a-z0-9\-].*$', FLAGS)


def check_instance_optional_key_map(property_instance_key,
                                    property_instance_map,
                                    property_definition_map=None,
                                    _m=KEY_FORMAT.match):
    """Check inctances optional fields key-map pairs correctness and format.

    Optional fields must be an unordered set of key-map pairs.

    Arguments:
        property_instance_key {string} -- key, property instance keyword.
        property_instance_map {dict} -- map, property instance key-value pairs.
        property_definition_map {dict} -- property definition key-value pairs.
            (default None)

    """
    try:
        check_key_format(property_instance_key, _m=_m)
        check_instance_optional_key_standard_pairs_format(
            property_instance_map, property_definition_map)
    except KIMPropertyError:
        msg = f'in property instance key = "{property_instance_key}"\n'
        msg += str(KIMPropertyError)
        raise KIMPropertyError(msg)


def check_instance_optional_key_marked_required_are_present(
        property_instance,
        property_definition):
    """Check the optional variable marked required is present.

    In the property definition, a "required" key indicates whether the
    variable must be reported in every property instance of the property or
    not. This function check all the optional variable marked required in the
    property definition are present or not.

    Arguments:
        property_instance {dict} -- property instance
        property_definition {dict} -- property definition

    """
    if not isinstance(property_instance, dict):
        msg = 'property instance is not a dict.'
        raise KIMPropertyError(msg)

    if not isinstance(property_definition, dict):
        msg = 'property definition is not a dict.'
        raise KIMPropertyError(msg)

    for k in property_definition:
        if k not in def_required_keys:
            if property_definition[k]["required"]:
                if k not in property_instance:
                    msg = f'variable "{k}" is marked required in the '
                    msg += 'property definition, but it is not present in '
                    msg += 'the property instance.\nA "required" flag in the '
                    msg += 'property definition indicates the variable '
                    msg += f'"{k}" must be in the property-instance '
                    msg += 'of the property.'
                    raise KIMPropertyError(msg)


def check_property_instances(fi, fp=None, fp_path=None, _m=KEY_FORMAT.match):
    r"""Check the KIM property instances format.

    Check the KIM property instances format from a deserialized ``fi``.

    Property Instances are either Predictions or items of Reference Data and
    must conform to the specification in the associated Property Definition.
    A Property Instance is stored in a subset of the EDN format. Multiple
    Property Instances in a file may optionally be contained within an array
    represented by a start bracket \(\[\) at the beginning, and an end
    bracket \(\]\) at the end of the file:

    Arguments:
        fi (a ``.read()``-supporting file-like object,
            or a name string to a file containing a KIM-EDN document
            or a string
            or a KIM-EDN object) to a property instance Python object.

        fp (a ``.read()``-supporting file-like object,
            or a name string to a file containing a KIM-EDN document
            or a string) to a property definition Python object.
            (default: None)

        fp_path should be an absolute path (or a valid relative path)
            to the KIM property definition folder. (default: None)
            or
            a KIM properties object containing all the available properties

    """
    # Check whether the property definition is provided?
    if fp is None:
        # Check whether the path is provided to the property files?
        if fp_path is None:
            msg = 'either the absolute path to the KIM properties '
            msg += 'or a KIM property definition should be provided.'
            raise KIMPropertyError(msg)

        if isinstance(fp_path, str):
            # Check whether the provided path is an absolute path?
            if not isabs(fp_path):
                # Loosen the check for the relative path which exists
                if isdir(fp_path):
                    fp_path = abspath(fp_path)
                else:
                    msg = 'the path KIM properties should be an '
                    msg += 'absolute path name.'
                    raise KIMPropertyError(msg)
        elif not isinstance(fp_path, dict):
            msg = 'wrong KIM properties object.'
            raise KIMPropertyError(msg)
    # Property definition file is provided
    elif fp_path is not None:
        msg = 'only the absolute path to the KIM properties '
        msg += 'or a KIM property file should be provided (not both).'
        raise KIMPropertyError(msg)

    # Property instance
    if isinstance(fi, (list, dict)):
        pi = fi
    else:
        pi = kim_edn.load(fi)

    if isinstance(pi, dict):
        check_required_keys_present(pi, rk=required_keys)

        check_property_id_format(pi["property-id"])

        if fp is None:
            if isinstance(fp_path, dict):
                if pi["property-id"] in fp_path:
                    fp = fp_path[pi["property-id"]]
                else:
                    msg = 'the requested property ID = \n"'
                    msg += pi["property-id"]
                    msg += '"\ndoes not exist in the input KIM properties.'
                    raise KIMPropertyError(msg)
            else:
                _path, _, _, _property_name = get_property_id_path(
                    pi["property-id"])

                if isfile(join(fp_path, _path)):
                    fp = join(fp_path, _path)
                elif isfile(join(fp_path, _property_name + ".edn")):
                    fp = join(fp_path, _property_name + ".edn")
                else:
                    msg = 'unable to find a KIM property definition at {\n"'
                    msg += join(fp_path, _path)
                    msg += '",\nnor at\n"'
                    msg += join(fp_path, _property_name + ".edn")
                    msg += '"}'
                    raise KIMPropertyError(msg)
                del _path
                del _property_name

        if isinstance(fp, dict):
            # It is already in the KIM-EDN format
            pd = fp
        else:
            # property definition
            pd = kim_edn.load(fp)

        # We have to check if required keys are there
        check_required_keys_present(pd, rk=def_required_keys)

        if pd["property-id"] != pi["property-id"]:
            msg = 'wrong property definition is provided.\n'
            msg += f'Property id :\n{pd["property-id"]}\n'
            msg += 'read from the property definition file is different '
            msg += f'from the property id :\n{pi["property-id"]}\n'
            msg += 'read from the property instance file.'
            raise KIMPropertyError(msg)

        check_instance_id_format(pi["instance-id"])

        # Check optional fields.
        for k in pi:
            if k not in required_keys + optional_keys:
                if k in pd:
                    check_instance_optional_key_map(k, pi[k], pd[k], _m=_m)
                else:
                    check_instance_optional_key_map(k, pi[k], _m=_m)

        # Check optional variables marked required are present in the instance.
        check_instance_optional_key_marked_required_are_present(pi, pd)

    elif isinstance(pi, list):
        instance_id = []
        for pi_ in pi:
            check_required_keys_present(pi_, rk=required_keys)

            check_property_id_format(pi_["property-id"])

            if fp is None:
                if isinstance(fp_path, dict):
                    if pi_["property-id"] in fp_path:
                        pd = fp_path[pi_["property-id"]]
                    else:
                        msg = 'the requested property ID = \n"'
                        msg += pi_["property-id"]
                        msg += '"\ndoes not exist in the input KIM '
                        msg += 'properties.'
                        raise KIMPropertyError(msg)
                else:
                    _path, _, _, _property_name = get_property_id_path(
                        pi_["property-id"])

                    if isfile(join(fp_path, _path)):
                        fp = join(fp_path, _path)
                    elif isfile(join(fp_path, _property_name + ".edn")):
                        fp = join(fp_path, _property_name + ".edn")
                    else:
                        msg = 'unable to find a KIM property definition '
                        msg += 'at {\n"'
                        msg += join(fp_path, _path)
                        msg += '",\nnor at\n"'
                        msg += join(fp_path, _property_name + ".edn")
                        msg += '"}'
                        raise KIMPropertyError(msg)

                    # property definition
                    pd = kim_edn.load(fp)

                # Set fp back to None for the next property in the loop
                fp = None
            else:
                if isinstance(fp, dict):
                    # It is already in the KIM-EDN format
                    pd = fp
                else:
                    # property definition
                    pd = kim_edn.load(fp)

                # We have to check if required keys are there
                check_required_keys_present(pd, rk=def_required_keys)

            if pd["property-id"] != pi_["property-id"]:
                msg = 'wrong property definition is provided.\n'
                msg += f'Property id :\n{pd["property-id"]}\n'
                msg += 'read from the property definition file is different '
                msg += f'from the property id :\n{pi_["property-id"]}\n'
                msg += 'read from the property instance file.'
                raise KIMPropertyError(msg)

            check_instance_id_format(pi_["instance-id"])

            if pi_["instance-id"] in instance_id:
                msg = 'the "instance-id’s" cannot repeat.'
                raise KIMPropertyError(msg)

            instance_id.append(pi_["instance-id"])

            # Check optional fields.
            for k in pi_:
                if k not in required_keys + optional_keys:
                    if k in pd:
                        check_instance_optional_key_map(
                            k, pi_[k], pd[k], _m=_m)
                    else:
                        check_instance_optional_key_map(k, pi_[k], _m=_m)

            # Check optional variables marked required
            # are present in the instance.
            check_instance_optional_key_marked_required_are_present(pi_, pd)

    else:
        msg = 'input to the function does not have a correct KIM-EDN format.'
        raise KIMPropertyError(msg)
