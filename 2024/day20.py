import unittest
from os import path
from collections import defaultdict


NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())}
            self.allDirs = (NORTH, SOUTH, EAST, WEST)

        start = next(a[0] for a in self.gridMap.items() if a[1] == 'S')
        end = next(a[0] for a in self.gridMap.items() if a[1] == 'E')
        loc, track = start, [start]

        while loc != end:
            for vec in self.allDirs:
                nextLoc = (loc[0]+vec[0], loc[1]+vec[1])
                if nextLoc not in track and self.gridMap.get(nextLoc) in '.E':
                    track.append(nextLoc)
                    loc = nextLoc
                    break

        self.trackMap = {l: s for s, l in enumerate(reversed(track))}

    def dumpGrid(self, grid: dict):
        extents = max(grid.keys())
        for j in range(extents[0]+1):
            row = ''.join(grid.get((j, i)) for i in range(extents[1]+1))
            print(f"[{j:03}] {row}")

    def buildCheatInfoTotalMap(self, maxSteps: int):
        totalMap = defaultdict(int)
        stepDeltas = {(y, x): steps
                      for x in range(-maxSteps, maxSteps+1)
                      for y in range(-maxSteps, maxSteps+1)
                      if (steps := abs(x) + abs(y)) <= maxSteps and steps > 1}
        for loc, time in self.trackMap.items():
            for vec, steps in stepDeltas.items():
                nextLoc = (loc[0]+vec[0], loc[1]+vec[1])
                timeSaved = time - self.trackMap.get(nextLoc, 1e12) - steps
                if timeSaved > 0:
                    totalMap[timeSaved] += 1

        return totalMap

    def part1(self):
        totalMap = self.buildCheatInfoTotalMap(2)
        return sum(b for a, b in totalMap.items() if a >= 100)

    def part2(self):
        totalMap = self.buildCheatInfoTotalMap(20)
        return sum(b for a, b in totalMap.items() if a >= 100)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        totalMap = impl.buildCheatInfoTotalMap(2)
        self.assertEqual(totalMap[2], 14)
        self.assertEqual(totalMap[4], 14)
        self.assertEqual(totalMap[6], 2)
        self.assertEqual(totalMap[8], 4)
        self.assertEqual(totalMap[10], 2)
        self.assertEqual(totalMap[12], 3)
        self.assertEqual(totalMap[20], 1)
        self.assertEqual(totalMap[36], 1)
        self.assertEqual(totalMap[38], 1)
        self.assertEqual(totalMap[40], 1)
        self.assertEqual(totalMap[64], 1)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 1387)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        totalMap = impl.buildCheatInfoTotalMap(20)
        self.assertEqual(totalMap[50], 32)
        self.assertEqual(totalMap[52], 31)
        self.assertEqual(totalMap[54], 29)
        self.assertEqual(totalMap[56], 39)
        self.assertEqual(totalMap[58], 25)
        self.assertEqual(totalMap[60], 23)
        self.assertEqual(totalMap[62], 20)
        self.assertEqual(totalMap[64], 19)
        self.assertEqual(totalMap[66], 12)
        self.assertEqual(totalMap[68], 14)
        self.assertEqual(totalMap[70], 12)
        self.assertEqual(totalMap[72], 22)
        self.assertEqual(totalMap[74], 4)
        self.assertEqual(totalMap[76], 3)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1015092)
