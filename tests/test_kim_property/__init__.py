import doctest
import unittest

try:
    import kim_property
except:
    raise Exception('Failed to import `kim_property` utility module')


class PyTest(unittest.TestCase):
    """Make a basic py test class.

    The basic py test class will be used by the other tests.

    """

    KIMPropertyError = staticmethod(kim_property.KIMPropertyError)
    kim_property = staticmethod(kim_property)
