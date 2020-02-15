import os
from os.path import join, isfile, split

from tests.test_kim_property import PyTest

SOURCE_VALUE = [
    [0, 0, 0, 0, 0, 0, ],
    "P-1",
    0,
    8.00524023,
    96.73127369,
    [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    "P2_1/c",
    ["Mn", "Mn", "Mn", "Mn"]
]

SOURCE_VALUE_TYPE = [
    "float",  # [0, 0, 0, 0, 0, 0, ],
    "string",  # "P-1",
    "float",  # 0,
    "float",  # 8.00524023,
    "float",  # 96.73127369,
    "float",  # [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    "string",  # "P2_1/c",
    "string",  # ["Mn", "Mn", "Mn", "Mn"]
]

SOURCE_VALUE_SCLAR = [
    False,  # [0, 0, 0, 0, 0, 0, ],
    True,  # "P-1",
    True,  # 0,
    True,  # 8.00524023,
    True,  # 96.73127369,
    False,  # [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    True,  # "P2_1/c",
    False,  # ["Mn", "Mn", "Mn", "Mn"]
]

SOURCE_VALUE_NDIMS = [
    1,  # [0, 0, 0, 0, 0, 0, ],
    0,  # "P-1",
    0,  # 0,
    0,  # 8.00524023,
    0,  # 96.73127369,
    2,  # [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    0,  # "P2_1/c",
    1,  # ["Mn", "Mn", "Mn", "Mn"]
]


class TestPropertyInstanceModuleComponents:
    """Test property instance utility module components."""

    def test_get_property_id_path(self):
        """Test the source-value checking scalar component."""
        for k, v in self.kim_property.kim_properties.items():
            _path, _, _, _property_name = self.kim_property.get_property_id_path(
                k)

            property_name = self.kim_property.property_id_to_property_name[k]
            self.assertTrue(_property_name == property_name)

            # Property definition edn file
            path = join("properties", _path)
            v_path = join("properties", split(split(split(v)[0])[
                          0])[-1], split(split(v)[0])[-1], split(v)[-1])
            self.assertTrue(path == v_path)

    def test_check_optional_key_source_value_scalar(self):
        """Test the source-value checking scalar component."""
        for i, e in enumerate(SOURCE_VALUE):
            n1 = self.kim_property.check_optional_key_source_value_scalar(
                e, SOURCE_VALUE_TYPE[i])
            n2 = SOURCE_VALUE_SCLAR[i]
            self.assertTrue(n1 == n2)

    def test_get_optional_key_source_value_ndimensions(self):
        """Test the source-value ndimensions component."""
        for i, e in enumerate(SOURCE_VALUE):
            n1 = self.kim_property.get_optional_key_source_value_ndimensions(e)
            n2 = SOURCE_VALUE_NDIMS[i]
            self.assertTrue(n1 == n2)


property_instance_names = [
    "RD_000018659700_000_data.edn",
    "RD_999984936526_000_data.edn",
]


class TestPropertyInstance:
    """Test property instance utility module."""

    def test_property(self):
        """Check the property instance."""
        for pi in property_instance_names:
            fi = join("tests", "fixtures", pi)

            self.assertTrue(isfile(fi))

            self.kim_property.check_property_instances(
                fi, fp_path=join("kim_property", "properties"))


class TestPyTestPropertyInstanceModuleComponents(TestPropertyInstanceModuleComponents, PyTest):
    pass


class TestPyTestPropertyInstance(TestPropertyInstance, PyTest):
    pass
