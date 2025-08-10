import unittest
from os import path
from collections import defaultdict


class Implementation:

    def __init__(self, valMin: int, valMax: int):
        self.valMin = valMin
        self.valMax = valMax

    def search(self, level: int, value: int, isPart1: bool):
        if level == 6:
            if self.valMin <= value <= self.valMax:
                valueMap, valueStr = defaultdict(int), str(value)
                for a, b in zip(valueStr[:-1], valueStr[1:]):
                    if a == b:
                        valueMap[a] += 1
                if isPart1:
                    return len(valueMap) > 0
                else:
                    return 1 in valueMap.values()
            return 0

        return sum(self.search(level+1, 10*value+i, isPart1)
                   for i in range(value % 10, 10))

    def part1(self):
        return self.search(0, 0, True)

    def part2(self):
        return self.search(0, 0, False)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    # def test_part1_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 9999999)

    def test_part1_real(self):
        impl = Implementation(353096, 843212)
        result = impl.part1()
        self.assertEqual(result, 579)

    # def test_part2_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 9999999)

    def test_part2_real(self):
        impl = Implementation(353096, 843212)
        result = impl.part2()
        self.assertEqual(result, 358)
