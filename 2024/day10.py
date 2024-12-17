import unittest
from os import path


class Implementation:

    nextVecList = ((0, 1), (-1, 0), (0, -1), (1, 0))

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): int(c)
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())}
            self.extents = max(self.gridMap.keys())

    def dumpGrid(self, grid: dict):
        for j in range(self.extents[0]+1):
            print(''.join(grid.get((j, i)) for i in range(self.extents[1]+1)))

    def countTrails(self, currLoc: tuple, lastVal: int, found: dict):
        currVal = self.gridMap.get(currLoc)
        if currVal is None or currVal != lastVal+1:
            return 0
        if currVal == 9 and found is None:
            return 1
        if currVal == 9 and currLoc not in found:
            found[currLoc] = 1
            return 1

        return sum(
            self.countTrails(
                (currLoc[0]+vec[0], currLoc[1]+vec[1]), currVal, found)
            for vec in self.nextVecList)

    def part1(self):
        return sum(self.countTrails(head, -1, dict())
                   for head, val in self.gridMap.items() if val == 0)

    def part2(self):
        return sum(self.countTrails(head, -1, None)
                   for head, val in self.gridMap.items() if val == 0)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 36)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 786)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 81)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1722)
