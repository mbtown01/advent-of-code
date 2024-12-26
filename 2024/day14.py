import unittest
from os import path
from collections import defaultdict
from functools import reduce
from operator import mul


class Implementation:

    def __init__(self, dataPath: str):
        self.robotList = list()
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                self.robotList.append(dict())
                for p in line.strip().split(' '):
                    self.robotList[-1][p[0]] = \
                        tuple(int(a) for a in p[2:].split(',')[::-1])

    def part1(self, extents: tuple, seconds: int):
        middle, quadCounts = tuple(a // 2 for a in extents), [0, 0, 0, 0]
        for r in self.robotList:
            finalY = (r['p'][0] + r['v'][0]*seconds) % extents[0]
            finalX = (r['p'][1] + r['v'][1]*seconds) % extents[1]
            if finalY != middle[0] and finalX != middle[1]:
                quadY = 0 if finalY < middle[0] else 1
                quadX = 0 if finalX < middle[1] else 1
                quadCounts[2*quadY + quadX] += 1

        return reduce(mul, quadCounts)

    def part2(self, extents: tuple):
        # Since the extents are both prime numbers, each element will touch
        # every point in the scene, found at t=7400
        for t in range(extents[0]*extents[1]):
            grid = {((r['p'][0] + r['v'][0]*t) % extents[0],
                     (r['p'][1] + r['v'][1]*t) % extents[1]): 1
                    for r in self.robotList}

            clusterScore = sum(grid.get((a[0], a[1]+1), 0) +
                               grid.get((a[0], a[1]-1), 0) +
                               grid.get((a[0]+1, a[1]), 0) +
                               grid.get((a[0]-1, a[1]), 0)
                               for a in grid)
            if clusterScore > 1000:
                for y in range(extents[0]):
                    line = list('#' if (y, x) in grid else ' '
                                for x in range(extents[1]))
                    print(f"[{y:03d}] {''.join(line)}")
                return t

        raise RuntimeError('Never found a big enough cluster')


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1((7, 11), 100)
        self.assertEqual(result, 12)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1((103, 101), 100)
        self.assertEqual(result, 226179492)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2((103, 101))
        self.assertEqual(result, 7502)
