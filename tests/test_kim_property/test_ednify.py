from os.path import abspath, join, isdir
from os import rename, makedirs
from shutil import rmtree, copy
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

KIM_PROPERTY_FILES_PATH = join(
    "external", "openkim-properties", "properties")
KIM_PROPERTY_FILES_BACKUP_PATH = KIM_PROPERTY_FILES_PATH + '_'


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

    def test_unednify_kim_properties(self):
        """Test unednifying the KIM properties."""

        # Fails when can't load edn from unicode string
        self.assertRaises(
            kim_edn.decoder.KIMEDNDecodeError,
            unednify_kim_properties,
            'kim_properties.edn',
        )

        sio = StringIO()
        ednify_kim_properties(PROPERTIES, sio)

        # Test the unpickle utility
        _properties, _name_to_id, _id_to_name = unednify_kim_properties(sio.getvalue())

        self.assertTrue(_properties == PROPERTIES)
        self.assertTrue(_name_to_id == NAME_TO_ID)
        self.assertTrue(_id_to_name == ID_TO_NAME)

        sio1 = StringIO()
        # Fails when neither can open nor load the input
        self.assertRaises(
            kim_edn.decoder.KIMEDNDecodeError, unednify_kim_properties, sio1.getvalue()
        )


class TestPyTestEdnify(TestEdnify, PyTest):
    pass


class TestEdnifyFromExternal:
    """Test ednifying from external/openkim-properties/properties"""

    @classmethod
    def setUpClass(cls):
        """
        If KIM_PROPERTY_FILES_PATH exists (i.e. if you're running
        locally and you've checked out the submodule), back it up.
        Create mock directory with known properties.
        """
        if isdir(abspath(KIM_PROPERTY_FILES_PATH)):
            if isdir(abspath(KIM_PROPERTY_FILES_BACKUP_PATH)):
                raise RuntimeError(
                    'Intended property backup path\n"'
                    f'{KIM_PROPERTY_FILES_BACKUP_PATH}'
                    '"\nalready exists, can\'t run test!'
                    )
            rename(
                KIM_PROPERTY_FILES_PATH,
                KIM_PROPERTY_FILES_BACKUP_PATH
                )
        # Place files in correct directories
        dir1 = join(KIM_PROPERTY_FILES_PATH, NAME1, f'{DATE1}-{EMAIL1}')
        makedirs(dir1)
        copy(EDN_FILE1, dir1)
        dir2 = join(KIM_PROPERTY_FILES_PATH, NAME2, f'{DATE2}-{EMAIL2}')
        makedirs(dir2, exist_ok=True)
        copy(EDN_FILE2, dir2)
        # Create an intentionally invalid file in a directory with an older
        # date, to check that only the newest version of the property is read
        dir_invalid = join(KIM_PROPERTY_FILES_PATH, NAME2, f'1111-11-11-{EMAIL2}')
        makedirs(dir_invalid)
        with open(join(dir_invalid, NAME2 + '.edn'), 'w') as f:
            f.write('foo')

    @classmethod
    def tearDownClass(cls):
        """
        Restore KIM_PROPERTY_FILES backup
        """
        # This should have been removed during the test,
        # but in case it failed
        if isdir(abspath(KIM_PROPERTY_FILES_PATH)):
            rmtree(KIM_PROPERTY_FILES_PATH)
        if isdir(abspath(KIM_PROPERTY_FILES_BACKUP_PATH)):
            rename(
                KIM_PROPERTY_FILES_BACKUP_PATH,
                KIM_PROPERTY_FILES_PATH
                )

    def test_ednify_kim_properties(self):
        sio = StringIO()
        # ednify with no properties argument to read from
        # KIM_PROPERTY_FILES_PATH
        ednify_kim_properties(fp=sio)

        _properties, _name_to_id, _id_to_name = kim_edn.loads(sio.getvalue())

        self.assertTrue(_properties == PROPERTIES)
        self.assertTrue(_name_to_id == NAME_TO_ID)
        self.assertTrue(_id_to_name == ID_TO_NAME)

        # Test that it correctly fails to read a missing directory
        rmtree(KIM_PROPERTY_FILES_PATH)
        sio = StringIO()
        self.assertRaises(
            self.KIMPropertyError, ednify_kim_properties, None, sio)

        msg = 'property files can not be found at.*'
        self.assertRaisesRegex(
            self.KIMPropertyError, msg, ednify_kim_properties, None, sio
        )


class TestPyTestEdnifyFromExternal(TestEdnifyFromExternal, PyTest):
    pass
