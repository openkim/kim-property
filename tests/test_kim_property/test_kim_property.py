from io import StringIO

try:
    import kim_edn
except:
    raise Exception('Failed to import `kim_edn` utility module')

from tests.test_kim_property import PyTest


class TestPropertyModule:
    """Test kim_property utility module components."""

    def test_create(self):
        """Test the create functionality."""
        # Correct object
        str_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

        # Create the property instance with the property name
        str1 = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal')

        self.assertTrue(str1 == str_obj)

        # Create the property instance with the full property name and tag
        str2 = self.kim_property.kim_property_create(
            1, 'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal')

        self.assertTrue(str2 == str_obj)

        # Fails when theinstance id is not an integer equal to or greater than 1
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          - 1, 'cohesive-energy-relation-cubic-crystal')

        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          0, 'cohesive-energy-relation-cubic-crystal')

        str_obj2 = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

        # Create the property instance with the property name to the already created instance
        str3 = self.kim_property.kim_property_create(
            2, 'atomic-mass', str1)

        self.assertTrue(str3 == str_obj2)

        # It will fail if the property instance already exists
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          1, 'atomic-mass', str1)

    def test_destroy(self):
        """Test the destroy functionality."""
        str_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

        # Destroy the property instance
        str1 = self.kim_property.kim_property_destroy(str_obj, 1)

        self.assertTrue(str1 == '[]')

        str_obj2 = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

        # Destroy one of the property instance
        str2 = self.kim_property.kim_property_destroy(str_obj2, 2)

        self.assertTrue(str2 == str_obj)

        # Test the empty string
        for str_obj3 in ['', 'None', '[]']:
            str3 = self.kim_property.kim_property_destroy(str_obj3, 1)

            self.assertTrue(str3 == '[]')

    def test_modify(self):
        """Test the modify functionality."""
        # Create the property instance with the property name
        str_obj = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal')

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
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

        kim_obj = kim_edn.load(str_obj)[0]

        Property_Instance = '{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1 "short-name" {"source-value" ["fcc"]} "species" {"source-value" ["Al" "Al" "Al" "Al"]} "a" {"source-value" [3.9149 4.0 4.032 4.0817 4.1602] "source-unit" "angstrom" "digits" 5} "basis-atom-coordinates" {"source-value" [[0.0 0.0 0.0] [0.5 0.5 0.0] [0.5 0.0 0.5] [0.0 0.5 0.5]]} "cohesive-potential-energy" {"source-value" [3.324 3.3576 3.36 3.355 3.326] "source-std-uncert-value" [0.002 0.0001 1e-05 0.0012 0.00015] "source-unit" "eV" "digits" 5}}'

        self.assertTrue(Property_Instance == kim_edn.dumps(kim_obj))

        # Create the property instance with the property name
        str_obj = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal')

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "short-name",
            "source-value", "1", "fcc",
            "key", "species",
            "source-value", "1:4", "Al", "Al", "Al", "Al")

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "a",
            "source-value", "1:5", "3.9149", "4.0000", "4.032", "4.0817", "4.1602")

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "a",
            "source-unit", "angstrom", "digits", "5")

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "basis-atom-coordinates",
            "source-value", "4", "2:3", "0.5", "0.5",
            "key", "basis-atom-coordinates",
            "source-value", "3", "3", "0.5",
            "key", "basis-atom-coordinates",
            "source-value", "2", "1:2", "0.5", "0.5")

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "basis-atom-coordinates",
            "source-value", "3", "1", "0.5")

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "cohesive-potential-energy",
            "source-value", "1:5", "3.324", "3.3576", "3.3600", "3.3550", "3.3260",
            "source-std-uncert-value", "1:5", "0.002", "0.0001", "0.00001", "0.0012", "0.00015",
            "source-unit", "eV",
            "digits", "5")

        kim_obj = kim_edn.load(str_obj)[0]

        self.assertTrue(Property_Instance == kim_edn.dumps(kim_obj))

    def test_remove(self):
        """Test the remove functionality."""
        # Create the property instance with the property name
        str_obj = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal')

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
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

        kim_obj = kim_edn.load(str_obj)[0]

        self.assertTrue("a" in kim_obj)
        self.assertTrue("source-value" in kim_obj["a"])
        self.assertTrue("cohesive-potential-energy" in kim_obj)
        self.assertTrue("basis-atom-coordinates" in kim_obj)

        # Removing the whole key
        str_obj1 = self.kim_property.kim_property_remove(
            str_obj, 1, "key", "a")
        kim_obj1 = kim_edn.load(str_obj1)[0]

        self.assertFalse("a" in kim_obj1)
        del(str_obj1)
        del(kim_obj1)

        # Removing the internal key from the key-map pairs for key
        str_obj2 = self.kim_property.kim_property_remove(
            str_obj, 1, "key", "a", "source-value")
        kim_obj2 = kim_edn.load(str_obj2)[0]

        self.assertTrue("a" in kim_obj2)
        self.assertFalse("source-value" in kim_obj2["a"])
        del(str_obj2)
        del(kim_obj2)

        # Removing multiple keys
        str_obj3 = self.kim_property.kim_property_remove(
            str_obj, 1, "key", "cohesive-potential-energy", "key", "basis-atom-coordinates")
        kim_obj3 = kim_edn.load(str_obj3)[0]

        self.assertFalse("cohesive-potential-energy" in kim_obj3)
        self.assertFalse("basis-atom-coordinates" in kim_obj3)

        str_obj3 = self.kim_property.kim_property_remove(
            str_obj3, 1, "key", "a", "source-unit")
        kim_obj3 = kim_edn.load(str_obj3)[0]

        self.assertTrue("a" in kim_obj3)
        self.assertTrue("source-value" in kim_obj3["a"])
        self.assertFalse("source-unit" in kim_obj3["a"])

    def test_dump(self):
        """Test the dump functionality."""
        # Create the property instance with the property name
        str_obj = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal')

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
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

        kim_obj = kim_edn.load(str_obj)[0]
        out_str = kim_edn.dumps(kim_obj, indent=0) + '\n'

        sio = StringIO()
        self.kim_property.kim_property_dump(str_obj, sio, indent=0)

        self.assertTrue(sio.getvalue() == out_str)


class TestPyTestPropertyModule(TestPropertyModule, PyTest):
    pass
