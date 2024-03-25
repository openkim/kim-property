"""Error module."""

import inspect

__all__ = [
    "KIMPropertyError",
]


class KIMPropertyError(Exception):
    """Raise an exception.

    It raises an exception when receives an error message.

    msg {string} -- The error message

    """

    def __init__(self, msg: str):
        """Constuctor."""
        _msg = '\nERROR(@' + \
            inspect.currentframe().f_back.f_code.co_name + '): ' + msg
        Exception.__init__(self, _msg)
        self.msg = _msg

    def __reduce__(self):
        """Efficient pickling."""
        return self.__class__, (self.msg, )

    def __str__(self):
        """Message string representation."""
        return self.msg
