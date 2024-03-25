r"""KIM-PROPERTY utility module.

The objective is to make it as easy as possible to convert a script (for
example a [LAMMPS](https://lammps.sandia.gov/) script) that computes a
property to a KIM Test.

This utility module has 5 modes:

1- Create
    Take as input the property instance ID and property definition name and
    create initial property instance data structure. It checks and indicates
    whether the property definition exists in [OpenKIM](https://openkim.org/).

2- Destroy
    Delete a previously created property instance ID.

3- Modify
    Incrementally build the property instance by receiving keys with
    associated arguments. It can "append" and add to a key's existing array
    argument.

4- Remove
    Remove a key.

5- Dump
    Take as input the generated instance and a filename, validate instance
    against the property definition and either issues an error or writes the
    instance out to file in edn format. Final validation should make sure
    all keys/arguments are legal and all required keys are provided.

Creating property instances::

    >>> kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    >>> str = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')

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

Destroying property instances::

    >>> obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    >>> kim_property_destroy(obj, 1)
    '[]'

    >>> obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

    >>> kim_property_destroy(obj, 2)
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

Modifying (setting) property instances::

    >>> str = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> str = kim_property_modify(str, 1,
                "key", "short-name",
                "source-value", "1", "fcc",
                "key", "species",
                "source-value", "1:4", "Al", "Al", "Al", "Al",
                "key", "a",
                "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                "source-unit", "angstrom", "digits", "5")
    >>> obj = kim_edn.loads(str)
    >>> print(kim_edn.dumps(obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "short-name" {
                "source-value" [
                    "fcc"
                ]
            }
            "species" {
                "source-value" [
                    "Al"
                    "Al"
                    "Al"
                    "Al"
                ]
            }
            "a" {
                "source-value" [
                    3.9149
                    4.0
                    4.032
                    4.0817
                    4.1602
                ]
                "source-unit" "angstrom"
                "digits" 5
            }
        }
    ]

For cases where there are multiple keys or a key receives an array of values
computed one at a time, the `kim_property_modify` can be called multiple
times and append values to a given key.

    >>> str = kim_property_modify(str, 1,
                "key", "basis-atom-coordinates",
                "source-value", "2", "1:2", "0.5", "0.5")

    >>> obj = kim_edn.loads(str)
    >>> print(kim_edn.dumps(obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "short-name" {
                "source-value" [
                    "fcc"
                ]
            }
            "species" {
                "source-value" [
                    "Al"
                    "Al"
                    "Al"
                    "Al"
                ]
            }
            "a" {
                "source-value" [
                    3.9149
                    4.0
                    4.032
                    4.0817
                    4.1602
                ]
                "source-unit" "angstrom"
                "digits" 5
            }
            "basis-atom-coordinates" {
                "source-value" [
                    [
                        0.0
                        0.0
                        0.0
                    ]
                    [
                        0.5
                        0.5
                        0.0
                    ]
                ]
            }
        }
    ]
    >>> str = kim_property_modify(str, 1,
                "key", "basis-atom-coordinates",
                "source-value", "3", "1:3", "0.5", "0.0", "0.5",
                "key", "basis-atom-coordinates",
                "source-value", "4", "2:3", "0.5", "0.5")

    >>> obj = kim_edn.loads(str)
    >>> print(kim_edn.dumps(obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "short-name" {
                "source-value" [
                    "fcc"
                ]
            }
            "species" {
                "source-value" [
                    "Al"
                    "Al"
                    "Al"
                    "Al"
                ]
            }
            "a" {
                "source-value" [
                    3.9149
                    4.0
                    4.032
                    4.0817
                    4.1602
                ]
                "source-unit" "angstrom"
                "digits" 5
            }
            "basis-atom-coordinates" {
                "source-value" [
                    [
                        0.0
                        0.0
                        0.0
                    ]
                    [
                        0.5
                        0.5
                        0.0
                    ]
                    [
                        0.5
                        0.0
                        0.5
                    ]
                    [
                        0.0
                        0.5
                        0.5
                    ]
                ]
            }
        }
    ]

    >>> str = kim_property_modify(str, 1,
                "key", "cohesive-potential-energy",
                "source-value", "1:5", "3.324", "3.3576", "3.3600", "3.3550", "3.3260",
                "source-std-uncert-value", "1:5", "0.002", "0.0001", "0.00001", "0.0012", "0.00015",
                "source-unit", "eV",
                "digits", "5")

    >>> obj = kim_edn.loads(str)
    >>> print(kim_edn.dumps(obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "short-name" {
                "source-value" [
                    "fcc"
                ]
            }
            "species" {
                "source-value" [
                    "Al"
                    "Al"
                    "Al"
                    "Al"
                ]
            }
            "a" {
                "source-value" [
                    3.9149
                    4.0
                    4.032
                    4.0817
                    4.1602
                ]
                "source-unit" "angstrom"
                "digits" 5
            }
            "basis-atom-coordinates" {
                "source-value" [
                    [
                        0.0
                        0.0
                        0.0
                    ]
                    [
                        0.5
                        0.5
                        0.0
                    ]
                    [
                        0.5
                        0.0
                        0.5
                    ]
                    [
                        0.0
                        0.5
                        0.5
                    ]
                ]
            }
            "cohesive-potential-energy" {
                "source-value" [
                    3.324
                    3.3576
                    3.36
                    3.355
                    3.326
                ]
                "source-std-uncert-value" [
                    0.002
                    0.0001
                    1e-05
                    0.0012
                    0.00015
                ]
                "source-unit" "eV"
                "digits" 5
            }
        }
    ]

Removing (a) key(s) from a property instance::

    >>> str = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> str = kim_property_modify(str, 1,
                "key", "short-name",
                "source-value", "1", "fcc",
                "key", "species",
                "source-value", "1:4", "Al", "Al", "Al", "Al",
                "key", "a",
                "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                "source-unit", "angstrom", "digits", "5",
                "key", "basis-atom-coordinates",
                "source-value", "2", "1:2", "0.5", "0.5",
                "key", "basis-atom-coordinates",
                "source-value", "3", "1:3", "0.5", "0.0", "0.5",
                "key", "basis-atom-coordinates",
                "source-value", "4", "2:3", "0.5", "0.5",
                "key", "cohesive-potential-energy",
                "source-value", "1:5", "3.324", "3.3576", "3.3600", "3.3550", "3.3260",
                "source-std-uncert-value", "1:5", "0.002", "0.0001", "0.00001", "0.0012", "0.00015",
                "source-unit", "eV",
                "digits", "5")

    >>> str = kim_property_remove(str, 1, "key", "a", "source-unit")
    >>> str = kim_property_remove(str, 1, "key", "cohesive-potential-energy", "key", "basis-atom-coordinates")

    >>> obj = kim_edn.loads(str)
    >>> print(kim_edn.dumps(obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "short-name" {
                "source-value" [
                    "fcc"
                ]
            }
            "species" {
                "source-value" [
                    "Al"
                    "Al"
                    "Al"
                    "Al"
                ]
            }
            "a" {
                "source-value" [
                    3.9149
                    4.0
                    4.032
                    4.0817
                    4.1602
                ]
                "digits" 5
            }
        }
    ]

"""  # noqa: E501

