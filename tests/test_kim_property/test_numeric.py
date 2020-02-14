from tests.test_kim_property import PyTest

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
    [0],  # [],
    [1, 0],  # [[]],
    [2, 0],  # [[], []],
    [1],  # [1],
    [3],  # [1, 2, 3],
    [2, 2],  # [[1, 2], [0, 0]],
    [5, 1],  # [[1], [2], [3], [4], [5]],
    [5, 2],  # [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]],
    [5, 3],  # [[0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    [3, 2, 3],  # [[[0, 1, 0], [0, 2, 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    [4, 4, 1],  # [[[1], [2], [3], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    [2, 2, 3],  # [[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_SIZE = [
    0,  # [],
    0,  # [[]],
    0,  # [[], []],
    1,  # [1],
    3,  # [1, 2, 3],
    4,  # [[1, 2], [0, 0]],
    5,  # [[1], [2], [3], [4], [5]],
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
    [2],    # [[], [1]],
    [2],   # [[1, 2], [0, 0, 0]],
    [5],  # [[1], [2, 1], [3], [4], [5, 2, 3]],
    [5],  # [[0, 1], [0], [0, 3], [0, 4], [0, 5]],
    [5, 3],  # [[0, 1, 0], [0, 2, [0]], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    [3, 2, 3],  # [[[0, 1, 0], [0, [2], 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    [4],  # [[[1], [2], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    [2, 2],  # [[[[1, 2, 3]], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

MULTIDIMENSION_ARRAYS_NONUNIFORM_SIZE = [
    2,  # [[], [1]],
    2,  # [[1, 2], [0, 0, 0]],
    5,   # [[1], [2, 1], [3], [4], [5, 2, 3]],
    5,  # [[0, 1], [0], [0, 3], [0, 4], [0, 5]],
    15,  # [[0, 1, 0], [0, 2, [0]], [0, 3, 0], [0, 4, 0], [0, 5, 0]],
    18,  # [[[0, 1, 0], [0, [2], 0]], [[0, 3, 0], [0, 4, 0]], [[0, 5, 0], [0, 6, 0]]],
    4,  # [[[1], [2], [4]], [[5], [6], [7], [8]], [[9], [8], [7], [6]], [[1], [1], [1], [1]]],
    4,  # [[[[1, 2, 3]], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]],
]

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
        for i, a in enumerate(MULTIDIMENSION_ARRAYS):
            s1 = MULTIDIMENSION_ARRAYS_SHAPE[i]
            s2 = self.kim_property.shape(a)
            self.assertTrue(s1 == s2)

        for i, a in enumerate(MULTIDIMENSION_ARRAYS_NONUNIFORM):
            s1 = MULTIDIMENSION_ARRAYS_NONUNIFORM_SHAPE[i]
            s2 = self.kim_property.shape(a)
            self.assertTrue(s1 == s2)

    def test_size(self):
        """Test the size function."""
        for i, a in enumerate(MULTIDIMENSION_ARRAYS):
            s1 = MULTIDIMENSION_ARRAYS_SIZE[i]
            s2 = self.kim_property.size(a)
            self.assertTrue(s1 == s2)

        for i, a in enumerate(MULTIDIMENSION_ARRAYS_NONUNIFORM):
            s1 = MULTIDIMENSION_ARRAYS_NONUNIFORM_SIZE[i]
            s2 = self.kim_property.size(a)
            self.assertTrue(s1 == s2)

    def test_is_array_uniform(self):
        """Test the size function."""
        for a in MULTIDIMENSION_ARRAYS:
            self.assertTrue(self.kim_property.is_array_uniform(a))

        for a in MULTIDIMENSION_ARRAYS_NONUNIFORM:
            self.assertFalse(self.kim_property.is_array_uniform(a))

    def test_create_full_array(self):
        """Test the create_full_array function."""
        a1 = self.kim_property.create_full_array([2, 3], 1)
        self.assertTrue(a1 == FULL_ARRAY_1)

        a2 = self.kim_property.create_full_array([3, 3, 2], True)
        self.assertTrue(a2 == FULL_ARRAY_2)

    def test_extend_full_array(self):
        """Test the extend_full_array function."""
        a1 = self.kim_property.extend_full_array(FULL_ARRAY_1, [6, 3], 0)
        self.assertTrue(a1 == FULL_ARRAY_1_EXTENDED)

        a2 = self.kim_property.extend_full_array(FULL_ARRAY_1, [3, 4], 0)
        self.assertTrue(a2 == FULL_ARRAY_1_EXTENDED_2)

        a3 = self.kim_property.extend_full_array(
            FULL_ARRAY_2, [3, 4, 2], False)
        self.assertTrue(a3 == FULL_ARRAY_2_EXTENDED)

        a4 = self.kim_property.extend_full_array(
            FULL_ARRAY_2, [4, 4, 2], False)
        self.assertTrue(a4 == FULL_ARRAY_2_EXTENDED_2)


class TestPyTestNumericComponents(TestNumericComponents, PyTest):
    pass
