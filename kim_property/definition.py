"""Definition validator."""

import re

import kim_edn

from .err import KIMPropertyError

__all__ = [
    "required_keys",
    "standard_keys",
    "check_key_present",
    "check_property_id_format",
    "check_property_title_format",
    "check_required_keys_present",
    "check_key_format",
    "check_optional_key_type_format",
    "check_optional_key_extent_format",
    "check_optional_key_extent_scalar",
    "get_optional_key_extent_ndimensions",
    "get_optional_key_extent_shape",
    "check_property_optional_key_standard_pairs_format",
    "check_property_optional_key_map",
    "check_property_definition",
]


# A Property Definition must contain the following required key-value pairs:
required_keys = ("property-id", "property-title", "property-description")

# The required fields list above are followed by an unordered set of
# key-map pairs. Each key is associated with a map which must contain
# the following standard keys-value pairs:
standard_keys = (
    # A string defining the variable type that can be set to one of the
    # following: "string", "float", "int", "bool", or "file".
    "type",
    # A boolean that indicates whether the variable value is
    # physically-dimensioned and therefore has a physical unit or not.
    # It can be set to either true or false.
    "has-unit",
    # An EDN vector specifying whether the variable is a scalar or an array
    # (EDN vector) of a specified extent. It can be set to either an empty
    # vector [] to represent a scalar, or the extent of the array with known
    # dimensions specified and unknown dimensions indicated by a string
    # containing a colon character, ":".
    # For example, [":"], [3,3], [":",2,":"].
    # It is recommended to store arrays in a by-row ordering for improved
    # readability, e.g., store the coordinates of 10 atoms as [10,3] as
    # opposed to [3,10].
    "extent",
    # A boolean that indicates whether the variable must be reported in every
    # Property Instance of the property or not. It can be set to either true
    # or false.
    "required",
    # A string which provides an explanation of what the variable is intended
    # to represent.
    "description"
)


FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL


def check_key_present(k, s):
    """Check if a key is present.

    Arguments:
        k {string} -- key
        s {string} -- input string

    """
    if isinstance(k, str) and isinstance(s, str):
        if s.find(k) == -1:
            msg = f'the required key "{k}" is not found.'
            raise KIMPropertyError(msg)
        return

    msg = 'input to the function is not a `str`.'
    raise KIMPropertyError(msg)


# A string containing the unique ID of the property. The Property ID conforms
# to the Tag URI Scheme as described in RFC 4151:
PROPERTY_ID = re.compile(
    r'^tag:[^+^A-Z]*@[^+^A-Z]*,\d{4}-\d{2}-\d{2}:property/[a-z0-9\-]*$', FLAGS)


def check_property_id_format(s, _m=PROPERTY_ID.match):
    r"""Check the property id fomrat.

    tag:<email-address>,<date>:property/<property-name>
    <email-address> is the e-mail address of the property contributor.
    A contributor has several options available.
        - own e-mail address,
        - openkim.org username followed by “@noreply.openkim.org”,
        - openkim.org organization name followed by “@noreply.openkim.org”,
        - openkim.org user or organization’s UUID followed by “@noreply.openkim.org”,
        - “staff@noreply.openkim.org” in agreement with the KIM Editor
    <email-address> must be in lowercase characters for the range of A-Z
    <email-address> cannot contain a plus (“+”) character
    <email-address> should be a valid e-mail address.

    Arguments:
        s {string} -- A string containing the unique ID of the property.

    """
    if isinstance(s, str):
        if _m(s) is None:
            msg = f'the "property-id" value :\n{s}\n'
            msg += 'doesn\'t meet the format specification.\n'
            msg += 'See KIM "property-id" format specification at '
            msg += 'https://openkim.org/doc/schema/properties-framework/ '
            msg += 'in section 2.2 for more detailed information.'
            raise KIMPropertyError(msg)
        return

    msg = 'input to the function is not a `str`.'
    raise KIMPropertyError(msg)


def check_property_title_format(s):
    """Check the property title does not include an ending period.

    The title will be used in citations of the property. The title should not
    include an ending period.

    Arguments:
        s {string} -- A string containing a one-line title for the property.

    """
    if isinstance(s, str):
        if s.endswith('.'):
            msg = f'the "property-title" value :\n{s}\n'
            msg += 'should not include an ending period.'
            raise KIMPropertyError(msg)
        return

    msg = 'input to the function is not a `str`.'
    raise KIMPropertyError(msg)


