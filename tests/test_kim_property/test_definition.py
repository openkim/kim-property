import os
from os.path import join, isfile
import re

try:
    import kim_edn
except:
    raise Exception('Failed to import `kim_edn` utility module')

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

    def test_get_optional_key_extent_ndimensions(self):
        """Test the key-extent ndimensions component."""
        for i, e in enumerate(EXTENT_LIST):
            n1 = self.kim_property.get_optional_key_extent_ndimensions(e)
            n2 = EXTENT_LIST_NDIMS[i]
            self.assertTrue(n1 == n2)

    def test_get_optional_key_extent_shape(self):
        """Test the key-extent shape component."""
        for i, e in enumerate(EXTENT_LIST):
            n1 = self.kim_property.get_optional_key_extent_shape(e)
            n2 = EXTENT_LIST_SHAPES[i]
            self.assertTrue(n1 == n2)

    def test_check_optional_key_extent_scalar(self):
        """Test the key-extent checking scalar component."""
        for i, e in enumerate(EXTENT_LIST):
            n1 = self.kim_property.check_optional_key_extent_scalar(e)
            n2 = EXTENT_LIST_SCLAR[i]
            self.assertTrue(n1 == n2)


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
        edn_file = join("tests", "fixtures", "properties", "atomic-mass",
                        "2016-05-11-brunnels@noreply.openkim.org",
                        "atomic-mass.edn")
        self.assertTrue(isfile(edn_file))

        pd = kim_edn.load(edn_file)

        fp = kim_edn.dumps(pd)

        # Complete check on the property definition
        self.kim_property.check_property_definition(fp)

    def test_property(self):
        """Check the property definition."""
        for k, edn_file in self.kim_property.kim_properties.items():
            self.assertTrue(isfile(edn_file))

            if self.kim_property.property_id_to_property_name[k] in EXCEPTIONS:
                # Complete check on the property definition
                self.kim_property.check_property_definition(
                    edn_file, _m=KEY_FORMAT.match)
            else:
                # Complete check on the property definition
                self.kim_property.check_property_definition(edn_file)


class TestPyTestPropertyDefinitionModuleComponents(TestPropertyDefinitionModuleComponents, PyTest):
    pass


class TestPyTestPropertyDefinition(TestPropertyDefinition, PyTest):
    pass
