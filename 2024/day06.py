import unittest
from os import path


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
            # nj, ni = max(self.gridMap.keys())

            # # Build a map storing the final destination of every point
            # # on the grid given a direction.  Without obstacles, that map
            # # shows falling off the grid in every direction
            # self.newGridMap = dict()
            # for loc, toVec in \
            #         [((j, 0), (0, 1)) for j in range(nj)] + \
            #         [((j, ni-1), (0, -1)) for j in range(nj)] + \
            #         [((0, i), (1, 0)) for i in range(ni)] + \
            #         [((nj-1, i), (-1, 0)) for i in range(ni)]:
            #     fromVec = (-toVec[0], -toVec[1])

    def findPath(self, grid: dict):
        pathSet, pathList = set(), list()
        loc, vec = self.start, (-1, 0)
        while loc in grid:
            while grid.get((loc[0]+vec[0], loc[1]+vec[1])) == '#':
                vec = self.nextVecMap[vec]
            pathSet.add((loc, vec))
            pathList.append((loc, vec))
            loc = (loc[0]+vec[0], loc[1]+vec[1])
            if (loc, vec) in pathSet:
                return None
        return pathList

    def part1(self):
        return len(set(a[0] for a in self.findPath(self.gridMap)))

    def part2(self):
        obstructionMap, pathList = dict(), self.findPath(self.gridMap)
        for loc, vec in pathList:
            testLoc = (loc[0]+vec[0], loc[1]+vec[1])
            if self.gridMap.get(testLoc) == '.':
                self.gridMap[testLoc] = '#'
                result = self.findPath(self.gridMap)
                self.gridMap[testLoc] = '.'
                if result is None:
                    obstructionMap[testLoc] = 'O'
                elif testLoc in list(a[0] for a in result):
                    print('well that did not work')

        return len(obstructionMap)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

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


if __name__ == '__main__':
    TestCase().test_part2_real()
