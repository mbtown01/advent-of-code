import unittest
from enum import Enum


class Direction(Enum):
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4


class Implementation:

    tiltVectorMap = {Direction.WEST: (0, -1), Direction.EAST: (0, 1),
                     Direction.NORTH: (-1, 0), Direction.SOUTH: (1, 0)}

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.grid = list(list(a for a in line.strip()) for line in reader)
            self.height = len(self.grid)
            self.width = len(self.grid[0])

        nj, ni = self.height, self.width
        self.tiltCheckOrder = {
            Direction.NORTH: list(
                (j, i) for j in range(nj) for i in range(ni)),
            Direction.SOUTH: list(
                (j, i) for j in reversed(range(nj)) for i in range(ni)),
            Direction.WEST: list(
                (j, i) for i in range(ni) for j in range(nj)),
            Direction.EAST: list(
                (j, i) for i in reversed(range(ni)) for j in range(nj)),
        }

    def tilt(self, direction: Direction):
        jTilt, iTilt = self.tiltVectorMap[direction]
        for jStart, iStart in self.tiltCheckOrder[direction]:
            if self.grid[jStart][iStart] == 'O':
                jCurrent, iCurrent = jStart, iStart
                while True:
                    jNext, iNext = jCurrent + jTilt, iCurrent + iTilt
                    nextLocChar = (self.grid[jNext][iNext]
                                   if 0 <= jNext < self.height and
                                   0 <= iNext < self.width else None)
                    if nextLocChar is None or nextLocChar in '#O':
                        if (jCurrent, iCurrent) != (jStart, iStart):
                            self.grid[jStart][iStart] = '.'
                            self.grid[jCurrent][iCurrent] = 'O'
                        break
                    jCurrent, iCurrent = jNext, iNext

    def getTotalLoad(self):
        return sum(self.height - j
                   for j, row in enumerate(self.grid)
                   for char in row
                   if char == 'O')

    def part1(self):
        self.tilt(Direction.NORTH)
        return self.getTotalLoad()

    def part2(self):
        sequence = list()
        sequenceCheckMap = dict()
        sequenceCheckKeyLen = 25
        cycles = 1000000000
        while True:
            self.tilt(Direction.NORTH)
            self.tilt(Direction.WEST)
            self.tilt(Direction.SOUTH)
            self.tilt(Direction.EAST)
            sequence.append(self.getTotalLoad())

            if len(sequence) > sequenceCheckKeyLen:
                sequenceCheckKey = tuple(sequence[-sequenceCheckKeyLen:])
                lastSeen = sequenceCheckMap.get(sequenceCheckKey)
                if lastSeen is not None:
                    sequenceLen = len(sequence) - lastSeen
                    return sequence[lastSeen + (cycles-lastSeen-1) % sequenceLen]
                sequenceCheckMap[sequenceCheckKey] = len(sequence)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 136)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 113456)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 64)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 118747)