def check_required_keys_present(s, rk=required_keys):
    """Check the required property keys are present.

    Arguments:
        s {string or dict} -- input object
        rk {tuple or list} -- required keys (default required_keys)

    """
    if isinstance(s, str):
        for r in rk:
            check_key_present(r, s)
    elif isinstance(s, dict):
        for r in rk:
            if r not in s:
                msg = f'the required key "{r}" is not found.'
                raise KIMPropertyError(msg)
    else:
        msg = 'input to the function is not a `str` '
        msg += 'or a `dict`.'
        raise KIMPropertyError(msg)

# checks for optional keys


# A key is a string. Key names can only include lower-case alphanumeric
# characters and dashes. The names are arbitrary and set by the developer
# to reflect the meaning of the key.
KEY_FORMAT = re.compile(r'^[a-z0-9\-]+$', FLAGS)


def check_key_format(s, _m=KEY_FORMAT.match):
    """Check a key format.

    Arguments:
        s {string} -- A key is a string which only includes lower-case
        alphanumeric characters and dashes.

    """
    if isinstance(s, str):
        if _m(s) is None:
            msg = f'"{s}" is an invalid optional key. '
            msg += 'A key is a string which only includes lower-case '
            msg += 'alphanumeric characters and dashes.'
            raise KIMPropertyError(msg)
        return

    msg = 'input to the function is not a `str`.'
    raise KIMPropertyError(msg)


def check_optional_key_type_format(s):
    """Check optional key type is a valid type.

    Arguments:
        s {string} -- key type, one of "string", "float", "int",
            "bool", "file"

    """
    if isinstance(s, str):
        str_type = ("string", "float", "int", "bool", "file")
        if s in str_type:
            return
        msg = 'input string defining the variable type is not '
        msg += 'valid. A string defining the variable type can be set to '
        msg += 'one of ::\n'
        msg += '"string", "float", "int", "bool", or "file".'
    else:
        msg = 'input to the function is not a `str`.'
    raise KIMPropertyError(msg)


EXTENT_KEY = re.compile(r'^\[([0-9\, ]*|(":")*)*\]$', FLAGS)
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)


def check_optional_key_extent_format(s, _m=EXTENT_KEY.match, _ws=WHITESPACE.sub):
    """Check extent key format.

    extent is an EDN vector specifying whether the variable is a scalar or
    an array (EDN vector) of a specified extent. It can be set to either:
        - an empty vector [] to represent a scalar
        - the extent of the array with known dimensions
        - the extent of the array with unknown dimensions
            (indicated by a string containing a colon character, ":".

    For example, [":"], [3,3], [":",2,":"].

    It is recommended to store arrays in a by-row ordering for improved
    readability, e.g., store the coordinates of 10 atoms as [10,3] as
    opposed to [3,10].

    Arguments:
        s {string, or list} -- input "extent"-key value

    """
    if isinstance(s, str):
        e = _ws('', s)
        if _m(e) is None:
            msg = f'the specified extent :\n{s}\ncontains invalid character.'
            raise KIMPropertyError(msg)
    elif isinstance(s, list):
        for s_ in s:
            if isinstance(s_, str):
                if s_ != ':':
                    msg = f'the specified extent contains invalid input "{s_}".'
                    raise KIMPropertyError(msg)
            elif isinstance(s_, int):
                continue
            else:
                msg = f'the specified extent contains invalid input "{s_}".'
                raise KIMPropertyError(msg)

    else:
        msg = 'input to the function is not a `str` or a `list`.'
        raise KIMPropertyError(msg)


WHITESPACE_EDN = re.compile(r'[, \t\n\r]*', FLAGS)


def check_optional_key_extent_scalar(s, _ws=WHITESPACE_EDN.sub):
    """Check optional key "extent" specifies a single item value.

    Arguments:
        s {string, or list} -- input "extent"-key value

    Returns:
        bool -- True if the optional key "extent" has scalar value

    """
    if isinstance(s, str):
        e = _ws('', s)
        return e == '[]'

    if isinstance(s, list):
        return len(s) == 0

    msg = 'input to the function is not a `list` or `str`.'
    raise KIMPropertyError(msg)


def get_optional_key_extent_ndimensions(extent_key):
    """Get the number of dimensions specified by optional key "extent".

    Get the number of dimensions specified by optional key "extent", where
    extent-value is an KIM-EDN vector specifying whether the variable is a
    scalar or an array.

    Arguments:
        extent_key {list} -- input "extent"-key value

    Returns:
        int -- Number of dimensions

    """
    if isinstance(extent_key, list):
        return len(extent_key)

    msg = 'input to the function is not a `list`.'
    raise KIMPropertyError(msg)


