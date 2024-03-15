"""Numerics functionality for kim utility module."""

from .err import KIMPropertyError

__all__ = [
    "shape",
    "size",
    "is_array_uniform",
    "create_full_array",
    "extend_full_array",
]


def is_array_first_dimension_uniform(arr):
    """Is the input array uniform along the first dimension.

    Arguments:
        arr {ndarray} -- Input array.

    Returns:
        bool -- true the input array is uniform along the first dimension.

    """
    if type(arr) in (list, tuple):
        if len(arr) == 0:
            return True
        u = True
        s = type(arr[0])
        for i in range(1, len(arr)):
            u = u and isinstance(arr[i], s)
        if not u:
            return False
        if type(arr[0]) in (list, tuple):
            s = len(arr[0])
            for i in range(1, len(arr)):
                u = u and s == len(arr[i])
            if not u:
                return False
        return True
    return True


def shape(arr):
    """Return the shape of an array.

    Return the shape of an array with the assumption of uniformity along
    all dimensions. Otherwise return the shape of the array till uniformity
    is broken.

    Arguments:
        arr {ndarray} -- Input array.

    Returns:
        list -- shape, the elements of the shape list give the lengths of
            the corresponding array dimensions.

    """
    if not is_array_first_dimension_uniform(arr):
        return [len(arr)]
    if type(arr) in (list, tuple):
        if len(arr) == 0:
            return [0]
        return [len(arr)] + shape(arr[0])
    return []


def size(arr):
    """Return the size of an array.

    Return the size of an array with the assumption of uniformity along
    all dimensions. Otherwise return the size of the array till uniformity
    is broken.

    Arguments:
        arr {ndarray} -- Input array.

    Returns:
        int -- size of the array.

    """
    if not is_array_first_dimension_uniform(arr):
        return len(arr)
    if type(arr) in (list, tuple):
        if len(arr) == 0:
            return 0
        return len(arr) * size(arr[0])
    return 1


def is_array_uniform(arr):
    """Is the input array uniform along all dimensions.

    Check if the input array is uniform along all dimensions.

    Arguments:
        arr {ndarray} -- Input array.

    Returns:
        bool -- true the input array is uniform along all dimensions.

    """
    if type(arr) in (list, tuple):
        if len(arr) == 0:
            return True
        u = True
        s = type(arr[0])
        for i in range(1, len(arr)):
            u = u and isinstance(arr[i], s)
        if not u:
            return False
        if type(arr[0]) in (list, tuple):
            s = len(arr[0])
            for i in range(1, len(arr)):
                u = u and s == len(arr[i])
            if not u:
                return False
        for i in range(len(arr)):
            u = u and is_array_uniform(arr[i])
        return u
    return True


def create_full_array(array_shape, fill_value=None):
    """Return a full array with the given shape and filled with given value.

    Arguments:
        array_shape {list} -- list of ints
        fill_value {scalar} -- Fill value. (default: None)

    Returns:
        ndarray -- array of fill_value with the requested shape filled with
            fill_value

    """
    if isinstance(array_shape, (list, tuple)):
        if array_shape:
            return [create_full_array(array_shape[1:], fill_value)
                    for i in range(array_shape[0])]

        return fill_value

    msg = 'input "array_shape" is not a `list` or `tuple`.'
    raise KIMPropertyError(msg)


def extend_full_array(full_array, array_shape, fill_value=None, _shape=shape):
    """Return a full array with the given shape and filled with given value.

    Return a full array with the given shape initialize with the given value
    and the known values from the old array

    Arguments:
        full_array {ndarray} -- original ndarray to be extended
        array_shape {list} -- list of ints
        fill_value {scalar} -- Fill value. (default: None)

    Returns:
        ndarray -- array of fill_value with the requested shape filled with
            fill_value

    """
    if not isinstance(array_shape, list):
        if not isinstance(array_shape, tuple):
            msg = 'input "array_shape" is not a `list` or `tuple`.'
            raise KIMPropertyError(msg)

    if not is_array_uniform(full_array):
        msg = 'the input array is not uniform along all dimensions.'
        raise KIMPropertyError(msg)

    # Creat a new array
    new_array = create_full_array(array_shape, fill_value)
    new_array_ndims = len(array_shape)

    # old array shape and dimensions
    full_array_shape = _shape(full_array)
    full_array_ndims = len(full_array_shape)

    # Dimensionality check
    if new_array_ndims != full_array_ndims:
        msg = 'the old array has "{}" '.format(full_array_ndims)
        msg += 'dimensions and can not be extended to a new '
        msg += '"{}" dimensional array.'.format(new_array_ndims)
        raise KIMPropertyError(msg)

    # Shape check
    for o, n in zip(full_array_shape, array_shape):
        if o > n:
            msg = 'the old array with the shape of '
            msg += '{} '.format(full_array_shape)
            msg += 'does not fit within the new array with the shape of '
            msg += '{}.'.format(array_shape)
            raise KIMPropertyError(msg)

    if full_array_ndims == 1:
        d0 = full_array_shape[0]
        new_array[0:d0] = full_array[0:d0]
        return new_array

    if full_array_ndims == 2:
        d0, d1 = full_array_shape
        for i in range(d0):
            new_array[i][0:d1] = full_array[i][0:d1]
        return new_array

    if full_array_ndims == 3:
        d0, d1, d2 = full_array_shape
        for i in range(d0):
            for j in range(d1):
                new_array[i][j][0:d2] = full_array[i][j][0:d2]
        return new_array

    if full_array_ndims == 4:
        d0, d1, d2, d3 = full_array_shape
        for i in range(d0):
            for j in range(d1):
                for k in range(d2):
                    new_array[i][j][k][0:d3] = full_array[i][j][k][0:d3]
        return new_array

    if full_array_ndims == 5:
        d0, d1, d2, d3, d4 = full_array_shape
        for i in range(d0):
            for j in range(d1):
                for k in range(d2):
                    for m in range(d3):
                        new_array[i][j][k][m][0:d4] = \
                            full_array[i][j][k][m][0:d4]
        return new_array

    if full_array_ndims == 6:
        d0, d1, d2, d3, d4, d5 = full_array_shape
        for i in range(d0):
            for j in range(d1):
                for k in range(d2):
                    for m in range(d3):
                        for n in range(d4):
                            new_array[i][j][k][m][n][0:d5] = \
                                full_array[i][j][k][m][n][0:d5]
        return new_array

    msg = 'maximum number of 6 dimensions is supported while '
    msg += '{} is requested.'.format(full_array_ndims)
    raise KIMPropertyError(msg)
