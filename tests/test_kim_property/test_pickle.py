from os.path import join, isfile
from io import BytesIO, StringIO
import pickle

import kim_edn

from kim_property.pickle import \
    pickle_kim_properties, \
    unpickle_kim_properties
from tests.test_kim_property import PyTest


class TestPickle:
    """Test KIM properties pickle module."""

    def test_pickle_kim_properties(self):
        """Test pickling the KIM properties."""
        # Property definition edn file
        edn_file1 = join("tests", "fixtures", "atomic-mass.edn")
        self.assertTrue(isfile(edn_file1))

        edn_file2 = join("tests", "fixtures",
                         "cohesive-energy-relation-cubic-crystal.edn")
        self.assertTrue(isfile(edn_file2))

        properties = {"tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass": kim_edn.load(edn_file1),
                      "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal": kim_edn.load(edn_file2)}

        name_to_id = {"atomic-mass": "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass",
                      "cohesive-energy-relation-cubic-crystal": "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"}

        id_to_name = {"tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass": "atomic-mass",
                      "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal": "cohesive-energy-relation-cubic-crystal"}

        bio = BytesIO()
        pickle_kim_properties(properties, bio)

        _properties, _name_to_id, _id_to_name = pickle.loads(bio.getvalue())

        self.assertTrue(_properties == properties)
        self.assertTrue(_name_to_id == name_to_id)
        self.assertTrue(_id_to_name == id_to_name)

        sio = StringIO()
        self.assertRaises(self.KIMPropertyError, pickle_kim_properties,
                          properties, sio)

    def test_pickle_err_class(self):
        """Test pickling the KIM Error module."""
        obj = pickle.dumps(self.KIMPropertyError(
            "Test pickling the KIM Error module."))
        self.assertTrue(obj != None)

    def test_unpickle_kim_properties(self):
        """Test unpickling the KIM properties."""

        # Fails when can't load pickle from unicode string
        self.assertRaises(self.KIMPropertyError,
                          unpickle_kim_properties,
                          'kim_properties.pickle')

        # Property definition edn file
        edn_file1 = join("tests", "fixtures", "atomic-mass.edn")
        self.assertTrue(isfile(edn_file1))

        edn_file2 = join("tests", "fixtures",
                         "cohesive-energy-relation-cubic-crystal.edn")
        self.assertTrue(isfile(edn_file2))

        properties = {"tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass": kim_edn.load(edn_file1),
                      "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal": kim_edn.load(edn_file2)}

        bio = BytesIO()
        pickle_kim_properties(properties, bio)

        # Test the unpickle utility
        _properties, _name_to_id, _id_to_name = unpickle_kim_properties(
            bio.getvalue())

        name_to_id = {"atomic-mass": "tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass",
                      "cohesive-energy-relation-cubic-crystal": "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal"}

        id_to_name = {"tag:brunnels@noreply.openkim.org,2016-05-11:property/atomic-mass": "atomic-mass",
                      "tag:staff@noreply.openkim.org,2014-04-15:property/cohesive-energy-relation-cubic-crystal": "cohesive-energy-relation-cubic-crystal"}

        self.assertTrue(_properties == properties)
        self.assertTrue(_name_to_id == name_to_id)
        self.assertTrue(_id_to_name == id_to_name)

        bio1 = BytesIO()
        # Fails when neither can open nor load the input
        self.assertRaises(self.KIMPropertyError,
                          unpickle_kim_properties,
                          bio1.getvalue())


class TestPyTestPickle(TestPickle, PyTest):
    pass
