import unittest
from os import path
from collections import defaultdict
# from itertools import combinations


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())}
            self.extents = max(self.gridMap.keys())

    def findAntiNodes(self, isPart1: bool):
        antennaMap, antiNodeMap = defaultdict(list), dict()
        for loc, a in self.gridMap.items():
            if a != '.':
                antennaMap[a].append(loc)

        for antennaList in antennaMap.values():
            for a1, a2 in list((a1, a2) for a1 in antennaList
                               for a2 in antennaList if a1 != a2):
                vec = (a2[0]-a1[0], a2[1]-a1[1])
                loc = (a1[0]-vec[0], a1[1]-vec[1]) if isPart1 else a1
                l = 1 if isPart1 else 99999
                while loc in self.gridMap and l > 0:
                    antiNodeMap[loc] = '#'
                    loc = (loc[0]-vec[0], loc[1]-vec[1])
                    l = l - 1

        return len(antiNodeMap)

    def part1(self):
        return self.findAntiNodes(True)

    def part2(self):
        return self.findAntiNodes(False)


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 14)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 396)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 34)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1200)
