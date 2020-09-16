from tests.test_kim_property import PyTest
from kim_property.numeric import shape, size, \
    is_array_uniform, create_full_array, \
    extend_full_array


MULTIDIMENSION_ARRAYS = [
    [],
    [[]],
    [[], []],
    [1],
    [1, 2, 3],
    [[1, 2], [0, 0]],
    [[1], [2], [3], [4], [5]],
    [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]],
    [[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    [[[0, 1, 0], [0, 2, 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    [[[1], [2], [3], [4]], [[5], [6], [7], [8]], [
        [9], [8], [7], [6]], [[1], [1], [1], [1]]],
    [[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_SHAPE = [
    [0],        # [],
    [1, 0],     # [[]],
    [2, 0],     # [[], []],
    [1],        # [1],
    [3],        # [1, 2, 3],
    [2, 2],     # [[1, 2], [0, 0]],
    [5, 1],     # [[1], [2], [3], [4], [5]],
    [5, 2],     # [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]],
    [5, 3],     # [[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    [3, 2, 3],  # [[[0, 1, 0], [0, 2, 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    [4, 4, 1],  # [[[1], [2], [3], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    [2, 2, 3],  # [[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_SIZE = [
    0,   # [],
    0,   # [[]],
    0,   # [[], []],
    1,   # [1],
    3,   # [1, 2, 3],
    4,   # [[1, 2], [0, 0]],
    5,   # [[1], [2], [3], [4], [5]],
    10,  # [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]],
    15,  # [[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    18,  # [[[0, 1, 0], [0, 2, 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    16,  # [[[1], [2], [3], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    12,  # [[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_NONUNIFORM = [
    [[], [1]],
    [[1, 2], [0, 0, 0]],
    [[1], [2, 1], [3], [4], [5, 2, 3]],
    [[0, 1], [0], [0, 3], [0, 4], [0, 5]],
    [[0, 1, 0], [0, 2, [0]], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    [[[0, 1, 0], [0, [2], 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    [[[1], [2], [4]], [[5], [6], [7], [8]], [
        [9], [8], [7], [6]], [[1], [1], [1], [1]]],
    [[[[1, 2, 3]], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_NONUNIFORM_SHAPE = [
    [2],        # [[], [1]],
    [2],        # [[1, 2], [0, 0, 0]],
    [5],        # [[1], [2, 1], [3], [4], [5, 2, 3]],
    [5],        # [[0, 1], [0], [0, 3], [0, 4], [0, 5]],
    [5, 3],     # [[0, 1, 0], [0, 2, [0]], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    [3, 2, 3],  # [[[0, 1, 0], [0, [2], 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    [4],        # [[[1], [2], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    [2, 2],     # [[[[1, 2, 3]], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_NONUNIFORM_SIZE = [
    2,   # [[], [1]],
    2,   # [[1, 2], [0, 0, 0]],
    5,   # [[1], [2, 1], [3], [4], [5, 2, 3]],
    5,   # [[0, 1], [0], [0, 3], [0, 4], [0, 5]],
    15,  # [[0, 1, 0], [0, 2, [0]], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    18,  # [[[0, 1, 0], [0, [2], 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    4,   # [[[1], [2], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    4,   # [[[[1, 2, 3]], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

FULL_ARRAY_0 = [1, 1, 1]


FULL_ARRAY_1 = [
    [1, 1, 1],
    [1, 1, 1]
]

FULL_ARRAY_1_EXTENDED = [
    [1, 1, 1],
    [1, 1, 1],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

FULL_ARRAY_1_EXTENDED_2 = [
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0]
]

FULL_ARRAY_2 = [
    [[True, True], [True, True], [True, True]],
    [[True, True], [True, True], [True, True]],
    [[True, True], [True, True], [True, True]]
]

FULL_ARRAY_2_EXTENDED = [
    [[True, True], [True, True], [True, True], [False, False]],
    [[True, True], [True, True], [True, True], [False, False]],
    [[True, True], [True, True], [True, True], [False, False]]
]

FULL_ARRAY_2_EXTENDED_2 = [
    [[True, True], [True, True], [True, True], [False, False]],
    [[True, True], [True, True], [True, True], [False, False]],
    [[True, True], [True, True], [True, True], [False, False]],
    [[False, False], [False, False], [False, False], [False, False]]
]


class TestNumericComponents:
    """Test numeric module components."""

    def test_shape(self):
        """Test the shape function."""
        self.assertTrue(shape(2) == [])
        self.assertTrue(shape(-2) == [])
        self.assertTrue(shape(2.) == [])
        self.assertTrue(shape(-2.) == [])
        self.assertTrue(shape(2e-10) == [])
        self.assertTrue(shape(-2e-10) == [])
        self.assertTrue(shape(True) == [])
        self.assertTrue(shape('one two three') == [])

        for i, a in enumerate(MULTIDIMENSION_ARRAYS):
            s1 = MULTIDIMENSION_ARRAYS_SHAPE[i]
            s2 = shape(a)
            self.assertTrue(s1 == s2)

        for i, a in enumerate(MULTIDIMENSION_ARRAYS_NONUNIFORM):
            s1 = MULTIDIMENSION_ARRAYS_NONUNIFORM_SHAPE[i]
            s2 = shape(a)
            self.assertTrue(s1 == s2)

    def test_size(self):
        """Test the size function."""
        self.assertTrue(size(2) == 1)
        self.assertTrue(size(-2) == 1)
        self.assertTrue(size(2.) == 1)
        self.assertTrue(size(-2.) == 1)
        self.assertTrue(size(2e-10) == 1)
        self.assertTrue(size(-2e-10) == 1)
        self.assertTrue(size(True) == 1)
        self.assertTrue(size('one two three') == 1)

        for i, a in enumerate(MULTIDIMENSION_ARRAYS):
            s1 = MULTIDIMENSION_ARRAYS_SIZE[i]
            s2 = size(a)
            self.assertTrue(s1 == s2)

        for i, a in enumerate(MULTIDIMENSION_ARRAYS_NONUNIFORM):
            s1 = MULTIDIMENSION_ARRAYS_NONUNIFORM_SIZE[i]
            s2 = size(a)
            self.assertTrue(s1 == s2)

    def test_is_array_uniform(self):
        """Test the size function."""
        for a in MULTIDIMENSION_ARRAYS:
            self.assertTrue(is_array_uniform(a))

        for a in MULTIDIMENSION_ARRAYS_NONUNIFORM:
            self.assertFalse(is_array_uniform(a))

    def test_create_full_array(self):
        """Test the create_full_array function."""
        a1 = create_full_array([2, 3], 1)
        self.assertTrue(a1 == FULL_ARRAY_1)

        a2 = create_full_array([3, 3, 2], True)
        self.assertTrue(a2 == FULL_ARRAY_2)

        # if the input is not a list or tuple
        self.assertRaises(self.KIMPropertyError, create_full_array,
                          {2, 3, 2})

    def test_create_full_array_1d(self):
        """Test the create_full_array function for one-dimensional arrays."""
        a1 = create_full_array([1], 1)
        self.assertTrue(a1 == [1])
        a2 = create_full_array([1], 1.0)
        self.assertTrue(a2 == [1.0])
        a3 = create_full_array([2], True)
        self.assertTrue(a3 == [True, True])
        a4 = create_full_array([10], "Al")
        self.assertTrue(a4 == ["Al", "Al", "Al", "Al", "Al",
                               "Al", "Al", "Al", "Al", "Al"])

    def test_create_full_array_2d(self):
        """Test the create_full_array function for two-dimensional arrays."""
        a1 = create_full_array([1, 1], 1)
        self.assertTrue(a1 == [[1]])
        a2 = create_full_array([2, 1], 1.0)
        self.assertTrue(a2 == [[1.0], [1.0]])
        a3 = create_full_array([1, 2], 1.0)
        self.assertTrue(a3 == [[1.0, 1.0]])
        a4 = create_full_array([5, 2], 1)
        self.assertTrue(a4 == [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]])

    def test_create_full_array_3d(self):
        """Test the create_full_array function for three-dimensional arrays."""
        a1 = create_full_array([1, 1, 1], 1)
        self.assertTrue(a1 == [[[1]]])
        a2 = create_full_array([2, 1, 1], 1.0)
        self.assertTrue(a2 == [[[1.0]], [[1.0]]])
        a3 = create_full_array([1, 2, 1], 1.0)
        self.assertTrue(a3 == [[[1.0], [1.0]]])
        a4 = create_full_array([2, 2, 2], 1)
        self.assertTrue(a4 == [[[1, 1], [1, 1]], [[1, 1], [1, 1]]])

    def test_create_full_array_4d(self):
        """Test the create_full_array function for four-dimensional arrays."""
        a1 = create_full_array([1, 1, 1, 1], 1)
        self.assertTrue(a1 == [[[[1]]]])
        a2 = create_full_array([2, 1, 1, 1], 1.0)
        self.assertTrue(a2 == [[[[1.0]]], [[[1.0]]]])
        a3 = create_full_array([1, 2, 1, 1], 1.0)
        self.assertTrue(a3 == [[[[1.0]], [[1.0]]]])
        a4 = create_full_array([2, 2, 2, 2], 1)
        self.assertTrue(a4 == [[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [
                        [[1, 1], [1, 1]], [[1, 1], [1, 1]]]])

    def test_create_full_array_5d(self):
        """Test the create_full_array function for five-dimensional arrays."""
        a1 = create_full_array([1, 1, 1, 1, 1], 1)
        self.assertTrue(a1 == [[[[[1]]]]])
        a2 = create_full_array([2, 1, 1, 1, 1], 1.0)
        self.assertTrue(a2 == [[[[[1.0]]]], [[[[1.0]]]]])
        a3 = create_full_array([1, 2, 1, 1, 1], 1.0)
        self.assertTrue(a3 == [[[[[1.0]]], [[[1.0]]]]])
        a4 = create_full_array([2, 2, 2, 2, 2], 1)
        self.assertTrue(a4 == [[[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]], [
                        [[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]]])

    def test_create_full_array_6d(self):
        """Test the create_full_array function for six-dimensional arrays."""
        a1 = create_full_array([1, 1, 1, 1, 1, 1], 1)
        self.assertTrue(a1 == [[[[[[1]]]]]])
        a2 = create_full_array([2, 1, 1, 1, 1, 1], 1.0)
        self.assertTrue(a2 == [[[[[[1.0]]]]], [[[[[1.0]]]]]])
        a3 = create_full_array([1, 2, 1, 1, 1, 1], 1.0)
        self.assertTrue(a3 == [[[[[[1.0]]]], [[[[1.0]]]]]])
        a4 = create_full_array([2, 2, 2, 2, 2, 2], 1)
        self.assertTrue(a4 == [[[[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]], [[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]]], [
                        [[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]], [[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]]]])

    def test_extend_full_array(self):
        """Test the extend_full_array function."""
        a0 = extend_full_array(FULL_ARRAY_0, shape(FULL_ARRAY_0), 0)
        self.assertTrue(a0 == FULL_ARRAY_0)

        a1 = extend_full_array(FULL_ARRAY_1, shape(FULL_ARRAY_1), 0)
        self.assertTrue(a1 == FULL_ARRAY_1)

        a1 = extend_full_array(FULL_ARRAY_1, [6, 3], 0)
        self.assertTrue(a1 == FULL_ARRAY_1_EXTENDED)

        a2 = extend_full_array(FULL_ARRAY_1, [3, 4], 0)
        self.assertTrue(a2 == FULL_ARRAY_1_EXTENDED_2)

        a3 = extend_full_array(
            FULL_ARRAY_2, shape(FULL_ARRAY_2), False)
        self.assertTrue(a3 == FULL_ARRAY_2)

        a3 = extend_full_array(
            FULL_ARRAY_2, [3, 4, 2], False)
        self.assertTrue(a3 == FULL_ARRAY_2_EXTENDED)

        a4 = extend_full_array(
            FULL_ARRAY_2, [4, 4, 2], False)
        self.assertTrue(a4 == FULL_ARRAY_2_EXTENDED_2)

        # if the input is not a list or tuple
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          FULL_ARRAY_1, {6, 3}, 0)

        # if the input is not uniform
        a = [[1], [2, 1], [3], [4], [5, 2, 3]]
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, {5, 3}, 0)

        # dimensions do not match
        a = create_full_array([2, 3], 0)
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [2, 3, 2], 0)

        # full array dimensions are bigger
        a = create_full_array([2, 3, 4], 0)
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [2, 3, 2], 0)

        # input number of dimensions is greater than 6
        a = create_full_array([1, 1, 1, 1, 1, 1, 1, 1], 0)
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [1, 1, 1, 1, 1, 1, 1, 2], 0)

        # the input array is not uniform along all dimensions
        a = [[1, 2], [0, 0, 0]]
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [3, 3], 0)

        a = [[], [1]]
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [2, 2], 0)

        a = create_full_array([2, 2, 2, 2], 0)
        b = extend_full_array(a, [2, 2, 2, 4], 100)
        self.assertTrue(b[0][0][0][0] == 0)
        self.assertTrue(b[0][0][0][1] == 0)
        self.assertTrue(b[0][0][0][2] == 100)
        self.assertTrue(b[0][0][0][3] == 100)

        # Fail if the old shape is bigger than the new
        a = create_full_array([2, 2, 2, 2], 0)
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [2, 2, 1, 4], 0)

        a = create_full_array([1, 1, 1, 1, 1], 0)
        b = extend_full_array(a, [2, 2, 2, 2, 2], 100)
        self.assertTrue(b[0][0][0][0][0] == 0)
        self.assertTrue(b[0][0][0][0][1] == 100)

        a = create_full_array([2, 1, 2, 1, 2], 0)
        b = extend_full_array(a, [2, 2, 2, 2, 2], 100)
        self.assertTrue(b[0][0][0][0][0] == 0)
        self.assertTrue(b[0][0][0][0][1] == 0)
        self.assertTrue(b[0][0][0][1][1] == 100)
        self.assertTrue(b[1][1][1][1][1] == 100)

        # Fail if the old shape is bigger than the new
        a = create_full_array([2, 1, 2, 1, 2], 0)
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [2, 2, 2, 2, 1], 0)

        a = create_full_array([1, 1, 1, 1, 1, 1], 0)
        b = extend_full_array(a, [2, 2, 2, 2, 2, 2], 100)
        self.assertTrue(b[0][0][0][0][0][0] == 0)
        self.assertTrue(b[0][0][0][0][0][1] == 100)
        self.assertTrue(b[0][0][0][0][1][1] == 100)

        # Fail if the old shape is bigger than the new
        a = create_full_array([1, 2, 3, 3, 2, 1], 0)
        self.assertRaises(self.KIMPropertyError, extend_full_array,
                          a, [2, 2, 2, 2, 2, 2], 0)

        b = extend_full_array(a, [2, 2, 3, 3, 2, 2], 100)
        self.assertTrue(b[0][0][0][0][0][0] == 0)
        self.assertTrue(b[1][0][0][0][0][0] == 100)
        self.assertTrue(b[1][0][0][0][0][1] == 100)


class TestPyTestNumericComponents(TestNumericComponents, PyTest):
    pass
