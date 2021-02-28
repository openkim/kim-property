"""Remove module."""

import kim_edn

from .err import KIMPropertyError

__all__ = [
    "kim_property_remove",
]


def kim_property_remove(property_instances, instance_id, *argv):
    """Remove or delete a key from the property instance.

    Arguments:
        property_instances {string} -- A string containing the serialized
            KIM-EDN formatted property instances.
        instance_id {int} -- A positive integer identifying the property
            instance.

    Returns:
        string -- serialized KIM-EDN formatted property instances.

    """
    if property_instances is None or property_instances in ('None', '', '[]'):
        msg = 'there is no property instance to remove the content.'
        raise KIMPropertyError(msg)

    if not isinstance(instance_id, int):
        msg = 'the "instance_id" is not an `int`.'
        raise KIMPropertyError(msg)

    # Deserialize the KIM property instances.
    kim_property_instances = kim_edn.loads(property_instances)

    a_property_instance = None

    for p in kim_property_instances:
        if p["instance-id"] == instance_id:
            a_property_instance = p
            break

    if a_property_instance is None:
        msg = 'the requested instance id :\n{}\n'.format(instance_id)
        msg += 'doesn\'t match any of the property instances ids.'
        raise KIMPropertyError(msg)

    # Number of arguments
    n_arguments = len(argv)

    # key keyword
    k_keyword = False

    # new keyword
    new_keyword = None
    new_keyword_map = {}

    i = 0
    while i < n_arguments:
        try:
            arg = argv[i]
        except IndexError:
            msg = 'unexpected index exception happened.'
            raise KIMPropertyError(msg)

        if arg == 'key':
            k_keyword = True
            i += 1
            continue

        if k_keyword:
            k_keyword = False

            # new keyword
            new_keyword = arg
            if new_keyword not in a_property_instance:
                msg = 'the key {} '.format(new_keyword)
                msg += 'doesn\'t exist in the property instance.'
                raise KIMPropertyError(msg)

            # Remove the whole key if it is requested
            if i + 1 < n_arguments:
                try:
                    arg = argv[i + 1]
                except IndexError:
                    msg = 'unexpected index exception happened.'
                    raise KIMPropertyError(msg)

                if arg == 'key':
                    del a_property_instance[new_keyword]
                    i += 1
                    continue
            # There is no more argument delete a key and stop
            else:
                del a_property_instance[new_keyword]
                break

            new_keyword_map = a_property_instance[new_keyword]

            i += 1
            continue

        if arg in new_keyword_map:
            del new_keyword_map[arg]

        i += 1
        continue

    return kim_edn.dumps(kim_property_instances)
