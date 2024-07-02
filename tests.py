""" This file is used to write test cases for the application. """
from django.test import TestCase

class BaseTestCase(TestCase):
    """ Base test case """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base(self):
        """ Test base """
        self.assertEqual(1, 1)
        self.assertNotEqual(1, 2)
        # self.assertTrue(True)
        # self.assertFalse(False)
        self.assertIsNone(None)
        self.assertIsNotNone(1)
        self.assertIn(1, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])
        self.assertIsInstance(1, int)
        self.assertNotIsInstance(1, str)
        self.assertGreater(2, 1)
        self.assertLess(1, 2)
        self.assertGreaterEqual(2, 1)
        self.assertLessEqual(1, 2)
        self.assertAlmostEqual(1.0, 1.0000001)
        self.assertNotAlmostEqual(1.0, 1.1)
        self.assertGreater(2, 1)
        self.assertLess(1, 2)
        self.assertRegex("Hello", "^H")
        self.assertNotRegex("Hello", "^H")
        self.assertCountEqual([1, 2, 3], [3, 2, 1])
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        self.assertTupleEqual((1, 2, 3), (1, 2, 3))
        self.assertSetEqual({1, 2, 3}, {3, 2, 1})
        self.assertDictEqual({1: "one", 2: "two"}, {2: "two", 1: "one"})
        self.assertMultiLineEqual("Hello\nWorld", "Hello\nWorld")
        self.assertSequenceEqual([1, 2, 3], [1, 2, 3])
        # self.assertDictContainsSubset({1: "one"}, {1: "one", 2: "two"})
        self.assertLogs("logger", "INFO")
        self.assertWarns(UserWarning, lambda: None)
