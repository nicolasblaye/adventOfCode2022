import unittest
from main import is_pair_in_right_order


class TestPairInRightOrder(unittest.TestCase):

    def test_compare_values(self):
        self.assertTrue(is_pair_in_right_order([1], [2]))
        self.assertFalse(is_pair_in_right_order([1], [0]))
        self.assertIsNone(is_pair_in_right_order([], []))
        self.assertIsNone(is_pair_in_right_order([1], [1]))

    def test_compare_value_list(self):
        self.assertTrue(is_pair_in_right_order([1], [[2]]))
        self.assertTrue(is_pair_in_right_order([1], [[1, 2]]))
        self.assertFalse(is_pair_in_right_order([1], [[0]]))
        self.assertTrue(is_pair_in_right_order([1], [[1, 0]]))
        self.assertFalse(is_pair_in_right_order([1], [[]]))
        self.assertIsNone(is_pair_in_right_order([1], [[1]]))

    def test_compare_list_value(self):
        self.assertFalse(is_pair_in_right_order([[2]], [1]))
        self.assertFalse(is_pair_in_right_order([[1, 2]], [1]))
        self.assertTrue(is_pair_in_right_order([[]], [1]))
        self.assertIsNone(is_pair_in_right_order([[1]], [1]))

    def test_compare_list_list(self):
        self.assertFalse(is_pair_in_right_order([[1]], [[0]]))
        self.assertFalse(is_pair_in_right_order([[1]], [[]]))
        self.assertFalse(is_pair_in_right_order([[1]], [[0, 0]]))
        self.assertFalse(is_pair_in_right_order([[1]], [[0, 2]]))
        self.assertFalse(is_pair_in_right_order([[[]]], [[]]))

        self.assertTrue(is_pair_in_right_order([[]], [[[]]]))
        self.assertTrue(is_pair_in_right_order([[1]], [[1, 3]]))
        self.assertTrue(is_pair_in_right_order([[1]], [[1, 0]]))
        self.assertTrue(is_pair_in_right_order([[1]], [[2]]))
        self.assertTrue(is_pair_in_right_order([[]], [[0]]))

        self.assertIsNone(is_pair_in_right_order([[1, 2, 3]], [[1, 2, 3]]))
        self.assertIsNone(is_pair_in_right_order([[]], [[]]))


if __name__ == '__main__':
    unittest.main()
