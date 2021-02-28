"""Dump module."""

from os.path import isabs

import kim_edn

from .err import KIMPropertyError
from .instance import check_property_instances
from .create import get_properties

__all__ = [
    "kim_property_dump",
]


def kim_property_dump(property_instances,
                      fp, *,
                      fp_path=None,
                      cls=None,
                      indent=4,
                      default=None,
                      sort_keys=False):
    """Serialize ``property_instances`` object.

    Arguments:
        property_instances {string} -- A string containing the serialized
        KIM-EDN formatted property instances.

        fp {a ``.write()``-supporting file-like object or a name string to
        open a file} -- Serialize ``property_instances`` as a KIM-EDN
        formatted stream to ``fp``

    Keyword Arguments:
        fp_path should be an absolute path (or a valid relative path)
        to the KIM property definition folder. (default: None)

        To use a custom ``KIMEDNEncoder`` subclass (e.g. one that overrides
        the ``.default()`` method to serialize additional types), specify it
        with the ``cls`` kwarg; otherwise ``KIMEDNEncoder`` is used.

        If ``indent`` is a non-negative integer, then EDN array elements and
        object members will be pretty-printed with that indent level. An
        indent level of 0 will only insert newlines. (default 4)

        ``default(obj)`` is a function that should return a serializable
        version of obj or raise TypeError. The default simply raises
        TypeError.

        If *sort_keys* is true (default: ``False``), then the output of
        dictionaries will be sorted by key.

    """
    if property_instances is None or \
            property_instances in ('None', '', '[]'):
        msg = 'there is no property instance to dump it.'
        raise KIMPropertyError(msg)

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    if fp_path is not None and isabs(fp_path):
        # Check the property instances
        check_property_instances(
            kim_property_instances, fp_path=fp_path)
    else:
        kim_properties = get_properties()
        check_property_instances(
            kim_property_instances, fp_path=kim_properties)

    if len(kim_property_instances) == 1:
        kim_edn.dump(kim_property_instances[0], fp, cls=cls,
                     indent=indent, default=default, sort_keys=sort_keys)
    else:
        kim_edn.dump(kim_property_instances, fp, cls=cls,
                     indent=indent, default=default, sort_keys=sort_keys)
