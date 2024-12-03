import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        self.columns = list(), list()

        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                for i, value in enumerate(line.strip().split('   ')):
                    self.columns[i].append(int(value))

    def part1(self):
        return sum(abs(a - b) for a, b in zip(
            sorted(self.columns[0]), sorted(self.columns[1])))

    def part2(self):
        return sum(a * sum(a == b for b in self.columns[1])
                   for a in self.columns[0])


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 11)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 1258579)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 31)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 23981443)
