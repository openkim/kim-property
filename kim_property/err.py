"""Error module."""


__all__ = [
    "KIMPropertyError",
]


class KIMPropertyError(Exception):
    """Raise an exception.

    It raises an exception when receives an error message.

    msg {string} -- The error message

    """

    def __init__(self, msg):
        """Constuctor."""
        Exception.__init__(self, '\nERROR: ' + msg)
        self.msg = '\nERROR: ' + msg

    def __reduce__(self):
        """Efficient pickling."""
        return self.__class__, (self.msg)

    def __str__(self):
        """Message string representation."""
        return self.msg
