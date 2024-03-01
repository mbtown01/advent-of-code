import unittest
from enum import Enum
from collections import defaultdict


class Direction(Enum):
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4


class Implementation:

    instDirMap = {'U': Direction.NORTH, 'D': Direction.SOUTH,
                  'L': Direction.WEST, 'R': Direction.EAST}
    codeDirMap = {3: Direction.NORTH, 1: Direction.SOUTH,
                  2: Direction.WEST, 0: Direction.EAST}
    dirVectorMap = {Direction.WEST: (0, -1), Direction.EAST: (0, 1),
                    Direction.NORTH: (-1, 0), Direction.SOUTH: (1, 0)}

    def __init__(self, dataPath: str):
        self.instList = list()
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                inst, steps, color = line.strip().split(' ')
                self.instList.append(dict(
                    dirTo=self.instDirMap[inst],
                    steps=int(steps),
                    color=color[2:-1],
                ))

    def _addLoc(self, loc1: tuple, loc2: tuple):
        return (loc1[0] + loc2[0], loc1[1] + loc2[1])

    def getEnclosedArea(self, instList: list):
        # Shoelace forumla https://en.wikipedia.org/wiki/Shoelace_formula
        area, perimeter, currLoc = 0, 0, (0, 0)
        for instruction in reversed(instList):
            dirVector = self.dirVectorMap[instruction['dirTo']]
            dirVector = tuple(a*instruction['steps'] for a in dirVector)
            nextLoc = self._addLoc(currLoc, dirVector)
            (x1, y1), (x2, y2) = currLoc, nextLoc
            area += x1*y2 - x2*y1
            perimeter += instruction['steps']
            currLoc = nextLoc

        return (area + perimeter) // 2 + 1

    def part1(self):
        result = self.getEnclosedArea(self.instList)
        return result

    def part2(self):
        instList = list(dict(
            dirTo=self.codeDirMap[(int(a['color'][-1]))],
            steps=int(a['color'][:5], 16),
        ) for a in self.instList)
        result = self.getEnclosedArea(instList)
        return result


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 62)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        # 70260 is TOO HIGH
        self.assertEqual(result, 67891)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 952408144115)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 94116351948493)