def get_optional_key_extent_shape(extent_key):
    """Get the shape or dimensions specified by optional key "extent".

    Get the shape or dimensions specified by optional key "extent", where
    extent-value is an KIM-EDN vector specifying whether the variable is a
    scalar or an array. Unknown dimensions indicated by a string containing
    a colon character, ":" would be considered as 1.

    Arguments:
        extent_key {list} -- input "extent"-key value

    Returns:
        list -- shape or dimensions as list of integers

    """
    if isinstance(extent_key, list):
        s = []
        for d in extent_key:
            if isinstance(d, int):
                s.append(d)
            elif d == ':':
                s.append(1)
            else:
                msg = f'list contains non-standard value "{d}".'
                raise KIMPropertyError(msg)
        return s

    msg = 'input to the function is not a `list`.'
    raise KIMPropertyError(msg)


def check_property_optional_key_standard_pairs_format(standard_pairs):
    """Check the standard key-map pairs correctness and format.

    The required fields are followed by an unordered set of key-map pairs.
    Each key is associated with a map which must contain the following
    standard keys-value pairs:
    "type", "has-unit", "extent", "required", "description"

    Arguments:
        standard_pairs {dict} -- input key-value pairs

    """
    if not isinstance(standard_pairs, dict):
        msg = 'input to the function is not a `dict`.'
        raise KIMPropertyError(msg)

    for k in standard_pairs:
        if k not in standard_keys:
            msg = f'wrong key.\nThe input "{k}"-key is not '
            msg += 'part of the standard key-value pairs.\n'
            msg += 'See KIM standard key-value pairs at '
            msg += 'https://openkim.org/doc/schema/properties-framework/ '
            msg += 'in section 2.2 for more detailed information.'
            raise KIMPropertyError(msg)

    check_optional_key_type_format(standard_pairs["type"])

    if not isinstance(standard_pairs["has-unit"], bool):
        msg = 'invalid value.\n'
        msg += f'The input "{standard_pairs["has-unit"]}" value '
        msg += 'should be a boolean that indicates '
        msg += 'whether the variable value is physically-dimensioned '
        msg += 'and therefore has a physical unit or not.'
        raise KIMPropertyError(msg)

    check_optional_key_extent_format(standard_pairs["extent"])

    if not isinstance(standard_pairs["required"], bool):
        msg = f'invalid value.\nThe input "{standard_pairs["required"]}" '
        msg += 'value should be a boolean that indicates '
        msg += 'whether the variable must be reported in every '
        msg += 'property-instance of the property or not.'
        raise KIMPropertyError(msg)

    if not isinstance(standard_pairs["description"], str):
        msg = 'invalid value.\n'
        msg += 'This input value should be a string which provides an '
        msg += 'explanation of what the variable is intended to '
        msg += 'represent.'
        raise KIMPropertyError(msg)


def check_property_optional_key_map(k, m, _m=KEY_FORMAT.match):
    """Check the optional fields key-map pairs correctness and format.

    Optional fields must be an unordered set of key-map pairs.

    Arguments:
        k {string} -- Optional field keyword.
        m {dict, string} -- Optional field value.

    """
    check_key_format(k, _m=_m)
    check_property_optional_key_standard_pairs_format(m)


def check_property_definition(fp, _m=KEY_FORMAT.match):
    r"""Check the KIM property definition format.

    Check the KIM property definition format from a deserialized ``fp``.

    Arguments:
        fp (a ``.read()``-supporting file-like object,
            or a name string to a file containing a KIM-EDN document
            or a string
            or a KIM-EDN object) to a property definition Python object.

    """
    # property definition
    if isinstance(fp, dict):
        pd = fp
    # Other format should be loaded by kim_edn
    else:
        pd = kim_edn.load(fp)

    if isinstance(pd, dict):
        try:
            check_required_keys_present(pd, rk=required_keys)

            check_property_id_format(pd["property-id"])

            check_property_title_format(pd["property-title"])

            # Check optional fields.
            for k in pd:
                if k not in required_keys:
                    check_property_optional_key_map(k, pd[k], _m=_m)
        except KIMPropertyError:
            msg = f'{fp} \n' + str(KIMPropertyError)
            raise KIMPropertyError(msg)
    else:
        msg = f'input to the function :\n{fp}\n'
        msg += 'is not a correct KIM-EDN type.'
        raise KIMPropertyError(msg)
