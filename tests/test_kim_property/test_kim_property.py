from io import StringIO

import kim_edn

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

        # Fails when the instance id is not an integer equal to or greater than 1
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          - 1, 'cohesive-energy-relation-cubic-crystal')

        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          0, 'cohesive-energy-relation-cubic-crystal')

        # Fails when property-name is not an string
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          10, 1)

        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          10, ['cohesive-energy-relation-cubic-crystal'])

        # Fails when property-name is not a valid KIM property name.
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          10, 'new-name')

        str_obj2 = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1} {"property-id" "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass" "instance-id" 2}]'

        # Create the property instance with the property name to the already created instance
        str3 = self.kim_property.kim_property_create(
            2, 'atomic-mass', str1)

        self.assertTrue(str3 == str_obj2)

        # It will fail if the property instance already exists
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          1, 'atomic-mass', str1)

    def test_create_sorted(self):
        """Test create functionality and sorting based on instance-id."""
        str1 = self.kim_property.kim_property_create(2, 'atomic-mass')

        str1 = self.kim_property.kim_property_modify(str1, 2, "key", "species", "source-value", "Ar",
                                                     "key", "mass", "source-value", 39.948, "source-unit", "grams/mole")

        str1 = self.kim_property.kim_property_create(
            5, "cohesive-energy-lattice-invariant-shear-unrelaxed-path-cubic-crystal", str1)

        str1 = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal', str1)

        kim_obj = kim_edn.load(str1)

        self.assertTrue(kim_obj[0]["instance-id"] == 1)
        self.assertTrue(kim_obj[1]["instance-id"] == 2)
        self.assertTrue(kim_obj[2]["instance-id"] == 5)

    def test_destroy(self):
        """Test the destroy functionality."""
        str_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'

        # Destroy the property instance
        str1 = self.kim_property.kim_property_destroy(str_obj, 1)

        self.assertTrue(str1 == '[]')

        # Fails when the instance id is not an integer
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_destroy,
                          str_obj, 1.0)

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
        # Fails when the input is none or not created
        for str_obj in [None, '', 'None', '[]']:
            self.assertRaises(self.KIMPropertyError,
                              self.kim_property.kim_property_modify, str_obj, 1)

        # Fails when there is a different instance id
        str_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal" "instance-id" 1}]'
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify, str_obj, 2)

        # Fails when not having the instance id
        str_obj = '[{"property-id" "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"}]'
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify, str_obj, 1)

        # Fails when not having the property id
        str_obj = '[{"instance-id" 1}]'
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify, str_obj, 1)

        # Create the property instance with the property name
        str_obj = self.kim_property.kim_property_create(
            1, 'cohesive-energy-relation-cubic-crystal')

        # Fails when the instance id is not an integer
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify, str_obj, 1.0)

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

        # Test for scalar values
        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "space-group",
            "source-value", "Immm")

        kim_obj = kim_edn.load(str_obj)[0]

        self.assertTrue(kim_obj["space-group"]["source-value"] == "Immm")

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 1,
            "key", "space-group",
            "source-value", "Fm-3m")

        kim_obj = kim_edn.load(str_obj)[0]

        self.assertTrue(kim_obj["space-group"]["source-value"] == "Fm-3m")

        # Fails when new keyword is not in the property definition
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify,
                          str_obj, 1,
                          "key", "a", "source-value", 2.5)

        # Fails when not in the standard key-value pairs
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify,
                          str_obj, 1,
                          "key", "basis-atom-coordinates", "source-unknown", 2.5)

        # Fails when not enough input
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify,
                          str_obj, 1,
                          "key", "basis-atom-coordinates", "source-value", 3)

        msg = 'there is not enough input arguments '
        msg += 'to use.\nProcessing the {"basis-atom-coordinates"}:'
        msg += '{"source-value"} input arguments failed.\nThe second '
        msg += 'index is missing from the input arguments.'

        self.assertRaisesRegex(self.KIMPropertyError, msg,
                               self.kim_property.kim_property_modify,
                               str_obj, 1,
                               "key", "basis-atom-coordinates", "source-value", 3)

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify,
                          str_obj, 1,
                          "key", "basis-atom-coordinates", "source-value", 3, 3)

        msg = 'there is not enough input arguments '
        msg += 'to use.\nProcessing the {"basis-atom-coordinates"}:'
        msg += '{"source-value"} input arguments failed.\n'
        msg += 'At least we need one further input.'

        self.assertRaisesRegex(self.KIMPropertyError, msg,
                               self.kim_property.kim_property_modify,
                               str_obj, 1,
                               "key", "basis-atom-coordinates", "source-value", 3, 3)

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify,
                          str_obj, 1,
                          "key", "basis-atom-coordinates", "source-value", 3, 4)

        msg = 'this dimension has a fixed length = 3, while, '
        msg += 'wrong index = 4 is requested.\nProcessing the '
        msg += '{"basis-atom-coordinates"}:{"source-value"} input arguments,'
        msg += ' wrong index at the second dimension is requested.'

        self.assertRaisesRegex(self.KIMPropertyError, msg,
                               self.kim_property.kim_property_modify,
                               str_obj, 1,
                               "key", "basis-atom-coordinates", "source-value", 3, 4)

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

        # Fail when there is no property instance to remove the content.
        for str_obj1 in [None, 'None', '', '[]']:
            self.assertRaises(self.KIMPropertyError,
                              self.kim_property.kim_property_remove,
                              str_obj1, 1, "key", "a")

        # Fails when the "instance_id" is not an `int`.
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, 1.0, "key", "a")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, "1", "key", "a")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, [1], "key", "a")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, {1}, "key", "a")

        # Fails when the requested instance id doesn\'t match any
        # of the property instances ids.
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, 10, "key", "a")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, 2, "key", "a")

        # Fails when the key doesn\'t exist in the property instance.
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, 1, "key", "new_item")

        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_remove,
                          str_obj, 1, "key", "aa")

        # Removing the whole key
        str_obj1 = self.kim_property.kim_property_remove(
            str_obj, 1, "key", "a")
        kim_obj1 = kim_edn.load(str_obj1)[0]

        self.assertFalse("a" in kim_obj1)
        del str_obj1
        del kim_obj1

        # Removing the internal key from the key-map pairs for key
        str_obj2 = self.kim_property.kim_property_remove(
            str_obj, 1, "key", "a", "source-value")
        kim_obj2 = kim_edn.load(str_obj2)[0]

        self.assertTrue("a" in kim_obj2)
        self.assertFalse("source-value" in kim_obj2["a"])
        del str_obj2
        del kim_obj2

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

        # Test for scalar values
        str_obj4 = self.kim_property.kim_property_modify(
            str_obj3, 1,
            "key", "space-group",
            "source-value", "Immm")

        str_obj4 = self.kim_property.kim_property_modify(
            str_obj4, 1,
            "key", "space-group",
            "source-value", "Fm-3m")

        kim_obj4 = kim_edn.load(str_obj4)[0]

        self.assertTrue(kim_obj4["space-group"]["source-value"] == "Fm-3m")

        str_obj4 = self.kim_property.kim_property_remove(
            str_obj4, 1, "key", "space-group", "source-value")
        kim_obj4 = kim_edn.load(str_obj4)[0]

        self.assertFalse("source-value" in kim_obj4["space-group"])

        str_obj4 = self.kim_property.kim_property_modify(
            str_obj4, 1,
            "key", "space-group",
            "source-value", "Fm-3m")
        kim_obj4 = kim_edn.load(str_obj4)[0]

        self.assertTrue(kim_obj4["space-group"]["source-value"] == "Fm-3m")

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

        # Fail when there is no property instance to dump it.
        for str_obj1 in [None, 'None', '', '[]']:
            self.assertRaises(self.KIMPropertyError,
                              self.kim_property.kim_property_dump,
                              str_obj1, sio)

        self.kim_property.kim_property_dump(str_obj, sio, indent=0)

        self.assertTrue(sio.getvalue() == out_str)

        # Fail to create a file to dump the property
        self.assertRaises(self.KIMPropertyError,
                          self.kim_property.kim_property_modify,
                          str_obj, "output/results.edn")

        str_obj = self.kim_property.kim_property_create(
            2, 'atomic-mass', str_obj)

        str_obj = self.kim_property.kim_property_modify(
            str_obj, 2,
            "key", "species", "source-value", "Al",
            "key", "mass", "source-value", 26.98, "source-unit", "grams/mole")

        self.kim_property.kim_property_dump(str_obj, sio, indent=0)


class TestPyTestPropertyModule(TestPropertyModule, PyTest):
    pass
