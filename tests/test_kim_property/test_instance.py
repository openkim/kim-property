from os.path import join, isfile

import kim_edn

from tests.test_kim_property import PyTest
from kim_property.create import PROPERTY_ID_TO_PROPERTY_NAME

SOURCE_VALUE = [
    [0, 0, 0, 0, 0, 0, ],
    "P-1",
    ["P-1"],
    0,
    8.00524023,
    96.73127369,
    [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    "P2_1/c",
    ["Mn", "Mn", "Mn", "Mn"],
    False
]

SOURCE_VALUE_TYPE = [
    "float",  # [0, 0, 0, 0, 0, 0, ],
    "string",  # "P-1",
    "string",  # ["P-1"],
    "float",  # 0,
    "float",  # 8.00524023,
    "float",  # 96.73127369,
    "float",  # [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    "string",  # "P2_1/c",
    "string",  # ["Mn", "Mn", "Mn", "Mn"]
    "bool",  # "False"
]

SOURCE_VALUE_SCLAR = [
    False,  # [0, 0, 0, 0, 0, 0, ],
    True,  # "P-1",
    False,  # ["P-1"],
    True,  # 0,
    True,  # 8.00524023,
    True,  # 96.73127369,
    False,  # [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    True,  # "P2_1/c",
    False,  # ["Mn", "Mn", "Mn", "Mn"]
    True,  # "False"
]

SOURCE_VALUE_NDIMS = [
    1,  # [0, 0, 0, 0, 0, 0, ],
    0,  # "P-1",
    1,  # ["P-1"],
    0,  # 0,
    0,  # 8.00524023,
    0,  # 96.73127369,
    2,  # [[0.75, 0.251749, 0.149543, ], [0.75, 0.751749, 0.350457, ]],
    0,  # "P2_1/c",
    1,  # ["Mn", "Mn", "Mn", "Mn"]
    0,  # "False"
]


class TestPropertyInstanceModuleComponents:
    """Test property instance utility module components."""

    def test_get_property_id_path(self):
        """Test the source-value checking scalar component."""
        kim_properties = self.kim_property.get_properties()
        for k, _ in kim_properties.items():
            _, _, _, _property_name = self.kim_property.get_property_id_path(
                k)

            property_name = PROPERTY_ID_TO_PROPERTY_NAME[k]
            self.assertTrue(_property_name == property_name)

    def test_check_instance_id_format(self):
        """Test if the instance id format is correct."""
        # instance-id is a float
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_id_format,
                          1.0)

        # instance-id is a negative
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_id_format,
                          -1)

        # instance-id is zero
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_id_format,
                          0)

        # instance-id is bool zero
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_id_format,
                          False)

    def test_check_optional_key_source_value_scalar(self):
        """Test the source-value checking scalar component."""
        for i, e in enumerate(SOURCE_VALUE):
            n1 = self.kim_property.check_optional_key_source_value_scalar(
                e, SOURCE_VALUE_TYPE[i])
            n2 = SOURCE_VALUE_SCLAR[i]
            self.assertTrue(n1 == n2)

        # input is not a list, str, float, int or bool
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_source_value_scalar,
                          (1,), "int")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_optional_key_source_value_scalar,
                          {1, }, "int")

        # input is float but type is different
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(1.0, "float"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1.0, "int"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1.0, "list"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1.0, "bool"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1.0, "string"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1.0, "file"))

        # input is int but type is float, or bool or different
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(1, "int"))
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(1, "float"))
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(1, "bool"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(2, "bool"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1, "list"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1, "string"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(1, "file"))

        # input is str but type file or is different
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar("Al", "string"))
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar("Al", "file"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar("Al", "float"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar("Al", "int"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar("Al", "list"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar("Al", "bool"))

        # input is bool but type is different
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(True, "bool"))
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(True, "int"))
        self.assertTrue(
            self.kim_property.check_optional_key_source_value_scalar(True, "float"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(True, "file"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(True, "string"))
        self.assertFalse(
            self.kim_property.check_optional_key_source_value_scalar(True, "list"))

    def test_get_optional_key_source_value_ndimensions(self):
        """Test the source-value ndimensions component."""
        for i, e in enumerate(SOURCE_VALUE):
            n1 = self.kim_property.get_optional_key_source_value_ndimensions(e)
            n2 = SOURCE_VALUE_NDIMS[i]
            self.assertTrue(n1 == n2)

        # input is not a list, str, float, int or bool
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_source_value_ndimensions,
                          (1,))

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_source_value_ndimensions,
                          (1, 2))

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_source_value_ndimensions,
                          {1, })

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.get_optional_key_source_value_ndimensions,
                          {1: 100, 2: 200})

        self.assertTrue(
            2 == self.kim_property.get_optional_key_source_value_ndimensions([[1]]))
        self.assertTrue(
            3 == self.kim_property.get_optional_key_source_value_ndimensions([[[1]]]))
        self.assertTrue(
            4 == self.kim_property.get_optional_key_source_value_ndimensions([[[[1]]]]))
        self.assertTrue(
            5 == self.kim_property.get_optional_key_source_value_ndimensions([[[[[1]]]]]))
        self.assertTrue(
            6 == self.kim_property.get_optional_key_source_value_ndimensions([[[[[[1]]]]]]))

        self.assertTrue(
            2 == self.kim_property.get_optional_key_source_value_ndimensions([[1, 2]]))
        self.assertTrue(
            3 == self.kim_property.get_optional_key_source_value_ndimensions([[[1, 2]]]))
        self.assertTrue(
            4 == self.kim_property.get_optional_key_source_value_ndimensions([[[[1, 2]]]]))
        self.assertTrue(
            5 == self.kim_property.get_optional_key_source_value_ndimensions([[[[[1, 2]]]]]))
        self.assertTrue(
            6 == self.kim_property.get_optional_key_source_value_ndimensions([[[[[[1, 2]]]]]]))

        self.assertTrue(
            2 == self.kim_property.get_optional_key_source_value_ndimensions([[0.0, 0.0], [1.0, 2.0]]))
        self.assertTrue(
            2 == self.kim_property.get_optional_key_source_value_ndimensions([[0., 0., 0.],
                                                                              [5., 5., 0.],
                                                                              [5., 0., 5.],
                                                                              [0., 5., 0.]]))

    def test_check_instance_optional_key_standard_pairs_format(self):
        """Test the standard key-map pairs correctness."""
        # input is not a dict
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          [], None)

        # "source-value" is not available
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-unit": "angstrom", "digits": 5}, None)

        # input pm is not a dict
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-value": [3.9149], "source-unit": "angstrom", "digits": 5}, [])

        # "extent" specifies single item
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-value": [3.9149, 3.149], "source-unit": "angstrom", "digits": 5}, {"type": "float", "has-unit": True, "extent": [], "required": True})

        # "extent" dimension does not match with "source-unit" dimension
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-value": [3.9149], "digits": 5}, {"type": "float", "has-unit": True, "extent": [2], "required": True})

        # "source-unit" is required but is not there
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-value": [3.9149, 3.149], "digits": 5}, {"type": "float", "has-unit": True, "extent": [2], "required": True})

        # Fail for a wrong key in standard key-value pairs
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-value": [3.9149], "unknown": 5}, None)

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_standard_pairs_format,
                          {"source-value": [3.9149], "source-unit": "angstrom", "unknown": 5}, None)

    def test_check_instance_optional_key_map(self):
        """Test the inctances optional fields key-map pairs correctness."""
        # the key format is not correct
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_map,
                          "A", {"source-unit": "angstrom", "digits": 5})

    def test_check_instance_optional_key_marked_required_are_present(self):
        """Test the inctances optional presence of the keys marked as required."""
        import kim_edn
        pi = {"property-id": "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal", "instance-id": 1}
        pd = kim_edn.load(
            join("tests", "fixtures", "cohesive-energy-relation-cubic-crystal.edn"))

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_instance_optional_key_marked_required_are_present,
                          pi, pd)

    def test_check_property_instances(self):
        """Test property instances format."""
        # the input is None
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          None, None)

        pi = {"property-id": "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal", "instance-id": 1}

        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_instances,
                          pi, fp=None, fp_path=join("tests", "fixtures", "cohesive-energy-relation-cubic-crystal.edn"))

        pd = {"property-id": "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass",
              "property-title": "Atomic mass",
              "property-description": "The atomic mass of the element."}

        # the property-id is different
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_instances,
                          pi, pd)

        # Fails if the path KIM properties is not absolute
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_instances,
                          pi, fp=None, fp_path="cohesive-energy-relation-cubic-crystal.edn")

        # Fails if wrong KIM properties object
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_instances,
                          pi, fp=None, fp_path=[])

        pd = {"property-id": "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal",
              "property-title": "Cohesive energy versus lattice constant relation for a cubic crystal",
              "property-description": "Cohesive energy versus lattice constant relation for a cubic crystal at zero absolute temperature."}

        # Fails if both fp and fpath exists
        self.assertRaises(self.KIMPropertyError, self.kim_property.check_property_instances,
                          pi, fp=pd, fp_path="cohesive-energy-relation-cubic-crystal.edn")


