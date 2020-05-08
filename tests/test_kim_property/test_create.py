import os
from os.path import join, isfile

import kim_edn

from tests.test_kim_property import PyTest


class TestCreateModule:
    """Test kim_property utility module create component."""

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

        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          "1", 'cohesive-energy-relation-cubic-crystal')

        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          False, 'cohesive-energy-relation-cubic-crystal')

        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          [1], 'cohesive-energy-relation-cubic-crystal')

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

    def test_create_from_a_file(self):
        """Test the create functionality for a new file as input."""
        # Correct object
        str_obj = '[{"property-id" "tag:yafshar@noreply.openkim.org,2020-03-02:property/atomic-mass-test" "instance-id" 1}]'

        # Create the property instance from a property file
        edn_file = join("tests", "fixtures", "new-property.edn")
        self.assertTrue(isfile(edn_file))

        str1 = self.kim_property.kim_property_create(
            1, edn_file)

        self.assertTrue(str1 == str_obj)

        kim_properties = self.kim_property.get_properties()
        self.assertTrue(
            "tag:yafshar@noreply.openkim.org,2020-03-02:property/atomic-mass-test" in kim_properties)

        # Fails if the property instance already exists in OpenKIM
        self.assertRaises(self.KIMPropertyError, self.kim_property.kim_property_create,
                          1, join("tests", "fixtures", "atomic-mass.edn"))



class TestPyTestCreateModule(TestCreateModule, PyTest):
    pass
