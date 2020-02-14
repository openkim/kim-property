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

"""
import os
from os.path import abspath, join, isdir, pardir, dirname
import re

from .numeric import \
    shape, \
    size, \
    is_array_uniform, \
    create_full_array, \
    extend_full_array

from .definition import \
    KIMPropertyError, \
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

from .instance import standard_keys
from .instance import \
    get_property_id_path, \
    check_instance_id_format, \
    check_optional_key_source_value_scalar, \
    get_optional_key_source_value_ndimensions, \
    check_instance_optional_key_standard_pairs_format, \
    check_instnace_optional_key_map, \
    check_instance_optional_key_marked_required_are_present, \
    check_property_instances

__version__ = '1.0.0'

__all__ = [
    "shape",
    "size",
    "is_array_uniform",
    "create_full_array",
    "extend_full_array",
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
    "check_instnace_optional_key_map",
    "check_instance_optional_key_marked_required_are_present",
    "check_property_instances",
    "kim_properties",
    "property_id_to_property_name",
    "property_name_to_property_id",
    "kim_property_create",
    "kim_property_destroy",
    "kim_property_modify",
    "kim_property_remove",
    "kim_property_dump",
]

__author__ = 'Yaser Afshar <yafshar@umn.edu>'

try:
    import kim_edn
except:
    msg = '\nERROR: Failed to import the `kim_edn` utility module.'
    raise KIMPropertyError(msg)

kim_property_files = [
    join("atomic-mass", "2016-05-11-brunnels@noreply.openkim.org", "atomic-mass.edn"),
    join("bulk-modulus-isothermal-cubic-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "bulk-modulus-isothermal-cubic-crystal-npt.edn"),
    join("bulk-modulus-isothermal-hexagonal-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "bulk-modulus-isothermal-hexagonal-crystal-npt.edn"),
    join("cohesive-energy-lattice-invariant-shear-path-cubic-crystal", "2015-05-26-staff@noreply.openkim.org",
         "cohesive-energy-lattice-invariant-shear-path-cubic-crystal.edn"),
    join("cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal", "2015-05-26-staff@noreply.openkim.org",
         "cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal.edn"),
    join("cohesive-energy-relation-cubic-crystal", "2014-04-15-staff@noreply.openkim.org",
         "cohesive-energy-relation-cubic-crystal.edn"),
    join("cohesive-energy-shear-stress-path-cubic-crystal", "2015-05-26-staff@noreply.openkim.org",
         "cohesive-energy-shear-stress-path-cubic-crystal.edn"),
    join("cohesive-free-energy-cubic-crystal", "2014-04-15-staff@noreply.openkim.org",
         "cohesive-free-energy-cubic-crystal.edn"),
    join("cohesive-free-energy-hexagonal-crystal", "2014-04-15-staff@noreply.openkim.org",
         "cohesive-free-energy-hexagonal-crystal.edn"),
    join("cohesive-potential-energy-2d-hexagonal-crystal", "2015-05-26-staff@noreply.openkim.org",
         "cohesive-potential-energy-2d-hexagonal-crystal.edn"),
    join("cohesive-potential-energy-cubic-crystal", "2014-04-15-staff@noreply.openkim.org",
         "cohesive-potential-energy-cubic-crystal.edn"),
    join("cohesive-potential-energy-hexagonal-crystal", "2014-04-15-staff@noreply.openkim.org",
         "cohesive-potential-energy-hexagonal-crystal.edn"),
    join("configuration-cluster-fixed", "2014-04-15-staff@noreply.openkim.org",
         "configuration-cluster-fixed.edn"),
    join("configuration-cluster-relaxed", "2014-04-15-staff@noreply.openkim.org",
         "configuration-cluster-relaxed.edn"),
    join("configuration-nonorthogonal-periodic-3d-cell-fixed-particles-fixed", "2014-04-15-staff@noreply.openkim.org",
         "configuration-nonorthogonal-periodic-3d-cell-fixed-particles-fixed.edn"),
    join("configuration-nonorthogonal-periodic-3d-cell-fixed-particles-relaxed", "2014-04-15-staff@noreply.openkim.org",
         "configuration-nonorthogonal-periodic-3d-cell-fixed-particles-relaxed.edn"),
    join("configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-fixed", "2014-04-15-staff@noreply.openkim.org",
         "configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-fixed.edn"),
    join("configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-relaxed", "2014-04-15-staff@noreply.openkim.org",
         "configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-relaxed.edn"),
    join("configuration-periodic-2d-cell-fixed-particles-fixed", "2015-10-12-staff@noreply.openkim.org",
         "configuration-periodic-2d-cell-fixed-particles-fixed.edn"),
    join("elastic-constants-first-strain-gradient-isothermal-cubic-crystal-npt", "2016-05-24-staff@noreply.openkim.org",
         "elastic-constants-first-strain-gradient-isothermal-cubic-crystal-npt.edn"),
    join("elastic-constants-first-strain-gradient-isothermal-monoatomic-hexagonal-crystal-npt", "2016-05-24-staff@noreply.openkim.org",
         "elastic-constants-first-strain-gradient-isothermal-monoatomic-hexagonal-crystal-npt.edn"),
    join("elastic-constants-isothermal-cubic-crystal-npt", "2014-05-21-staff@noreply.openkim.org",
         "elastic-constants-isothermal-cubic-crystal-npt.edn"),
    join("enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-npt", "2017-07-31-staff@noreply.openkim.org",
         "enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-npt.edn"),
    join("enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-nvt", "2017-07-31-staff@noreply.openkim.org",
         "enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-nvt.edn"),
    join("extrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "extrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt.edn"),
    join("gamma-surface-relaxed-fcc-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "gamma-surface-relaxed-fcc-crystal-npt.edn"),
    join("grain-boundary-symmetric-tilt-energy-ideal-cubic-crystal", "2016-01-23-brunnels@noreply.openkim.org",
         "grain-boundary-symmetric-tilt-energy-ideal-cubic-crystal.edn"),
    join("grain-boundary-symmetric-tilt-energy-relaxed-cubic-crystal", "2016-01-23-brunnels@noreply.openkim.org",
         "grain-boundary-symmetric-tilt-energy-relaxed-cubic-crystal.edn"),
    join("grain-boundary-symmetric-tilt-energy-relaxed-relation-cubic-crystal", "2016-02-18-brunnels@noreply.openkim.org",
         "grain-boundary-symmetric-tilt-energy-relaxed-relation-cubic-crystal.edn"),
    join("intrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "intrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt.edn"),
    join("linear-thermal-expansion-coefficient-cubic-crystal-npt", "2015-07-30-staff@noreply.openkim.org",
         "linear-thermal-expansion-coefficient-cubic-crystal-npt.edn"),
    join("melting-temperature-constant-pressure-cubic-crystal", "2014-08-21-staff@noreply.openkim.org",
         "melting-temperature-constant-pressure-cubic-crystal.edn"),
    join("monovacancy-formation-energy-monoatomic-cubic-diamond", "2014-04-15-staff@noreply.openkim.org",
         "monovacancy-formation-energy-monoatomic-cubic-diamond.edn"),
    join("monovacancy-neutral-formation-free-energy-crystal-npt", "2015-07-28-staff@noreply.openkim.org",
         "monovacancy-neutral-formation-free-energy-crystal-npt.edn"),
    join("monovacancy-neutral-migration-energy-crystal-npt", "2015-09-16-staff@noreply.openkim.org",
         "monovacancy-neutral-migration-energy-crystal-npt.edn"),
    join("monovacancy-neutral-relaxation-volume-crystal-npt", "2015-07-28-staff@noreply.openkim.org",
         "monovacancy-neutral-relaxation-volume-crystal-npt.edn"),
    join("monovacancy-neutral-relaxed-formation-potential-energy-crystal-npt", "2015-07-28-staff@noreply.openkim.org",
         "monovacancy-neutral-relaxed-formation-potential-energy-crystal-npt.edn"),
    join("monovacancy-neutral-unrelaxed-formation-potential-energy-crystal-npt", "2015-07-28-staff@noreply.openkim.org",
         "monovacancy-neutral-unrelaxed-formation-potential-energy-crystal-npt.edn"),
    join("phonon-dispersion-dos-cubic-crystal-npt", "2014-05-21-staff@noreply.openkim.org",
         "phonon-dispersion-dos-cubic-crystal-npt.edn"),
    join("phonon-dispersion-relation-cubic-crystal-npt", "2014-05-21-staff@noreply.openkim.org",
         "phonon-dispersion-relation-cubic-crystal-npt.edn"),
    join("shear-stress-path-cubic-crystal", "2015-05-26-staff@noreply.openkim.org",
         "shear-stress-path-cubic-crystal.edn"),
    join("stacking-fault-relaxed-energy-curve-fcc-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "stacking-fault-relaxed-energy-curve-fcc-crystal-npt.edn"),
    join("structure-2d-hexagonal-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "structure-2d-hexagonal-crystal-npt.edn"),
    join("structure-cubic-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-cubic-crystal-npt.edn"),
    join("structure-hexagonal-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-hexagonal-crystal-npt.edn"),
    join("structure-monoclinic-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-monoclinic-crystal-npt.edn"),
    join("structure-orthorhombic-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-orthorhombic-crystal-npt.edn"),
    join("structure-rhombohedral-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-rhombohedral-crystal-npt.edn"),
    join("structure-tetragonal-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-tetragonal-crystal-npt.edn"),
    join("structure-triclinic-crystal-npt", "2014-04-15-staff@noreply.openkim.org",
         "structure-triclinic-crystal-npt.edn"),
    join("surface-energy-broken-bond-fit-cubic-bravais-crystal-npt", "2014-05-21-staff@noreply.openkim.org",
         "surface-energy-broken-bond-fit-cubic-bravais-crystal-npt.edn"),
    join("surface-energy-cubic-crystal-npt", "2014-05-21-staff@noreply.openkim.org",
         "surface-energy-cubic-crystal-npt.edn"),
    join("surface-energy-ideal-cubic-crystal", "2014-05-21-staff@noreply.openkim.org",
         "surface-energy-ideal-cubic-crystal.edn"),
    join("unstable-stacking-fault-relaxed-energy-fcc-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "unstable-stacking-fault-relaxed-energy-fcc-crystal-npt.edn"),
    join("unstable-twinning-fault-relaxed-energy-fcc-crystal-npt", "2015-05-26-staff@noreply.openkim.org",
         "unstable-twinning-fault-relaxed-energy-fcc-crystal-npt.edn"),
    join("verification-check", "2017-02-01-tadmor@noreply.openkim.org",
         "verification-check.edn"),
]
"""list: KIM property files."""

kim_property_files_path = join("external", "openkim-properties", "properties")
"""str: KIM property files path.

