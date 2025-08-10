import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.massList = list(int(a.strip()) for a in reader)

    @classmethod
    def calcFuel(cls, mass: int):
        return mass // 3 - 2

    @classmethod
    def calcFuelWithFuel(cls, mass: int):
        result = cls.calcFuel(mass)
        return 0 if result <= 0 else result + cls.calcFuelWithFuel(result)

    def part1(self):
        return sum(self.calcFuel(a) for a in self.massList)

    def part2(self):
        return sum(self.calcFuelWithFuel(a) for a in self.massList)


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex1(self):
        self.assertEqual(Implementation.calcFuel(12), 2)
        self.assertEqual(Implementation.calcFuel(14), 2)
        self.assertEqual(Implementation.calcFuel(1969), 654)
        self.assertEqual(Implementation.calcFuel(100756), 33583)

    def test_part1_ex2(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 2+2+654+33583)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 3315383)

    def test_part2_ex1(self):
        self.assertEqual(Implementation.calcFuelWithFuel(12), 2)
        self.assertEqual(Implementation.calcFuelWithFuel(14), 2)
        self.assertEqual(Implementation.calcFuelWithFuel(1969), 966)
        self.assertEqual(Implementation.calcFuelWithFuel(100756), 50346)

    def test_part2_ex2(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 2+2+966+50346)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 4970206)
