"""Create module."""

from os.path import isfile
from typing import Optional

import kim_edn

from .err import KIMPropertyError
from .definition import check_property_definition
from .instance import get_property_id_path, check_instance_id_format
from .ednify import unednify_kim_properties

__all__ = [
    "get_properties",
    "kim_property_create",
    "unset_property_id",
]

KIM_PROPERTIES = None
"""dict: KIM properties dictionary indexed by properties full IDs."""

PROPERTY_NAME_TO_PROPERTY_ID = None
"""dict: KIM properties name to full ID dictionary."""

PROPERTY_ID_TO_PROPERTY_NAME = None
"""dict: KIM properties full ID to name dictionary."""

# Get the standard KIM properties
KIM_PROPERTIES, PROPERTY_NAME_TO_PROPERTY_ID, \
    PROPERTY_ID_TO_PROPERTY_NAME = unednify_kim_properties()

NEW_PROPERTY_IDS = None
"""list: Newly added property IDs """


def get_properties():
    """Get the kim properties object hierarchy from the edn object.

    Returns:
        dict -- KIM_PROPERTIES.
    """
    return KIM_PROPERTIES


def unset_property_id(property_id):
    """Unset a property with a "property_id" from kim properties.

    If a requested property with a "property_id" is a newly created
    property, then it will remove that property from KIM_PROPERTIES,
    otherwise it does nothing.

    Arguments:
        property_id {string} -- KIM property-id, a string containing the
            unique ID of the property.

    """
    global NEW_PROPERTY_IDS
    global PROPERTY_NAME_TO_PROPERTY_ID
    global PROPERTY_ID_TO_PROPERTY_NAME

    if NEW_PROPERTY_IDS is not None:
        if property_id in NEW_PROPERTY_IDS:
            del KIM_PROPERTIES[property_id]
            _name = PROPERTY_ID_TO_PROPERTY_NAME[property_id]
            del PROPERTY_NAME_TO_PROPERTY_ID[_name]
            del PROPERTY_ID_TO_PROPERTY_NAME[property_id]
            NEW_PROPERTY_IDS.remove(property_id)
            if len(NEW_PROPERTY_IDS) == 0:
                NEW_PROPERTY_IDS = None


def kim_property_create(
    instance_id: int,
    property_name: str,
    property_instances: Optional[str] = None,
    property_disclaimer: Optional[str] = None):
    """Create a new kim property instance.

    It takes as input the property instance ID and property definition name
    and creates initial property instance data structure. If the
    "property_instances" obj is already exist it adds the newly created
    property instance to the obj and fails if it already exist there.

    For example::

    >>> kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    >>> str = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')

    Creating and addition of a second property instance::

    >>> kim_property_create(2, 'atomic-mass', str)
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

    >>> str = kim_property_create(2, 'atomic-mass', str)
    >>> obj = kim_edn.loads(str)
    >>> print(kim_edn.dumps(obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
        }
        {
            "property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass"
            "instance-id" 2
        }
    ]

    Arguments:
        instance_id {int} -- A positive integer identifying the property
            instance.
        property_name {string} --
            - A string containing the property name or
            - unique ID of the property, or
            - a path-like object giving the pathname (absolute or relative to
              the current working directory) of the file to be opened
        property_instances {string} -- A string containing the serialized
            KIM-EDN formatted property instances. (default: {None})
        property_disclaimer {string} -- A string containing an optional
            statement of applicability of the data contained in this property
            instance. (default: {None})

    Returns:
        string -- serialized KIM-EDN formatted property instances.

    """  # noqa: E501
    global KIM_PROPERTIES
    global PROPERTY_NAME_TO_PROPERTY_ID
    global PROPERTY_ID_TO_PROPERTY_NAME
    global NEW_PROPERTY_IDS

    if not isinstance(instance_id, int):
        msg = 'the "instance_id" is not an `int`.'
        raise KIMPropertyError(msg)

    # Check instance id format to prevent mistakes as early as possible
    check_instance_id_format(instance_id)

    if not isinstance(property_name, str):
        msg = 'the "property_name" is not an `str`.'
        raise KIMPropertyError(msg)

    if property_instances is None:
        kim_property_instances = []
    else:
        # Deserialize the KIM property instances.
        kim_property_instances = kim_edn.loads(property_instances)

        for a_property_instance in kim_property_instances:
            if instance_id == a_property_instance["instance-id"]:
                msg = 'the "instance-id"’s cannot repeat. '
                msg += 'In the case where there are multiple property '
                msg += 'instances, the instance-id’s cannot repeat.'
                raise KIMPropertyError(msg)

    # KIM property names.
    kim_property_names = list(PROPERTY_NAME_TO_PROPERTY_ID.keys())

    # KIM property full IDs.
    kim_property_ids = list(PROPERTY_ID_TO_PROPERTY_NAME.keys())

    new_property_instance = {}

    # If the property_name is a path-like object to a file to be opened
    if isfile(property_name):
        # Load the property definition from a file
        pd = kim_edn.load(property_name)

        # Check the correctness of th eproperty definition
        check_property_definition(pd)

        # Get the property ID
        _property_id = pd["property-id"]

        # Check to make sure that this property does not exist in OpenKIM
        if _property_id in KIM_PROPERTIES:
            msg = 'the input property_name file contains a property ID:\n'
            msg += f'"{_property_id}"\nwhich already exists in the KIM '
            msg += 'Property Definition list.\nUse the KIM Property '
            msg += 'Definition or update the ID in the property_name '
            msg += 'file.\nSee the KIM Property Definitions at https://'
            msg += 'openkim.org/properties for more detailed information.'
            raise KIMPropertyError(msg)

        # Add the new property definition to KIM_PROPERTIES
        KIM_PROPERTIES[_property_id] = pd

        # Get the property name
        _, _, _, _property_name = get_property_id_path(_property_id)

        PROPERTY_NAME_TO_PROPERTY_ID[_property_name] = _property_id
        PROPERTY_ID_TO_PROPERTY_NAME[_property_id] = _property_name

        kim_property_names.append(_property_name)
        kim_property_ids.append(_property_id)

        # Keep the record of a newly added properties
        if NEW_PROPERTY_IDS is None:
            NEW_PROPERTY_IDS = []
        NEW_PROPERTY_IDS.append(_property_id)

        # Set the new instance property ID
        new_property_instance["property-id"] = _property_id
    else:
        if property_name in kim_property_names:
            new_property_instance["property-id"] = \
                PROPERTY_NAME_TO_PROPERTY_ID[property_name]
        elif property_name in kim_property_ids:
            new_property_instance["property-id"] = property_name
        else:
            msg = f'the requested "property_name" :\n"{property_name}"\nis not'
            msg += ' a valid KIM property property name nor a path-like object'
            msg += ' to a file.\nSee the KIM Property Definitions at https://'
            msg += 'openkim.org/properties for more detailed information.'
            raise KIMPropertyError(msg)

    new_property_instance["instance-id"] = instance_id

    if property_disclaimer is not None:
        new_property_instance["disclaimer"] = property_disclaimer

    # Add the newly created property instance to the collection
    kim_property_instances.append(new_property_instance)

    # If there are multiple keys sort them based on instance-id
    if len(kim_property_instances) > 1:
        kim_property_instances = sorted(
            kim_property_instances, key=lambda i: i["instance-id"])

    # Return the serialize KIM property instances
    return kim_edn.dumps(kim_property_instances)
