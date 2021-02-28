import os
from os.path import join, isfile
import re

import kim_edn

from kim_property.create import PROPERTY_ID_TO_PROPERTY_NAME
from tests.test_kim_property import PyTest

EXTENT_LIST = [
    [":"],
    [],
    [1, ],
    [":", 3],
    [6],
    [6, 3],
    [":", 3, ":"],
    [":", ":"],
    [":", ],
    [6, ],
    [":", 3, ":", ],
]

EXTENT_LIST_NDIMS = [
    1,  # [":"],
    0,  # [],
    0,  # [1,],
    2,  # [":", 3],
    1,  # [6],
    2,  # [6, 3],
    3,  # [":", 3, ":"],
    2,  # [":", ":"],
    1,  # [":", ],
    1,  # [6, ],
    3,  # [":", 3, ":", ],
]

EXTENT_LIST_SHAPES = [
    [1],  # [":"],
    [],  # [],
    [],  # [1,],
    [1, 3],  # [":", 3],
    [6],  # [6],
    [6, 3],  # [6, 3],
    [1, 3, 1],  # [":", 3, ":"],
    [1, 1],  # [":", ":"],
    [1],  # [":", ],
    [6],  # [6, ],
    [1, 3, 1],  # [":", 3, ":", ],
]

EXTENT_LIST_SCLAR = [
    False,  # [":"],
    True,  # [],
    True,  # [1,],
    False,  # [":", 3],
    False,  # [6],
    False,  # [6, 3],
    False,  # [":", 3, ":"],
    False,  # [":", ":"],
    False,  # [":", ],
    False,  # [6, ],
    False,  # [":", 3, ":", ],
]


class TestPropertyDefinitionModuleComponents:
    """Test property definition utility module components."""

    def test_check_key_present(self):
        """Test if a key is present."""
        # key is not an string
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_present,
                          1, '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]')

        # key does not exist
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_present,
                          "short-name", '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]')

        # key exists
        self.kim_property.check_key_present(
            "instance-id", '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]')

    def test_check_property_id_format(self):
        """Test if the property id fomrat is correct."""
        # Wrong property id format, input is not a string :
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          ["tags:taff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"])

        # Wrong property id format, tag with no :
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          "tagstaff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal")

        # Wrong property id format, wrong email address with a + :
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          "tag:staff+@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal")

        # Wrong property id format, wrong date format :
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          "tag:staff@noreply.openkim.org,15-04-2014:property/cohesive-energy-relation-cubic-crystal")

        # Wrong property id format, no seperator / :
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          "tag:staff@noreply.openkim.org,2014-04-15:propertycohesive-energy-relation-cubic-crystal")

        # Wrong property id format, property-id with capital letter:
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          "tag:staff@noreply.openkim.org,2014-04-15:property/Cohesive-energy-relation-cubic-crystal")

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_id_format,
                          "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-Energy-relation-cubic-crystal")

    def test_check_property_title_format(self):
        """Test if the property title includes an ending period."""
        # key is not an string
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_title_format,
                          ["Cohesive energy versus lattice constant relation for a cubic crystal."])

        # key ends in period
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_title_format,
                          "Cohesive energy versus lattice constant relation for a cubic crystal.")

    def test_check_required_keys_present(self):
        """Test if the required property keys are present."""
        str1 = '{"property-id" "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal" "property-title" "Cohesive energy for an unrelaxed lattice-invariant shear path deformation of a cubic crystal" "property-description" "Unrelaxed cohesive energy versus shear relation along a lattice-invariant deformation path of a cubic crystal at zero absolute temperature. The lattice-invariant shear path is defined by a shearing direction and shear plane normal relative to the reference conventional crystal coordinate system.  Unit cell atomic shifts are NOT minimized for each value of the shear parameter."}'

        obj1 = {"property-id": "tag:staff@noreply.openkim.org,2015-05-26:property/cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal",
                "property-title": "Cohesive energy for an unrelaxed lattice-invariant shear path deformation of a cubic crystal"}

        self.kim_property.check_required_keys_present(str1)

        # key is not an string
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_required_keys_present,
                          obj1)

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_required_keys_present,
                          list(obj1))

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_required_keys_present,
                          tuple(obj1))

    def test_check_key_format(self):
        """Test if the key format is correct."""
        # key is not an string
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_format,
                          ["short-name"])

        # key includes upper-case
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_format,
                          "Short-name")

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_format,
                          "short-Name")

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_format,
                          "short-namE")

        # key includes non alopha numeric
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_format,
                          "+short-name")

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_key_format,
                          "short\tname")

    def test_check_optional_key_type_format(self):
        """Test if the optional key type is a valid type."""
        # key is not an string
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_type_format,
                          ["float"])

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_type_format,
                          ("int", "int"))

        # key is not in str_type
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_type_format,
                          "long")

    def test_check_optional_key_extent_format(self):
        """Test if the optional key extent format is correct."""
        # key is not an string or list
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          (":"))

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          {":"})

        # invalid character
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          '[\':\']')

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          '[";"]')

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          [";"])

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          '[":", 2, , ";"]')

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          '["a"]')

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          [":", "a"])

        # key is a list with invalid input
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          [":", 2.34])

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_format,
                          [":", (1, 2)])

    def test_check_optional_key_extent_scalar(self):
        """Test the key-extent checking scalar component."""
        for i, e in enumerate(EXTENT_LIST):
            n1 = self.kim_property.check_optional_key_extent_scalar(e)
            n2 = EXTENT_LIST_SCLAR[i]
            self.assertTrue(n1 == n2)

        # input is not an string or list
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_scalar,
                          ())

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_extent_scalar,
                          {})

        # input is an empty string
        self.assertFalse(
            self.kim_property.check_optional_key_extent_scalar(""))

    def test_get_optional_key_extent_ndimensions(self):
        """Test the key-extent ndimensions component."""
        for i, e in enumerate(EXTENT_LIST):
            n1 = self.kim_property.get_optional_key_extent_ndimensions(e)
            n2 = EXTENT_LIST_NDIMS[i]
            self.assertTrue(n1 == n2)

        # input is not a list
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_extent_ndimensions,
                          ())

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_extent_ndimensions,
                          "[]")

    def test_get_optional_key_extent_shape(self):
        """Test the key-extent shape component."""
        for i, e in enumerate(EXTENT_LIST):
            n1 = self.kim_property.get_optional_key_extent_shape(e)
            n2 = EXTENT_LIST_SHAPES[i]
            self.assertTrue(n1 == n2)

        # input is not a list
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_extent_shape,
                          ())

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_extent_shape,
                          "[]")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_extent_shape,
                          [1, ":", "|"])

    def test_check_property_optional_key_standard_pairs_format(self):
        """Test if the standard key-map pairs format is correct."""
        # input is not a dict
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_optional_key_standard_pairs_format,
                          [])

        s = {"type": "string",
             "has-unit": False,
             "extent": [":"],
             "required": False,
             "description": "Short name defining the cubic crystal type."}

        self.kim_property.check_property_optional_key_standard_pairs_format(s)

        # has-unit is not a boolean

        s["has-unit"] = "False"

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_optional_key_standard_pairs_format,
                          s)

        # required is not a boolean
        s["has-unit"] = False
        s["required"] = "False"

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_optional_key_standard_pairs_format,
                          s)

        # description is not a string
        s["required"] = False
        s["description"] = []

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_optional_key_standard_pairs_format,
                          s)

        # key is not in standard keys
        s["description"] = "Short name defining the cubic crystal type."
        s["none"] = False

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_optional_key_standard_pairs_format,
                          s)

    def test_check_property_definition(self):
        """Test the KIM property definition format is correct."""
        # input is not a dict
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_definition,
                          {})

        s = '"property-id"'
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_definition,
                          s)


FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL

KEY_FORMAT = re.compile(r'^[ABa-z0-9\-].*$', FLAGS)

# There are keys in these file which do not conform with the KIM standard
# and starts with a capital character A or B
EXCEPTIONS = [
    "enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-npt",
    "enthalpy-of-mixing-curve-substitutional-binary-cubic-crystal-nvt"
]


class TestPropertyDefinition:
    """Test property definition utility module."""

    def test_commented_property(self):
        """Check the property definition in a commented edn property file."""
        # Test the commented property definition edn file
        edn_file = join("tests", "fixtures", "atomic-mass-commented.edn")

        self.assertTrue(isfile(edn_file))

        # Complete check on the property definition
        self.kim_property.check_property_definition(edn_file)

    def test_property_from_string(self):
        """Check the property definition from a KIM-EDN string."""
        # Property definition edn file
        edn_file = join("tests", "fixtures", "atomic-mass.edn")
        self.assertTrue(isfile(edn_file))

        pd = kim_edn.load(edn_file)

        fp = kim_edn.dumps(pd)

        # Complete check on the property definition
        self.kim_property.check_property_definition(fp)

    def test_property(self):
        """Check the property definition."""
        kim_properties = self.kim_property.get_properties()
        for k, pd in kim_properties.items():
            if PROPERTY_ID_TO_PROPERTY_NAME[k] in EXCEPTIONS:
                # Complete check on the property definition
                self.kim_property.check_property_definition(
                    pd, _m=KEY_FORMAT.match)
            else:
                # Complete check on the property definition
                self.kim_property.check_property_definition(pd)


class TestPyTestPropertyDefinitionModuleComponents(TestPropertyDefinitionModuleComponents, PyTest):
    pass


class TestPyTestPropertyDefinition(TestPropertyDefinition, PyTest):
    pass
