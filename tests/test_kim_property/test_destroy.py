from os.path import join, isfile

from tests.test_kim_property import PyTest


class TestDestroyModule:
    """Test kim_property utility module destroy component."""

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

    def test_destroy_new_from_a_file(self):
        """Test the destroy functionality for a new property created from a file as input."""
        # Correct object
        str_obj = '[{"property-id" "tag:yafshar@noreply.openkim.org,2020-03-02:property/atomic-mass-test" "instance-id" 1}]'

        # Make sure that the newly created proprty has been removed
        property_id = "tag:yafshar@noreply.openkim.org,2020-03-02:property/atomic-mass-test"
        self.kim_property.unset_property_id(property_id)

        # Create the property instance from a property file
        edn_file = join("tests", "fixtures", "new-property.edn")
        self.assertTrue(isfile(edn_file))

        str1 = self.kim_property.kim_property_create(
            1, edn_file)

        self.assertTrue(str1 == str_obj)

        self.kim_property.kim_property_destroy(str1, 1)

        kim_properties = self.kim_property.get_properties()
        self.assertTrue(property_id not in kim_properties)


class TestPyTestDestroyModule(TestDestroyModule, PyTest):
    pass