property_instance_names = [
    "RD_000018659700_000_data.edn",
    "RD_999984936526_000_data.edn",
]


class TestPropertyInstance:
    """Test property instance utility module."""

    def test_property(self):
        """Check the property instance."""
        kim_properties = self.kim_property.get_properties()

        for pi in property_instance_names:
            fi = join("tests", "fixtures", pi)

            self.assertTrue(isfile(fi))

            self.kim_property.check_property_instances(
                fi, fp_path=kim_properties)

    def test_invalid_instance(self):
        """Check failing the invalid property instance."""
        pi_str = self.kim_property.kim_property_create(1, 'atomic-mass')
        pi = kim_edn.loads(pi_str)[0]

        kim_properties = self.kim_property.get_properties()

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          fi=pi, fp_path=kim_properties)

        pd = kim_properties[pi["property-id"]]
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          fi=pi, fp=pd)

        pi = {"property-id": "tag:tadmor@noreply.openkim.org,2017-02-01:property/verification-check",
              "instance-id": 1}
        pd = kim_properties[pi["property-id"]]

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          fi=pi, fp=pd)

        pi = {
            "property-id": "tag:tadmor@noreply.openkim.org,2017-02-01:property/verification-check",
            "instance-id": 1,
            "vc-name": {
                "source-value": "vc-periodicity-support"
            },
            "vc-description": {
                "source-value": "..."
            },
            "vc-category": {
                "source-value": "mandatory"
            },
            "vc-grade-basis": {
                "source-value": "passfail"
            },
            "vc-grade": {
                "source-value": "P",
                "source-unit": "ATTENTION: Key 'vc-grade' is not supposed to have any units"
            }
        }

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          fi=pi, fp=pd)

        pi["vc-grade"] = {
            "source-value": "P"
        }

        pi["vc-files"] = {
            "source-value": "ATTN: This is supposed to be an array but it's not"
        }

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          fi=pi, fp=pd)

        del pi["vc-files"]

        pi["vc-grade"] = {
            "source-value": ["P"]
        }

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.check_property_instances,
                          fi=pi, fp=pd)


class TestPyTestPropertyInstanceModuleComponents(TestPropertyInstanceModuleComponents, PyTest):
    pass


class TestPyTestPropertyInstance(TestPropertyInstance, PyTest):
    pass
