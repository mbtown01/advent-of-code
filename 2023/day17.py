import unittest

from enum import Enum
from queue import PriorityQueue
from collections import defaultdict
from sys import stdout
from io import TextIOBase


class Direction(Enum):
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4


class Implementation:

    dirVectorMap = {Direction.WEST: (0, -1), Direction.EAST: (0, 1),
                    Direction.NORTH: (-1, 0), Direction.SOUTH: (1, 0)}
    dirOppositeMap = {Direction.WEST: Direction.EAST,
                      Direction.EAST: Direction.WEST,
                      Direction.NORTH: Direction.SOUTH,
                      Direction.SOUTH: Direction.NORTH}

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): int(char)
                            for j, row in enumerate(reader)
                            for i, char in enumerate(row.strip())}
            self.height = max(a[0] for a in self.gridMap) + 1
            self.width = max(a[1] for a in self.gridMap) + 1
            self.end = (self.height-1, self.width-1)
            self.start = (0, 0)

    def _dump(self,
              prevLocList: list,
              prevDirList: list,
              *,
              file: TextIOBase = stdout,
              nextLocVecList: list = None,
              ):
        dirCharMap = {Direction.WEST: '<', Direction.EAST: '>',
                      Direction.NORTH: '^', Direction.SOUTH: 'v'}

        nextLocVecList = [] if nextLocVecList is None else nextLocVecList
        allNextLocsMap = {vec[-1]: True for vec in nextLocVecList}
        outputGrid = list(
            list(' '.join('#' if (j, i) in allNextLocsMap
                          else str(self.gridMap[(j, i)])
                          for i in range(self.width)))
            if b % 2 == 0 else [' '] * (self.width*2-1)
            for j in range(self.height)
            for b in range(2))
        for prevDir, (j, i) in zip(prevDirList, prevLocList):
            dj, di = self.dirVectorMap[prevDir]
            outputGrid[2*j+-dj][i*2+-di] = dirCharMap[prevDir]

        print(file=file)
        for j, outputGridRow in enumerate(outputGrid[:-1]):
            print(f"{''.join(outputGridRow)} [{j//2}]", file=file)
        print(file=file)

    def _addLoc(self, loc1: tuple, loc2: tuple):
        return (loc1[0] + loc2[0], loc1[1] + loc2[1])

    def _getRecentDirMatchCount(self, prevDirList: list, nextDir: Direction):
        for i, d in enumerate(prevDirList[::-1]):
            if d != nextDir:
                return i
        return len(prevDirList)

    def _findBestPathAStar(self, minRun: int, maxRun: int):
        frontier = PriorityQueue()
        frontier.put((0, self.start, [], []))
        cumeHeatLossMap = defaultdict(dict)

        pointsEvaluated = 0
        minRunLimited = False
        while not frontier.empty():
            cumeHeatLoss, currLoc, prevLocList, prevDirList = frontier.get()

            if currLoc == self.end:
                trueHeatLoss = sum(self.gridMap[a] for a in prevLocList)
                self._dump(prevLocList, prevDirList)
                with open('output.txt', 'w', encoding='utf8') as output:
                    self._dump(prevLocList, prevDirList, file=output)
                print(f"True path heat loss: {trueHeatLoss}")
                print(f"Points evaluated: {pointsEvaluated}")
                return trueHeatLoss

            for nextDir in Direction:
                nextLoc = self._addLoc(currLoc, self.dirVectorMap[nextDir])
                nextLocHeatLoss = self.gridMap.get(nextLoc)
                prevDirNextDirMatchCount = \
                    self._getRecentDirMatchCount(prevDirList, nextDir)

                if minRun > 0 and len(prevDirList) > 0:
                    prevDirMatchCount = self._getRecentDirMatchCount(
                        prevDirList, prevDirList[-1])
                    minRunLimited = ((prevDirMatchCount < minRun and
                                      prevDirNextDirMatchCount == 0) or
                                     (nextLoc == self.end and
                                      prevDirNextDirMatchCount < minRun))

                if (nextLocHeatLoss is None or
                        nextLoc in prevLocList or
                        minRunLimited or
                        prevDirNextDirMatchCount == maxRun or
                        prevDirList[-1:] == [self.dirOppositeMap[nextDir]] or
                        nextLoc == self.start):
                    continue

                nextCumeHeatLoss = cumeHeatLoss + nextLocHeatLoss
                secondaryKey = (nextDir, prevDirNextDirMatchCount)
                nextLocHeatLoss = \
                    cumeHeatLossMap[nextLoc].get(secondaryKey, 1e99)
                if nextCumeHeatLoss < nextLocHeatLoss:
                    cumeHeatLossMap[nextLoc][secondaryKey] = nextCumeHeatLoss
                    frontier.put((nextCumeHeatLoss, nextLoc,
                                  prevLocList + [nextLoc],
                                  prevDirList + [nextDir]))

            pointsEvaluated += 1
            if pointsEvaluated % 10000 == 0:
                print(pointsEvaluated)

        raise RuntimeError('Never found the end')

    def part1(self):
        return self._findBestPathAStar(0, 3)

    def part2(self):
        return self._findBestPathAStar(4, 10)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 102)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 767)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 94)

    def test_part2_mbt(self):
        impl = Implementation(f'2023/data/{__name__}_example_mbt.txt')
        result = impl.part2()
        self.assertEqual(result, 94)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 904)
