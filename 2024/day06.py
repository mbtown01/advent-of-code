import unittest
from os import path
from collections import defaultdict


class Span():
    def __init__(self):
        self.locSet = set()


class Implementation:

    nextVecMap = {(-1, 0): (0, 1),   # NORTH turns EAST
                  (0, 1): (1, 0),    # EAST turns SOUTH
                  (1, 0): (0, -1),   # SOUTH turns WEST
                  (0, -1): (-1, 0)}  # WEST turns NORTH

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())}
            self.start = next(a for a, b in self.gridMap.items() if b == '^')
            self.extents = max(self.gridMap.keys())

    def dumpGrid(self, grid: dict):
        for j in range(self.extents[0]+1):
            print(''.join(grid.get((j, i)) for i in range(self.extents[1]+1)))

    def findPath(self, grid: dict):
        pathMap, pathList = defaultdict(dict), list()
        loc, vec = self.start, (-1, 0)
        while loc in grid:
            while grid.get((loc[0]+vec[0], loc[1]+vec[1])) == '#':
                vec = self.nextVecMap[vec]
            pathMap[loc][vec] = len(pathList)
            pathList.append((loc, vec))
            loc = (loc[0]+vec[0], loc[1]+vec[1])
            if loc in pathMap and vec in pathMap[loc]:
                return None
        return pathMap, pathList

    def part1(self):
        return len(self.findPath(self.gridMap)[0])

    def part2(self):
        obstructionMap, pathList = dict(), self.findPath(self.gridMap)[1]
        for i, (loc, vec) in enumerate(pathList):
            print(f"next {i} of {len(pathList)}")
            testLoc = (loc[0]+vec[0], loc[1]+vec[1])
            if self.gridMap.get(testLoc) == '.':
                self.gridMap[testLoc] = '#'
                result = self.findPath(self.gridMap)
                self.gridMap[testLoc] = '.'
                if result is None:
                    obstructionMap[testLoc] = 'O'

        return len(obstructionMap)


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 41)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 4559)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 6)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1604)
