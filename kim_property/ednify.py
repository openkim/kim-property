"""KIM properties object serialization/de-serialization."""

from os.path import abspath, join, isdir, pardir, isfile, dirname
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
        # KIM property files.
        kim_property_files = []

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
            "dislocation-core-energy-cubic-crystal-npt",
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
            "crystal-structure-npt",
            "binding-energy-crystal",
            "bulk-modulus-isothermal-npt",
            "elastic-constants-isothermal-npt"
        ]

        # KIM property full IDs.
        kim_property_ids = [
            "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass",
            "tag:staff@noreply.openkim.org,2014-04-15:property/bulk-modulus-isothermal-cubic-crystal-npt",
            "tag:staff@noreply.openkim.org,2014-04-15:property/bulk-modulus-isothermal-hexagonal-crystal-npt",
            "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-lattice-invariant-shear-path-cubic-crystal",
            "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal",  # noqa: E501
            "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal",
            "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-shear-stress-path-cubic-crystal",
            "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-free-energy-cubic-crystal",
            "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-free-energy-hexagonal-crystal",
            "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-potential-energy-2d-hexagonal-crystal",
            "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-potential-energy-cubic-crystal",
            "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-potential-energy-hexagonal-crystal",
            "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-cluster-fixed",
            "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-cluster-relaxed",
            "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-fixed-particles-fixed",  # noqa: E501
            "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-fixed-particles-relaxed",  # noqa: E501
            "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-fixed",  # noqa: E501
            "tag:staff@noreply.openkim.org,2014-04-15:property/configuration-nonorthogonal-periodic-3d-cell-relaxed-particles-relaxed",  # noqa: E501
            "tag:staff@noreply.openkim.org,2015-10-12:property/configuration-periodic-2d-cell-fixed-particles-fixed",
            "tag:staff@noreply.openkim.org,2021-02-24:property/dislocation-core-energy-cubic-crystal-npt",
            "tag:staff@noreply.openkim.org,2016-05-24:property/elastic-constants-first-strain-gradient-isothermal-cubic-crystal-npt",  # noqa: E501
            "tag:staff@noreply.openkim.org,2016-05-24:property/elastic-constants-first-strain-gradient-isothermal-monoatomic-hexagonal-crystal-npt",  # noqa: E501
            "tag:staff@noreply.openkim.org,2014-05-21:property/elastic-constants-isothermal-cubic-crystal-npt",
            "tag:staff@noreply.openkim.org,2017-07-31:property/enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-npt",  # noqa: E501
            "tag:staff@noreply.openkim.org,2017-07-31:property/enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-nvt",  # noqa: E501
            "tag:staff@noreply.openkim.org,2015-05-26:property/extrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt",
            "tag:staff@noreply.openkim.org,2015-05-26:property/gamma-surface-relaxed-fcc-crystal-npt",
            "tag:brunnels@noreply.openkim.org,2016-01-23:property/grain-boundary-symmetric-tilt-energy-ideal-cubic-crystal",
            "tag:brunnels@noreply.openkim.org,2016-01-23:property/grain-boundary-symmetric-tilt-energy-relaxed-cubic-crystal",
            "tag:brunnels@noreply.openkim.org,2016-02-18:property/grain-boundary-symmetric-tilt-energy-relaxed-relation-cubic-crystal",  # noqa: E501
            "tag:staff@noreply.openkim.org,2015-05-26:property/intrinsic-stacking-fault-relaxed-energy-fcc-crystal-npt",
            "tag:staff@noreply.openkim.org,2015-07-30:property/linear-thermal-expansion-coefficient-cubic-crystal-npt",
            "tag:staff@noreply.openkim.org,2014-08-21:property/melting-temperature-constant-pressure-cubic-crystal",
            "tag:staff@noreply.openkim.org,2014-04-15:property/monovacancy-formation-energy-monoatomic-cubic-diamond",
            "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-formation-free-energy-crystal-npt",
            "tag:staff@noreply.openkim.org,2015-09-16:property/monovacancy-neutral-migration-energy-crystal-npt",
            "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-relaxation-volume-crystal-npt",
            "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-relaxed-formation-potential-energy-crystal-npt",  # noqa: E501
            "tag:staff@noreply.openkim.org,2015-07-28:property/monovacancy-neutral-unrelaxed-formation-potential-energy-crystal-npt",  # noqa: E501
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
            "tag:staff@noreply.openkim.org,2023-02-21:property/crystal-structure-npt",
            "tag:staff@noreply.openkim.org,2023-02-21:property/binding-energy-crystal",
            "tag:staff@noreply.openkim.org,2024-07-10:property/bulk-modulus-isothermal-npt",
            "tag:staff@noreply.openkim.org,2024-07-10:property/elastic-constants-isothermal-npt"
        ]

        for _id in kim_property_ids:
            _path, _, _, _ = get_property_id_path(_id)
            kim_property_files.append(join(kim_property_files_path, _path))
            if not isfile(kim_property_files[-1]):
                msg = 'the property file =\n"'
                msg += kim_property_files[-1]
                msg += '"\ncan not be found!'
                raise KIMPropertyError(msg)

        del kim_property_files_path

        # KIM properties dictionary indexed by properties full IDs.
        kim_properties = {
            k: kim_edn.load(v) for k, v in zip(kim_property_ids, kim_property_files)
        }

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