from .err import KIMPropertyError
from .definition import \
    check_key_present, \
    check_property_id_format, \
    check_property_title_format, \
    check_required_keys_present, \
    check_key_format, \
    check_optional_key_type_format, \
    check_optional_key_extent_format, \
    check_optional_key_extent_scalar, \
    get_optional_key_extent_ndimensions, \
    get_optional_key_extent_shape,\
    check_property_optional_key_standard_pairs_format, \
    check_property_optional_key_map, \
    check_property_definition
from .instance import \
    get_property_id_path, \
    check_instance_id_format, \
    check_optional_key_source_value_scalar, \
    get_optional_key_source_value_ndimensions, \
    check_instance_optional_key_standard_pairs_format, \
    check_instance_optional_key_map, \
    check_instance_optional_key_marked_required_are_present, \
    check_property_instances
from .create import get_properties, kim_property_create, unset_property_id
from .destroy import kim_property_destroy
from .modify import kim_property_modify
from .remove import kim_property_remove
from .dump import kim_property_dump

__all__ = [
    "KIMPropertyError",
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
    "get_property_id_path",
    "check_instance_id_format",
    "check_optional_key_source_value_scalar",
    "get_optional_key_source_value_ndimensions",
    "check_instance_optional_key_standard_pairs_format",
    "check_instance_optional_key_map",
    "check_instance_optional_key_marked_required_are_present",
    "check_property_instances",
    "get_properties",
    "kim_property_create",
    "unset_property_id",
    "kim_property_destroy",
    "kim_property_modify",
    "kim_property_remove",
    "kim_property_dump",
]

__author__ = 'Yaser Afshar <yafshar@umn.edu>'

from . import _version  # noqa: E402
__version__ = _version.get_versions()['version']
