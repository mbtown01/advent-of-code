import unittest

from day5 import Span, Implementation


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.implTest = Implementation()
        self.impl = Implementation('2023/day5.txt')

    def test_containsPoint(self):
        span = Span(100, length=100)
        self.assertTrue(span.containsPoint(100))
        self.assertTrue(span.containsPoint(150))
        self.assertTrue(span.containsPoint(199))
        self.assertFalse(span.containsPoint(99))
        self.assertFalse(span.containsPoint(99))

    def test_part1(self):
        result = self.impl.part1()
        self.assertEqual(result[1], 324724204)

    def test_part2(self):
        result = self.impl.part2()
        self.assertEqual(result[1], 104070862)

    def test_part1_test(self):
        result = self.implTest.part1()
        self.assertEqual(result[1], 35)

    def test_part2_test(self):
        result = self.implTest.part2()
        self.assertEqual(result[1], 46)
