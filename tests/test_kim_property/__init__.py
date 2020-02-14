import os
from os.path import isdir, abspath
import sys

import doctest
import unittest

from test import support

if isdir(abspath('./utils/')):
    sys.path.insert(1, abspath('./utils/'))
elif isdir(abspath('../utils/')):
    sys.path.insert(1, abspath('../utils/'))
elif isdir(abspath('../../utils/')):
    sys.path.insert(1, abspath('../../utils/'))

try:
    import kim_edn
except:
    raise Exception('Failed to import `kim_edn` utility module')

try:
    import kim_property
except:
    raise Exception('Failed to import property `kim_property` utility module')

class PyTest(unittest.TestCase):
    """Make a basic py test class.

    The basic py test class will be used by the other tests.

    """

    loads = staticmethod(kim_edn.loads)
    dumps = staticmethod(kim_edn.dumps)
    KIMEDNDecodeError = staticmethod(kim_edn.KIMEDNDecodeError)

    kim_edn = staticmethod(kim_edn)
    KIMPropertyError = staticmethod(kim_property.KIMPropertyError)
    kim_property = staticmethod(kim_property)
