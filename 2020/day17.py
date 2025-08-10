import unittest
from os import path
from collections import defaultdict
from itertools import product


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())
                            if c == '#'}

    def buildNextGridMap(self, gridMap: dict, dimCount: int):
        vecList = list(a for a in product([-1, 0, 1], repeat=dimCount)
                       if a != tuple([0]*dimCount))
        activeNeighborCountMap = defaultdict(int)
        inactiveNeighborCountMap = defaultdict(int)

        for loc in gridMap.keys():
            for vec in vecList:
                nextLoc = tuple(loc[i]+vec[i] for i in range(dimCount))
                if nextLoc in gridMap:
                    activeNeighborCountMap[loc] += 1
                else:
                    inactiveNeighborCountMap[nextLoc] += 1

        nextGridMap = dict()
        for loc, count in activeNeighborCountMap.items():
            if count == 2 or count == 3:
                nextGridMap[loc] = '#'
        for loc, count in inactiveNeighborCountMap.items():
            if count == 3:
                nextGridMap[loc] = '#'

        return nextGridMap

    def part1(self):
        nextGridMap = {tuple([0, *a]): b for a, b in self.gridMap.items()}
        for _ in range(6):
            nextGridMap = self.buildNextGridMap(nextGridMap, 3)
        return len(nextGridMap)

    def part2(self):
        nextGridMap = {tuple([0, 0, *a]): b for a, b in self.gridMap.items()}
        for _ in range(6):
            nextGridMap = self.buildNextGridMap(nextGridMap, 4)
        return len(nextGridMap)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 112)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 346)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 848)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1632)


if __name__ == '__main__':
    TestCase().test_part2_real()