An absolute path (or a valid relative path) to the KIM property files folder.
"""

if isdir(abspath(kim_property_files_path)):
    kim_property_files_path = abspath(kim_property_files_path)
elif isdir(abspath(join(pardir, kim_property_files_path))):
    kim_property_files_path = abspath(join(pardir, kim_property_files_path))
elif isdir(abspath(join(pardir, pardir, kim_property_files_path))):
    kim_property_files_path = abspath(
        join(pardir, pardir, kim_property_files_path))
elif isdir(abspath(join(pardir, pardir, pardir, kim_property_files_path))):
    kim_property_files_path = abspath(
        join(pardir, pardir, pardir, kim_property_files_path))
else:
    kim_property_files_path = join(dirname(abspath(__file__)), "properties")
    if not isdir(kim_property_files_path):
        msg = '\nERROR: property files can not be found!'
        raise KIMPropertyError(msg)

for _i, _file in enumerate(kim_property_files):
    kim_property_files[_i] = join(kim_property_files_path, _file)

del(_i)
del(_file)

kim_property_names = [
    "atomic-mass",
    "bulk-modulus-isothermal-cubic-crystal-npt",
    "bulk-modulus-isothermal-hexagonal-crystal-npt",
    "cohesive-energy-lattice-invariant-shear-path-cubic-crystal",
    "cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal",
    "cohesive-energy-relation-cubic-crystal",
    "cohesive-energy-shear-stress-path-cubic-crystal",
    "cohesive-free-energy-cubic-crystal",
    "cohesive-free-energy-hexagonal-crystal",
    "cohesive-potential-energy-2d-hexagonal-crystal",
    "cohesive-potential-energy-cubic-crystal",
    "cohesive-potential-energy-hexagonal-crystal",
    "configuration-cluster-fixed",
    "configuration-cluster-relaxed",
    "configuration-nonorthogonal-periodic-3d-cell-fixed-particles-fixed",
    "configuration-nonorthogonal-periodic-3d-cell-fixed-particles-relaxed",
    "configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-fixed",
    "configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-relaxed",
    "configuration-periodic-2d-cell-fixed-particles-fixed",
    "elastic-constants-first-strain-gradient-isothermal-cubic-crystal-npt",
    "elastic-constants-first-strain-gradient-isothermal-monoatomic-hexagonal-crystal-npt",
    "elastic-constants-isothermal-cubic-crystal-npt",
    "enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-npt",
    "enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-nvt",
    "extrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt",
    "gamma-surface-relaxed-fcc-crystal-npt",
    "grain-boundary-symmetric-tilt-energy-ideal-cubic-crystal",
    "grain-boundary-symmetric-tilt-energy-relaxed-cubic-crystal",
    "grain-boundary-symmetric-tilt-energy-relaxed-relation-cubic-crystal",
    "intrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt",
    "linear-thermal-expansion-coefficient-cubic-crystal-npt",
    "melting-temperature-constant-pressure-cubic-crystal",
    "monovacancy-formation-energy-monoatomic-cubic-diamond",
    "monovacancy-neutral-formation-free-energy-crystal-npt",
    "monovacancy-neutral-migration-energy-crystal-npt",
    "monovacancy-neutral-relaxation-volume-crystal-npt",
    "monovacancy-neutral-relaxed-formation-potential-energy-crystal-npt",
    "monovacancy-neutral-unrelaxed-formation-potential-energy-crystal-npt",
    "phonon-dispersion-dos-cubic-crystal-npt",
    "phonon-dispersion-relation-cubic-crystal-npt",
    "shear-stress-path-cubic-crystal",
    "stacking-fault-relaxed-energy-curve-fcc-crystal-npt",
    "structure-2d-hexagonal-crystal-npt",
    "structure-cubic-crystal-npt",
    "structure-hexagonal-crystal-npt",
    "structure-monoclinic-crystal-npt",
    "structure-orthorhombic-crystal-npt",
    "structure-rhombohedral-crystal-npt",
    "structure-tetragonal-crystal-npt",
    "structure-triclinic-crystal-npt",
    "surface-energy-broken-bond-fit-cubic-bravais-crystal-npt",
    "surface-energy-cubic-crystal-npt",
    "surface-energy-ideal-cubic-crystal",
    "unstable-stacking-fault-relaxed-energy-fcc-crystal-npt",
    "unstable-twinning-fault-relaxed-energy-fcc-crystal-npt",
    "verification-check",
]
"""list: KIM property names."""

kim_property_ids = [
    "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass",
    "tag:staff@noreply.openkim.org,2014-04-15:property/bulk-modulus-isothermal-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/bulk-modulus-isothermal-hexagonal-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-lattice-invariant-shear-path-cubic-crystal",
    "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal",
    "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-shear-stress-path-cubic-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-free-energy-cubic-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-free-energy-hexagonal-crystal",
    "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-potential-energy-2d-hexagonal-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-potential-energy-cubic-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-potential-energy-hexagonal-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-cluster-fixed",
    "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-cluster-relaxed",
    "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-fixed-particles-fixed",
    "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-fixed-particles-relaxed",
    "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-fixed",
    "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-relaxed",
    "tag:staff@noreply.openkim.org,2015-10-12:property/configuration-periodic-2d-cell-fixed-particles-fixed",
    "tag:staff@noreply.openkim.org,2016-05-24:property/elastic-constants-first-strain-gradient-isothermal-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2016-05-24:property/elastic-constants-first-strain-gradient-isothermal-monoatomic-hexagonal-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-05-21:property/elastic-constants-isothermal-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2017-07-31:property/enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2017-07-31:property/enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-nvt",
    "tag:staff@noreply.openkim.org,2015-05-26:property/extrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-05-26:property/gamma-surface-relaxed-fcc-crystal-npt",
    "tag:brunnels@noreply.openkim.org,2016-01-23:property/grain-boundary-symmetric-tilt-energy-ideal-cubic-crystal",
    "tag:brunnels@noreply.openkim.org,2016-01-23:property/grain-boundary-symmetric-tilt-energy-relaxed-cubic-crystal",
    "tag:brunnels@noreply.openkim.org,2016-02-18:property/grain-boundary-symmetric-tilt-energy-relaxed-relation-cubic-crystal",
    "tag:staff@noreply.openkim.org,2015-05-26:property/intrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-07-30:property/linear-thermal-expansion-coefficient-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-08-21:property/melting-temperature-constant-pressure-cubic-crystal",
    "tag:staff@noreply.openkim.org,2014-04-15:property/monovacancy-formation-energy-monoatomic-cubic-diamond",
    "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-formation-free-energy-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-09-16:property/monovacancy-neutral-migration-energy-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-relaxation-volume-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-relaxed-formation-potential-energy-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-unrelaxed-formation-potential-energy-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-05-21:property/phonon-dispersion-dos-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-05-21:property/phonon-dispersion-relation-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-05-26:property/shear-stress-path-cubic-crystal",
    "tag:staff@noreply.openkim.org,2015-05-26:property/stacking-fault-relaxed-energy-curve-fcc-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-05-26:property/structure-2d-hexagonal-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-hexagonal-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-monoclinic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-orthorhombic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-rhombohedral-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-tetragonal-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-04-15:property/structure-triclinic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-05-21:property/surface-energy-broken-bond-fit-cubic-bravais-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-05-21:property/surface-energy-cubic-crystal-npt",
    "tag:staff@noreply.openkim.org,2014-05-21:property/surface-energy-ideal-cubic-crystal",
    "tag:staff@noreply.openkim.org,2015-05-26:property/unstable-stacking-fault-relaxed-energy-fcc-crystal-npt",
    "tag:staff@noreply.openkim.org,2015-05-26:property/unstable-twinning-fault-relaxed-energy-fcc-crystal-npt",
    "tag:tadmor@noreply.openkim.org,2017-02-01:property/verification-check",
]
"""list: KIM property full IDs."""

kim_properties = {k: v for k, v in zip(
    kim_property_ids, kim_property_files)}
"""dict: KIM properties dictionary indexed by properties full IDs."""

property_name_to_property_id = {k: v for k, v in zip(
    kim_property_names, kim_property_ids)}
"""dict: KIM properties name to full ID dictionary."""

property_id_to_property_name = {k: v for k, v in zip(
    kim_property_ids, kim_property_names)}
"""dict: KIM properties full ID to name dictionary."""


def kim_property_create(instance_id, property_name, property_instances=None):
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
        property_name {string} -- A string containing the property name or
        unique ID of the property.
        property_instances {string} -- A string containing the serialized
        KIM-EDN formatted property instances. (default: {None})

    Returns:
        string -- serialized KIM-EDN formatted property instances.

    """
    if not isinstance(instance_id, int):
        msg = '\nERROR: the "instance_id" is not an `int`.'
        raise KIMPropertyError(msg)

    # Check instance id format to prevent mistakes as early as possible
    check_instance_id_format(instance_id)

    if not isinstance(property_name, str):
        msg = '\nERROR: the "property_name" is not an `str`.'
        raise KIMPropertyError(msg)

    if property_instances is None:
        kim_property_instances = []
    else:
        # Deserialize the KIM property instances.
        kim_property_instances = kim_edn.loads(property_instances)

        for a_property_instance in kim_property_instances:
            if instance_id == a_property_instance["instance-id"]:
                msg = '\nERROR: the "instance-id"’s cannot repeat.'
                raise KIMPropertyError(msg)

    new_property_instance = {}

    if property_name in kim_property_names:
        new_property_instance["property-id"] = property_name_to_property_id[property_name]
    elif property_name in kim_property_ids:
        new_property_instance["property-id"] = property_name
    else:
        msg = '\nERROR: the input "property_name" :\n'
        msg += '"{}" \n'.format(property_name)
        msg += 'is not a valid KIM property name.'
        raise KIMPropertyError(msg)

    new_property_instance["instance-id"] = instance_id

    # Add the newly created property instance to the collection
    kim_property_instances.append(new_property_instance)

    # Return the serialize KIM property instances
    return kim_edn.dumps(kim_property_instances)


