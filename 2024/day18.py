import unittest
from os import path
from collections import defaultdict
from heapq import heappush, heappop

NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.byteLocs = list((int(a[1]), int(a[0]))
                                 for a in list(line.strip().split(',')
                                               for line in reader))

    def dumpGrid(self, grid: dict):
        extents = max(grid.keys())
        for j in enumerate(range(extents[0]+1)):
            row = ''.join(grid.get((j, i)) for i in range(extents[1]+1))
            print(f"[{j:03}] {row}")

    def findPathsAStar(self, grid: dict, nx: int, ny: int):
        start, end = (0, 0), (ny-1, nx-1)
        bestMap, distMap = defaultdict(list), {start: 0}
        frontier = [(nx+ny-2, start, [start])]
        while len(frontier) > 0:
            _, loc, history = heappop(frontier)
            if loc == end:
                bestMap[len(history)].append(history)

            for vec in (SOUTH, EAST, WEST, NORTH):
                nextLoc = (loc[0]+vec[0], loc[1]+vec[1])
                nextScore = distMap.get(nextLoc, 2**60)
                if grid.get(nextLoc) == '.' and distMap[loc]+1 < nextScore:
                    distMap[nextLoc] = distMap[loc]+1
                    priority = distMap[nextLoc] + \
                        abs(end[0]-nextLoc[0]) + abs(end[1]-nextLoc[1])
                    heappush(frontier, (priority, nextLoc, history+[nextLoc]))
        return bestMap

    def part1(self, byteCount: int, nx: int, ny: int):
        grid = {(y, x): '.' for y in range(ny) for x in range(nx)}
        grid.update({loc: '#' for loc in self.byteLocs[:byteCount]})
        bestMap = self.findPathsAStar(grid, nx, ny)
        return min(bestMap)-1

    def part2(self, byteCount: int, nx: int, ny: int):
        grid = {(y, x): '.' for y in range(ny) for x in range(nx)}
        grid.update({loc: '#' for loc in self.byteLocs[:byteCount]})
        bestMap = self.findPathsAStar(grid, nx, ny)
        for loc in self.byteLocs[byteCount:]:
            grid[loc] = '#'
            if all(loc in path for path in bestMap[min(bestMap)]):
                bestMap = self.findPathsAStar(grid, nx, ny)
                if len(bestMap) == 0:
                    return loc

        raise RuntimeError('never found a blocking byte')


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1(12, 7, 7)
        self.assertEqual(result, 22)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1(1024, 71, 71)
        self.assertEqual(result, 304)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2(12, 7, 7)
        self.assertEqual(result, (1, 6))

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2(1024, 71, 71)
        self.assertEqual(result, (28, 50))
