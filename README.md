# KIM-PROPERTY utility module

[![Python package](https://github.com/openkim/kim-property/workflows/Python%20package/badge.svg)](https://github.com/openkim/kim-property/actions)
[![codecov](https://codecov.io/gh/openkim/kim-property/branch/master/graph/badge.svg)](https://codecov.io/gh/openkim/kim-property)
[![Anaconda-Server Badge](https://img.shields.io/conda/vn/conda-forge/kim-property.svg)](https://anaconda.org/conda-forge/kim-property)
[![PyPI](https://img.shields.io/pypi/v/kim-property.svg)](https://pypi.python.org/pypi/kim-property)
[![License](https://img.shields.io/badge/license-LGPL--2.1--or--later-blue)](LICENSE)

The objective is to make it as easy as possible to convert a script (for
example a [LAMMPS](https://lammps.sandia.gov/) script) that computes a
[KIM property](https://openkim.org/properties) to a KIM Test.

This utility module has 5 modes:

1- **[Create](#create)**\
    Take as input the property instance ID and property definition name and
    create initial property instance data structure. It checks and indicates
    whether the property definition exists in [OpenKIM](https://openkim.org/).

2- **[Destroy](#destroy)**\
    Delete a previously created property instance ID.

3- **[Modify](#modify)**\
    Incrementally build the property instance by receiving keys with
    associated arguments. It can "append" and add to a key's existing array
    argument.

4- **[Remove](#remove)**\
    Remove a key.

5- **[Dump](#dump)**\
    Take as input the generated instance and a filename, validate each
    instance against the property definition and either issues an error or
    writes the instance out to file in edn format. Final validation should
    make sure all keys/arguments are legal and all required keys are
    provided.

To get started, you'll need to install the `kim-property` package. Please refer
to the [installation instructions](#installing-kim-property).

## Create

Creating property instances::

````py
    >>> kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')

    >>> kim_property_create(2, 'atomic-mass', property_inst)
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

    >>> property_inst = kim_property_create(2, 'atomic-mass', property_inst)
    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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

    >>> kim_property_create(1, 'cohesive-energy-relation-cubic-crystal', property_disclaimer="This is an example disclaimer.")
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1 "disclaimer" "This is an example disclaimer."}]'

    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')

    >>> kim_property_create(2, 'atomic-mass', property_inst, "This is an example disclaimer for atomic-mass.")
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2 "disclaimer" "This is an example disclaimer for atomic-mass."}]'
````

A property instance is stored in a subset of the KIM-EDN format as described in
[KIM Property Instances](https://openkim.org/doc/schema/properties-framework).
Each property instance must contain the `property-id` and `instance-id`.
`kim-property` utility module can create a new property instance, using a KIM
property ID. A KIM property ID is an identifier of a KIM Property Definition,
which can be,
(1) a property short name,
(2) the full unique ID of the property (including the contributor and date),
(3) a file name corresponding to a local property definition file.

Examples of each of these cases are shown below:

````py
    >>> kim_property_create(1, 'atomic-mass')
    >>> kim_property_create(2, 'cohesive-energy-relation-cubic-crystal')
````

````py
    >>> kim_property_create(1, 'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass')
    >>> kim_property_create(2, 'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal')
````

````py
    >>> kim_property_create(1, 'new-property.edn')
    >>> kim_property_create(2, '/home/mary/marys-kim-properties/dissociation-energy.edn')
````

In the last example, "new-property.edn" and
"/home/mary/marys-kim-properties/dissociation-energy.edn"
are the names of files that contain user-defined (local) property definitions.

## Destroy

Destroying property instances::

````py
    >>> property_inst_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    >>> kim_property_destroy(property_inst_obj, 1)
    '[]'

    >>> property_inst_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

    >>> kim_property_destroy(property_inst_obj, 2)
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'
````

## Modify

Modifying (setting) property instances.

Once a `kim_property_create` has been given to instantiate a property
instance, maps associated with the property's keys can be edited using the
kim_property_modify.
In using this command, the special keyword "key" should be given, followed
by the property key name and the key-value pair in the map associated with
the key that is to be set.

For example, the `cohesive-energy-relation-cubic-crystal` property definition
consists of property keys named "short-name", "species", ...
An instance of this property could be created like so::

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "short-name",
                "source-value", "1", "fcc",
                "key", "species",
                "source-value", "1:4", "Al", "Al", "Al", "Al",
                "key", "a",
                "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                "source-unit", "angstrom", "digits", "5")
    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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

    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
                "disclaimer", "This is an example disclaimer.",
                "key", "short-name",
                "source-value", "1", "fcc")
    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "disclaimer" "This is an example disclaimer."
            "short-name" {
                "source-value" [
                    "fcc"
                ]
            }
        }
    ]
````

For cases where there are multiple keys or a key receives an array of values
computed one at a time, the `kim_property_modify` can be called multiple
times and append values to a given key.

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "short-name",
                "source-value", "1", "fcc",
                "key", "species",
                "source-value", "1:4", "Al", "Al", "Al", "Al",
                "key", "a",
                "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                "source-unit", "angstrom", "digits", "5")
    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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
    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "basis-atom-coordinates",
                "source-value", "2", "1:2", "0.5", "0.5")

    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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
    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "basis-atom-coordinates",
                "source-value", "3", "1:3", "0.5", "0.0", "0.5",
                "key", "basis-atom-coordinates",
                "source-value", "4", "2:3", "0.5", "0.5")

    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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

    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "cohesive-potential-energy",
                "source-value", "1:5", "3.324", "3.3576", "3.3600", "3.3550", "3.3260",
                "source-std-uncert-value", "1:5", "0.002", "0.0001", "0.00001", "0.0012", "0.00015",
                "source-unit", "eV",
                "digits", "5")

    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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
````

**Note:**

Variables which are introduced with a specified extent of either an empty
vector `[]` or `[1]`, are scalars.

Calling a `kim_property_modify` will update the scalars and vector values
which are already set.

For example:

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "space-group",
                "source-value", "Immm")

    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "space-group" {
                "source-value" "Immm"
            }
        }
    ]
````

Calling the `kim_property_modify` again set the scalar variable with a new
value.

````py
    >>> property_inst = kim_property_modify(property_inst, 1,
                "key", "space-group",
                "source-value", "P6_3/mmc")

    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
    [
        {
            "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
            "instance-id" 1
            "space-group" {
                "source-value" "P6_3/mmc"
            }
        }
    ]

````

**Note:**

If the source-value key is a scalar, the values of the uncertainty and digits
keys must be scalars. Thus, calling the `kim_property_modify` with a non-scalar
key where the source-value key is a scalar fails.

**Note:**

If the source-value key's value is an array (EDN vector), the values of the
uncertainty and digits keys must be either arrays of the same extent, or
scalars in which case they are taken to apply equally to all values in the
source-value array. The keys associated with uncertainty and precision conform
to the
[ISO Guide to the Expression of Uncertainty in Measurement](https://www.iso.org/standard/50461.html)
and the
[ThermoML standard notation](https://www.degruyter.com/view/journals/ci/28/3/article-p22.xml).

The keys associated with uncertainty and precision of the
[KIM Property Instances](https://openkim.org/doc/schema/properties-framework)
are:

- source-std-uncert-value
- source-expand-uncert-value
- coverage-factor
- source-asym-std-uncert-neg
- source-asym-std-uncert-pos
- source-asym-expand-uncert-neg
- source-asym-expand-uncert-pos
- uncert-lev-of-confid
- digits

In below example, the `a`-key source-value key's value is an array, which means
the value of the `digits`-key must be either an array of the same extent, or a
scalar.

1. The value of the `digits`-key is a scalar:

    ````py
        >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
        >>> property_inst = kim_property_modify(property_inst, 1,
                    "key", "a",
                    "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                    "source-unit", "angstrom", "digits", "5")
        >>> property_inst_obj = kim_edn.loads(property_inst)
        >>> print(kim_edn.dumps(property_inst_obj, indent=4))
        [
            {
                "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
                "instance-id" 1
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
    ````

2. The value of the `digits`-key is an array of the same extent:

    ````py
        >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
        >>> property_inst = kim_property_modify(property_inst, 1,
                    "key", "a",
                    "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602",
                    "source-unit", "angstrom", "digits", "1:5", "5", "5", "5", "5", "5")
        >>> property_inst_obj = kim_edn.loads(property_inst)
        >>> print(kim_edn.dumps(property_inst_obj, indent=4))
        [
            {
                "property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"
                "instance-id" 1
                "a" {
                    "source-value" [
                        3.9149
                        4.0
                        4.032
                        4.0817
                        4.1602
                    ]
                    "source-unit" "angstrom"
                    "digits" [
                        5
                        5
                        5
                        5
                        5
                    ]
                }
            }
        ]
    ````

## Remove

Removing (a) key(s) from a property instance::

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
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

    >>> property_inst = kim_property_remove(property_inst, 1, "key", "a", "source-unit")
    >>> property_inst = kim_property_remove(property_inst, 1, "key", "cohesive-potential-energy", "key", "basis-atom-coordinates")

    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> print(kim_edn.dumps(property_inst_obj, indent=4))
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
````

## Dump

First, it validates the generated instances against the property definition.
Then serializes it to a [KIM-EDN](https://github.com/openkim/kim-edn#kim-edn)
formatted stream and dumps it to a `fp` (a `.write()`-supporting file-like
object or a name string to open a file).

The validation makes sure all keys/arguments are legal and all required keys
are provided.

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
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
    >>> kim_property_dump(property_inst, "results.edn")
````

or

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
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
    >>> property_inst_obj = kim_edn.loads(property_inst)
    >>> kim_property_dump(property_inst_obj, "results.edn")
````

or

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
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
    >>> with open("results.edn", 'w') as fp:
            kim_property_dump(property_inst, fp)
````

An example with two property instances,

````py
    >>> property_inst = kim_property_create(1, 'cohesive-energy-relation-cubic-crystal')
    >>> property_inst = kim_property_modify(property_inst, 1,
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
    >>> property_inst = kim_property_create(2, 'atomic-mass', property_inst)
    >>> property_inst = kim_property_modify(property_inst, 2,
                "key", "mass",
                "source-value", "1.434e-19", "source-unit", "si",
                "key", "species",
                "source-value", "Al")
    >>> kim_property_dump(property_inst, "results.edn")
````

## Installing kim-property

### Requirements

You need Python 3.8 or later to run `kim-property`. You can have multiple
Python versions (2.x and 3.x) installed on the same system without problems.

To install Python 3 for different Linux flavors, macOS and Windows, packages
are available at\
[https://www.python.org/getit/](https://www.python.org/getit/)

### Using pip

**pip** is the most popular tool for installing Python packages, and the one
included with modern versions of Python.

`kim-property` can be installed with `pip`:

```sh
pip install kim-property
```

**Note:**

Depending on your Python installation, you may need to use `pip3` instead of
`pip`.

```sh
pip3 install kim-property
```

Depending on your configuration, you may have to run `pip` like this:

```sh
python3 -m pip install kim-property
```

### Using pip (GIT Support)

`pip` currently supports cloning over `git`

```sh
pip install git+https://github.com/openkim/kim-property.git
```

For more information and examples, see the
[pip install](https://pip.pypa.io/en/stable/reference/pip_install/#id18) reference.

### Using conda

**conda** is the package management tool for Anaconda Python installations.

Installing `kim-property` from the `conda-forge` channel can be achieved
by adding `conda-forge` to your channels with:

```sh
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Once the `conda-forge` channel has been enabled, `kim-property` can be
installed with `conda`:

```sh
conda install kim-property
```

or with `mamba`:

```sh
mamba install kim-property
```

It is possible to list all of the versions of `kim-property` available on
your platform with `conda`:

```sh
conda search kim-property --channel conda-forge
```

or with `mamba`:

```sh
mamba search kim-property --channel conda-forge
```

Alternatively, `mamba repoquery` may provide more information:

```sh
# Search all versions available on your platform:
mamba repoquery search kim-property --channel conda-forge

# List packages depending on `kim-property`:
mamba repoquery whoneeds kim-property --channel conda-forge

# List dependencies of `kim-property`:
mamba repoquery depends kim-property --channel conda-forge
```

## Copyright

Copyright (c) 2020-2024, Regents of the University of Minnesota.\
All Rights Reserved

## Contributing

Contributors:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yaser Afshar