def kim_property_destroy(property_instances, instance_id):
    """Destroy a kim property instance.

    Delete a previously created property instance.

    For example::

    >>> obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    >>> kim_property_destroy(obj, 1)
    '[]'

    >>> obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

    >>> kim_property_destroy(obj, 2)
    '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

    Arguments:
        property_instances {string} -- A string containing the serialized
        KIM-EDN formatted property instances.
        instance_id {int} -- A positive integer identifying the property
        instance.

    Returns:
        string -- serialized KIM-EDN formatted property instances.

    """
    if not isinstance(instance_id, int):
        msg = '\nERROR: the "instance_id" is not an `int`.'
        raise KIMPropertyError(msg)

    if property_instances is None or \
            property_instances == 'None' or \
            property_instances == '' or \
            property_instances == '[]':
        return '[]'

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    for a_property_instance in kim_property_instances:
        if instance_id == a_property_instance["instance-id"]:
            kim_property_instances.remove(a_property_instance)

    # Return the serialize KIM property instances
    return kim_edn.dumps(kim_property_instances)


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
        if p["instance-id"] == instance_id:
            a_property_instance = p
            break

    if a_property_instance is None:
        msg = '\nERROR: The requested instance id :\n'
        msg += '{} \n'.format(instance_id)
        msg += 'does not match any of the property instances ids.'
        raise KIMPropertyError(msg)

    # Get the property definition id
    property_id = a_property_instance["property-id"]

    # property definition
    property_def = kim_edn.load(kim_properties[property_id])

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
                msg = '\nERROR: wrong keyword. \n The input '
                msg += '"{}"-key is not defined in '.format(new_keyword)
                msg += 'the property definition \n'
                msg += '({})'.format(property_def['property-id'])
                raise KIMPropertyError(msg)

            # Get the number of dimensions, shape and type of the key
            new_keyword_ndims = get_optional_key_extent_ndimensions(
                property_def[new_keyword]['extent'])
            new_keyword_shape = get_optional_key_extent_shape(
                property_def[new_keyword]['extent'])
            new_keyword_type = property_def[new_keyword]['type']

            if new_keyword in a_property_instance:
                if new_keyword_ndims == 0:
                    msg = '\nERROR: you can not append any extra value to '
                    msg += 'the scalar variable.'
                    raise KIMPropertyError(msg)

                new_keyword_map = a_property_instance[new_keyword]
            else:
                new_keyword_map = {}
                a_property_instance[new_keyword] = new_keyword_map

            i += 1
            continue

        new_keyword_key = arg
        i += 1

        if not new_keyword_key in standard_keys:
            msg = '\nERROR: Wrong key. \n The input '
            msg += '"{}"-key is not part of '.format(new_keyword_key)
            msg += 'the standard key-value pairs definition.'
            raise KIMPropertyError(msg)

        if new_keyword_key == 'source-unit':
            if not property_def[new_keyword]['has-unit']:
                msg = '\nERROR: Wrong key.\nThe unit is wrongly provided '
                msg += 'to a key that does not have a unit.\n'
                msg += 'The corresponding "has-unit" key in the property '
                msg += 'definition has `False` value.'
                raise KIMPropertyError(msg)

        if new_keyword_key in STANDARD_KEYS_WITH_EXTENT:
            if new_keyword_ndims > 0:
                if i + new_keyword_ndims - 1 > n_arguments:
                    msg = '\nERROR: there is not enough input arguments to '
                    msg += 'use. The input number of arguments = '
                    msg += '{} are less than the '.format(n_arguments)
                    msg += 'required number of arguments = '
                    msg += '{}.'.format(i + new_keyword_ndims - 1)
                    raise KIMPropertyError(msg)
            else:
                if i > n_arguments:
                    msg = '\nERROR: there is not enough input arguments to '
                    msg += 'use. The input number of arguments = '
                    msg += '{} are less than the '.format(n_arguments)
                    msg += 'required number of arguments = '
                    msg += '{}.'.format(i)
                    raise KIMPropertyError(msg)

            # Append
            if new_keyword_key in new_keyword_map:
                new_keyword_value = new_keyword_map[new_keyword_key]
                new_keyword_shape_new = shape(new_keyword_value)
                new_keyword_index = []
                _n = -1
                _l = 0
                _u = 0
                for n in range(new_keyword_ndims):
                    arg = str(argv[i])
                    if re.match(r'^[1-9][0-9]*$', arg) is None:
                        if re.match(r'^[1-9][:0-9]*$', arg) is None:
                            msg = '\nERROR: requested index '
                            msg += '"{}" '.format(arg)
                            msg += 'doesn\'t meet the format specification '
                            msg += '(an integer equal to or greater than 1 '
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
                                msg = '\nERROR: this dimension has a fixed '
                                msg += 'length = '
                                msg += '{}, '.format(new_keyword_shape[n])
                                msg += 'while, wrong index = {} '.format(_u)
                                msg += 'is requested.'
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
                            msg += 'is requested.'
                            raise KIMPropertyError(msg)
                        if new_keyword_shape[n] == 1 and int(arg) > 1:
                            if property_def[new_keyword]["extent"][n] == ':':
                                if new_keyword_shape_new[n] < int(arg):
                                    new_keyword_shape_new[n] = int(arg)
                            else:
                                msg = '\nERROR: this dimension has a fixed '
                                msg += 'length = 1, while, wrong index = '
                                msg += '{} '.format(arg)
                                msg += 'is requested.'
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
                    if i + _u - _l - 1 > n_arguments:
                        msg = '\nERROR: there is not enough input arguments '
                        msg += 'to use. The input number of arguments = '
                        msg += '{} are less than the '.format(n_arguments)
                        msg += 'required number of arguments = '
                        msg += '{}.'.format(i + _u - _l - 1)
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
                    if i > n_arguments:
                        msg = '\nERROR: there is not enough input arguments '
                        msg += 'to use. The input number of arguments = '
                        msg += '{} are less than the '.format(n_arguments)
                        msg += 'required number of arguments = '
                        msg += '{}.'.format(i)
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
                                    msg += '{} is requested.'.format(_u)
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
                                msg += '{} is requested.'.format(arg)
                                raise KIMPropertyError(msg)
                            if new_keyword_shape[n] == 1 and int(arg) > 1:
                                if property_def[new_keyword]["extent"][n] == ':':
                                    new_keyword_shape_new[n] = int(arg)
                                else:
                                    msg = '\nERROR: this dimension has a '
                                    msg += 'fixed length = 1, while, wrong '
                                    msg += 'index = {} '.format(arg)
                                    msg += 'is requested.'
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
                        if i + _u - _l - 1 > n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use. The input number of '
                            msg += 'arguments = {} are '.format(n_arguments)
                            msg += 'less than the required number of '
                            msg += 'arguments = {}.'.format(i + _u - _l - 1)
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
                        if i > n_arguments:
                            msg = '\nERROR: there is not enough input '
                            msg += 'arguments to use. The input number of '
                            msg += 'arguments = {} are '.format(n_arguments)
                            msg += 'less than the required number of '
                            msg += 'arguments = {}.'.format(i)
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

            if i > n_arguments:
                msg = '\nERROR: there is not enough input arguments to '
                msg += 'use. The input number of arguments = '
                msg += '{} are less than the '.format(n_arguments)
                msg += 'required number of arguments = '
                msg += '{}.'.format(i)
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


