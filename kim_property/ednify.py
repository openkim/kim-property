"""KIM properties object serialization/de-serialization."""

from os.path import abspath, join, isdir, pardir, isfile, dirname
from os import listdir
from io import IOBase
from typing import Dict, Optional, Union

import kim_edn

from .err import KIMPropertyError
from .instance import get_property_id_path

__all__ = [
    "ednify_kim_properties",
    "unednify_kim_properties",
]


kim_properties_path: str = join(dirname(abspath(__file__)), "properties")
"""Absolute path to the KIM properties folder."""


def ednify_kim_properties(
    properties: Optional[Dict] = None,
    fp: Union[str, bytes, bytearray, IOBase] = join(
        kim_properties_path, "kim_properties.edn"
    ),
):
    """Serialize KIM properties.

    Keyword Arguments:
        properties {dict} -- KIM properties dictionary indexed by properties
            full IDs. (default: {None})
        fp {string, or a ``.write()``-supporting bytes-like object} -- fp is a
            file name string to open it or a ``.write()``-supporting
            bytes-like object.

    """
    # List of KIM properties to be ednified
    kim_properties_list = []

    if properties is None:
        # KIM property files path. An absolute path (or a valid relative path)
        # to the KIM property files folder.
        kim_property_files_path = join(
            dirname(abspath(__file__)),
            pardir,
            "external",
            "openkim-properties",
            "properties",
        )

        if isdir(abspath(kim_property_files_path)):
            kim_property_files_path = abspath(kim_property_files_path)
        else:
            msg = f"property files can not be found at\n{kim_property_files_path}"
            raise KIMPropertyError(msg)

        # KIM property names.
        kim_property_names = []
        # KIM property full IDs.
        kim_property_ids = []
        # KIM properties dictionary indexed by properties full IDs.
        kim_properties = {}

        # The directories under openkim-properties/properties
        # are the property names.
        for property_name in sorted(listdir(kim_property_files_path)):
            # directory containing all versions of the property
            property_name_dir = join(kim_property_files_path, property_name)
            # relative to `kim_property_files_path`, this is the full path
            # to the property file of the latest version of the property
            _path = join(
                property_name,
                sorted(listdir(property_name_dir))[-1],
                property_name + ".edn"
                )
            property_file = join(kim_property_files_path, _path)
            if not isfile(property_file):
                msg = 'the property file =\n"'
                msg += property_file
                msg += '"\ncan not be found!'
                raise KIMPropertyError(msg)
            # load the property dictionary
            property = kim_edn.load(property_file)
            # extract the property-id from the property dictionary
            property_id = property["property-id"]
            # consistency check between the path we got the
            # file from and its property-id
            _check_path, _, _, _ = get_property_id_path(property_id)
            if _path != _check_path:
                msg = 'the property-id\n"'
                msg += property_id
                msg += '"\nwas loaded from file\n"'
                msg += _path
                msg += '",\nbut implies the path\n"'
                msg += _check_path
                msg += '"!'
                raise KIMPropertyError(msg)
            # Everything looks correct, accumulate
            # lists and dictionary
            kim_property_names.append(property_name)
            kim_property_ids.append(property_id)
            kim_properties[property_id] = property

        del kim_property_files_path

        # KIM properties name to full ID dictionary.
        property_name_to_property_id = dict(zip(kim_property_names, kim_property_ids))

        # KIM properties full ID to name dictionary.
        property_id_to_property_name = dict(zip(kim_property_ids, kim_property_names))

        del kim_property_names
        del kim_property_ids

        kim_properties_list = [
            kim_properties,
            property_name_to_property_id,
            property_id_to_property_name,
        ]
    else:
        if not isinstance(properties, dict):
            msg = 'wrong input, "properties" is not a `dict`.'
            raise KIMPropertyError(msg)

        if len(properties) == 0:
            msg = 'wrong input, "properties" is empty.'
            raise KIMPropertyError(msg)

        property_ids = list(properties.keys())

        property_names = []
        for _id in property_ids:
            _, _, _, _name = get_property_id_path(_id)
            property_names.append(_name)

        # KIM properties name to full ID dictionary.
        name_to_property_id = dict(zip(property_names, property_ids))

        # KIM properties full ID to name dictionary.
        id_to_property_name = dict(zip(property_ids, property_names))

        del property_names
        del property_ids

        kim_properties_list = [
            properties,
            name_to_property_id,
            id_to_property_name,
        ]

    kim_edn.dump(kim_properties_list, fp)


def unednify_kim_properties(
    fp: Union[str, bytes, bytearray, IOBase] = join(
        kim_properties_path, "kim_properties.edn"
    )
):
    """Deserialize KIM properties.

    Return reconstituted object hierarchy from the edn object. Read the
    edn representation of an object from the "name" file and return the
    reconstituted object hierarchy specified therein. By default, it
    the "kim_properties", "property_name_to_property_id", and
    returns "property_id_to_property_name" objects.

    Keyword Arguments:
        fp {string or a ``.read()``-supporting bytes-like object} -- fp is a
            file name string to open a file or a ``.read()``-supporting
            bytes-like object.

    Returns:
        Deserialized KIM properties

    """
    return kim_edn.load(fp)
