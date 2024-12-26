import unittest
from os import path
from collections import defaultdict
from heapq import heappush, heappop, heapify

NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)


class Implementation:
    vecNextScoreMap = {
        NORTH: {NORTH: 1, EAST: 1001, WEST: 1001},
        SOUTH: {SOUTH: 1, EAST: 1001, WEST: 1001},
        EAST: {EAST: 1, SOUTH: 1001, NORTH: 1001},
        WEST: {WEST: 1, SOUTH: 1001, NORTH: 1001},
    }

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line.strip())}
            self.extents = max(self.gridMap.keys())

    def dumpGrid(self, grid: dict):
        for j in range(self.extents[0]+1):
            print(''.join(grid.get((j, i)) for i in range(self.extents[1]+1)))

    def buildBestMap(self):
        bestMap, seenMap = defaultdict(list), dict()
        start = next(a[0] for a in self.gridMap.items() if a[1] == 'S')
        heapify(frontier := [(0, start, EAST, [start])])
        while len(frontier) > 0:
            score, loc, vec, history = heappop(frontier)
            if len(bestMap) > 0 and score > min(bestMap.keys()):
                continue
            if score > seenMap.get((loc, vec), 99999999):
                continue
            seenMap[(loc, vec)] = score
            for nextVec, nextScore in (self.vecNextScoreMap[vec].items()):
                nextLoc = (loc[0]+nextVec[0], loc[1]+nextVec[1])
                nextChar = self.gridMap.get(nextLoc)
                if nextChar == '.' and nextLoc not in history:
                    heappush(frontier, [score+nextScore,
                                        nextLoc, nextVec,
                                        history+[nextLoc],])
                elif nextChar == 'E':
                    bestMap[score+nextScore].append(history+[nextLoc])

        return bestMap

    def part1(self):
        bestMap = self.buildBestMap()
        return min(bestMap.keys())

    def part2(self):
        bestMap = self.buildBestMap()
        return len(set(loc for history in bestMap[min(bestMap.keys())]
                       for loc in history))


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 7036)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 95444)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 45)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 513)