def kim_property_remove(property_instances, instance_id, *argv):
    """Remove or delete a key from the property instance.

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
        msg = '\nERROR: There is no property instance to remove the content.'
        raise KIMPropertyError(msg)

    if not isinstance(instance_id, int):
        msg = '\nERROR: the "instance_id" is not an `int`.'
        raise KIMPropertyError(msg)

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    a_property_instance = None

    for p in kim_property_instances:
        if p["instance-id"] == instance_id:
            a_property_instance = p
            break

    if a_property_instance is None:
        msg = '\nERROR: There requested instance id :\n'
        msg += '{} \n'.format(instance_id)
        msg += 'doesn\'t match any of the property instances ids.'
        raise KIMPropertyError(msg)

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
            msg = '\nERROR: unexpected index exception happened.'
            raise KIMPropertyError(msg)

        if arg == 'key':
            k_keyword = True
            i += 1
            continue

        if k_keyword:
            k_keyword = False

            # new keyword
            new_keyword = arg
            if new_keyword not in a_property_instance:
                msg = '\nERROR: the key {} '.format(new_keyword)
                msg += 'doesn\'t exist in the property instance.'
                raise KIMPropertyError(msg)

            # Remove the whole key if it is requested
            if i + 1 < n_arguments:
                try:
                    arg = argv[i + 1]
                except IndexError:
                    msg = '\nERROR: unexpected index exception happened.'
                    raise KIMPropertyError(msg)

                if arg == 'key':
                    del a_property_instance[new_keyword]
                    i += 1
                    continue
            # There is no more argument delete a key and stop
            else:
                del a_property_instance[new_keyword]
                break

            new_keyword_map = a_property_instance[new_keyword]

            i += 1
            continue

        if arg in new_keyword_map:
            del new_keyword_map[arg]

        i += 1
        continue

    return kim_edn.dumps(kim_property_instances)


def kim_property_dump(property_instances, fp, *,
                      fp_path=kim_property_files_path,
                      cls=None, indent=4, default=None, sort_keys=False):
    """Serialize ``property_instances`` object.

    Arguments:
        property_instances {string} -- A string containing the serialized
        KIM-EDN formatted property instances.

        fp {a ``.write()``-supporting file-like object or a name string to
        open a file} -- Serialize ``property_instances`` as a KIM-EDN
        formatted stream to ``fp``

    Keyword Arguments:
        fp_path should be an absolute path (or a valid relative path)
        to the KIM property definition folder. (default: kim_property_files_path)

        To use a custom ``KIMEDNEncoder`` subclass (e.g. one that overrides
        the ``.default()`` method to serialize additional types), specify it
        with the ``cls`` kwarg; otherwise ``KIMEDNEncoder`` is used.

        If ``indent`` is a non-negative integer, then EDN array elements and
        object members will be pretty-printed with that indent level. An
        indent level of 0 will only insert newlines. (default 4)

        ``default(obj)`` is a function that should return a serializable
        version of obj or raise TypeError. The default simply raises
        TypeError.

        If *sort_keys* is true (default: ``False``), then the output of
        dictionaries will be sorted by key.

    """
    if property_instances is None or \
            property_instances == 'None' or \
            property_instances == '' or \
            property_instances == '[]':
        msg = '\nERROR: There is no property instance to modify the content.'
        raise KIMPropertyError(msg)

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    # Check the property instances
    check_property_instances(
        kim_property_instances, fp_path=fp_path)

    if len(kim_property_instances) == 1:
        kim_edn.dump(kim_property_instances[0], fp, cls=cls,
                     indent=indent, default=default, sort_keys=sort_keys)
    else:
        kim_edn.dump(kim_property_instances, fp, cls=cls,
                     indent=indent, default=default, sort_keys=sort_keys)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
