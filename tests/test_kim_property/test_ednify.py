from os.path import abspath, join, isfile, isdir
from os import removedirs
from io import BytesIO, StringIO

import kim_edn

from kim_property.ednify import ednify_kim_properties, unednify_kim_properties
from tests.test_kim_property import PyTest

NAME1 = 'atomic-mass'
EMAIL1 = 'brunnels@noreply.openkim.org'
DATE1 = '2016-05-11'
ID1 = f'tag:{EMAIL1},{DATE1}:property/{NAME1}'

NAME2 = 'cohesive-energy-relation-cubic-crystal'
EMAIL2 = 'staff@noreply.openkim.org'
DATE2 = '2014-04-15'
ID2 = f'tag:{EMAIL2},{DATE2}:property/{NAME2}'

# Property definition edn file
EDN_FILE1 = join('tests', 'fixtures', f'{NAME1}.edn')

EDN_FILE2 = join(
    'tests', 'fixtures', f'{NAME2}.edn'
)

PROPERTIES = {
    ID1:
        kim_edn.load(EDN_FILE1),
    ID2:
        kim_edn.load(EDN_FILE2),
}

NAME_TO_ID = {
    NAME1:
        ID1,
    NAME2:
        ID2,
}

ID_TO_NAME = {
    ID1:
        NAME1,
    ID2:
        NAME2,
}


class TestEdnify:
    """Test KIM properties ednify module."""

    def test_ednify_kim_properties(self):
        """Test ednifying the KIM properties."""

        sio = StringIO()
        ednify_kim_properties(PROPERTIES, sio)

        _properties, _name_to_id, _id_to_name = kim_edn.loads(sio.getvalue())

        self.assertTrue(_properties == PROPERTIES)
        self.assertTrue(_name_to_id == NAME_TO_ID)
        self.assertTrue(_id_to_name == ID_TO_NAME)

        bio = BytesIO()
        self.assertRaises(TypeError, ednify_kim_properties, PROPERTIES, bio)

        msg = 'a bytes-like object is required.*'
        self.assertRaisesRegex(
            TypeError, msg, ednify_kim_properties, PROPERTIES, bio)

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
