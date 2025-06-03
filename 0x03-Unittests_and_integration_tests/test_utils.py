#!/usr/bin/env python3

import unittest
from utils import access_nested_map
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a", ), 1),
        ({"a": {"c": 2}}, ("a", "c"), 2),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected):
        """"
        Test that utils.access_nested_map returns the expected value for a given nested map and path.

        Args:
            nested_map (dict): The dictionary to search.
            path (tuple): The sequence of keys representing the path to the desired value.
            expected: The expected value to be returned by access_nested_map.

        Asserts:
            The value returned by utils.access_nested_map matches the expected value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError on invalid path"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
            self.assertEqual(str(path, cm.exception))

if __name__ == "__main__":
    unittest.main()
