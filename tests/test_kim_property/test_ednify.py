from os.path import abspath, join, isfile, isdir
from io import BytesIO, StringIO

import kim_edn

from kim_property.ednify import ednify_kim_properties, unednify_kim_properties
from tests.test_kim_property import PyTest


class TestEdnify:
    """Test KIM properties ednify module."""

    def test_ednify_kim_properties(self):
        """Test ednifying the KIM properties."""
        # Property definition edn file
        edn_file1 = join('tests', 'fixtures', 'atomic-mass.edn')
        self.assertTrue(isfile(edn_file1))

        edn_file2 = join(
            'tests', 'fixtures', 'cohesive-energy-relation-cubic-crystal.edn'
        )
        self.assertTrue(isfile(edn_file2))

        properties = {
            'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass':
                kim_edn.load(edn_file1),
            'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal':
                kim_edn.load(edn_file2),
        }

        name_to_id = {
            'atomic-mass':
                'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass',
            'cohesive-energy-relation-cubic-crystal':
                'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal',
        }

        id_to_name = {
            'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass':
                'atomic-mass',
            'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal':
                'cohesive-energy-relation-cubic-crystal',
        }

        sio = StringIO()
        ednify_kim_properties(properties, sio)

        _properties, _name_to_id, _id_to_name = kim_edn.loads(sio.getvalue())

        self.assertTrue(_properties == properties)
        self.assertTrue(_name_to_id == name_to_id)
        self.assertTrue(_id_to_name == id_to_name)

        bio = BytesIO()
        self.assertRaises(TypeError, ednify_kim_properties, properties, bio)

        msg = 'a bytes-like object is required.*'
        self.assertRaisesRegex(
            TypeError, msg, ednify_kim_properties, properties, bio)

        kim_property_files_path = join(
            "external", "openkim-properties", "properties")

        if not isdir(abspath(kim_property_files_path)):
            sio = StringIO()
            self.assertRaises(
                self.KIMPropertyError, ednify_kim_properties, None, sio)

            msg = 'property files can not be found at.*'
            self.assertRaisesRegex(
                self.KIMPropertyError, msg, ednify_kim_properties, None, sio
            )

    def test_unednify_kim_properties(self):
        """Test unednifying the KIM properties."""

        # Fails when can't load edn from unicode string
        self.assertRaises(
            kim_edn.decoder.KIMEDNDecodeError,
            unednify_kim_properties,
            'kim_properties.edn',
        )

        # Property definition edn file
        edn_file1 = join('tests', 'fixtures', 'atomic-mass.edn')
        self.assertTrue(isfile(edn_file1))

        edn_file2 = join(
            'tests', 'fixtures', 'cohesive-energy-relation-cubic-crystal.edn'
        )
        self.assertTrue(isfile(edn_file2))

        properties = {
            'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass':
                kim_edn.load(edn_file1),
            'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal':
                kim_edn.load(edn_file2),
        }

        sio = StringIO()
        ednify_kim_properties(properties, sio)

        # Test the unpickle utility
        _properties, _name_to_id, _id_to_name = unednify_kim_properties(sio.getvalue())

        name_to_id = {
            'atomic-mass':
                'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass',
            'cohesive-energy-relation-cubic-crystal':
                'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal',
        }

        id_to_name = {
            'tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass':
                'atomic-mass',
            'tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal':
                'cohesive-energy-relation-cubic-crystal',
        }

        self.assertTrue(_properties == properties)
        self.assertTrue(_name_to_id == name_to_id)
        self.assertTrue(_id_to_name == id_to_name)

        sio1 = StringIO()
        # Fails when neither can open nor load the input
        self.assertRaises(
            kim_edn.decoder.KIMEDNDecodeError, unednify_kim_properties, sio1.getvalue()
        )


class TestPyTestEdnify(TestEdnify, PyTest):
    pass
