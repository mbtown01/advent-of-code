import unittest
from enum import Enum
from collections import defaultdict


class Direction(Enum):
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4


class Implementation:

    moveVectorMap = {Direction.WEST: (0, -1), Direction.EAST: (0, 1),
                     Direction.NORTH: (-1, 0), Direction.SOUTH: (1, 0)}
    nextStepMap = {
        '.': {a: [a] for a in Direction},
        '\\': {
            Direction.NORTH: [Direction.WEST],
            Direction.SOUTH: [Direction.EAST],
            Direction.EAST: [Direction.SOUTH],
            Direction.WEST: [Direction.NORTH],
        },
        '/': {
            Direction.NORTH: [Direction.EAST],
            Direction.SOUTH: [Direction.WEST],
            Direction.EAST: [Direction.NORTH],
            Direction.WEST: [Direction.SOUTH],
        },
        '-': {
            Direction.NORTH: [Direction.EAST, Direction.WEST],
            Direction.SOUTH: [Direction.EAST, Direction.WEST],
            Direction.EAST: [Direction.EAST],
            Direction.WEST: [Direction.WEST],
        },
        '|': {
            Direction.EAST: [Direction.NORTH, Direction.SOUTH],
            Direction.WEST: [Direction.NORTH, Direction.SOUTH],
            Direction.NORTH: [Direction.NORTH],
            Direction.SOUTH: [Direction.SOUTH],
        },
    }

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): char
                            for j, row in enumerate(reader)
                            for i, char in enumerate(row.strip())}
            self.height = max(a[0] for a in self.gridMap) + 1
            self.width = max(a[1] for a in self.gridMap) + 1

    def trackBeam(self, startLoc: tuple, startDir: Direction):
        energizedMap, nextPathQueue = defaultdict(int), [(startLoc, startDir)]
        seenMap = dict()

        while len(nextPathQueue) > 0:
            currLoc, currDir = nextPathQueue.pop(0)
            if currLoc in self.gridMap:
                energizedMap[currLoc] += 1
                seenMap[currLoc, currDir] = 1
                gridChar = self.gridMap[currLoc]
                for nextDir in self.nextStepMap[gridChar].get(currDir, []):
                    moveVector = self.moveVectorMap[nextDir]
                    nextLoc = (currLoc[0] + moveVector[0],
                               currLoc[1] + moveVector[1])
                    if (nextLoc, nextDir) not in seenMap:
                        nextPathQueue.append((nextLoc, nextDir))

        return len(energizedMap)

    def part1(self):
        return self.trackBeam((0, 0), Direction.EAST)

    def part2(self):
        return max(
            self.trackBeam(loc, dir) for dir, loc in
            list((Direction.EAST, (j, 0)) for j in range(self.height)) +
            list((Direction.WEST, (j, self.width-1)) for j in range(self.height)) +
            list((Direction.SOUTH, (0, i)) for i in range(self.width)) +
            list((Direction.NORTH, (self.height-1, i)) for i in range(self.width)))


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 46)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 6361)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 51)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 6701)
