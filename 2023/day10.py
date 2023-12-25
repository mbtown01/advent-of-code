import unittest
from enum import Enum


class Direction(Enum):
    WEST = 1
    EAST = 2
    NORTH = 3
    SOUTH = 4


class MazeNode:

    def __init__(self, loc: tuple, nodeChar: str):
        self.loc = loc
        self.nodeChar = nodeChar
        self.neighborMap = dict()

    def __repr__(self) -> str:
        return f"[MazeNode char='{self.nodeChar}' " \
            f"loc={self.loc}] n={len(self.neighborMap)}]"


class Implementation:

    nextLocDeltaMap = {Direction.WEST: (0, -1), Direction.EAST: (0, 1),
                       Direction.NORTH: (-1, 0), Direction.SOUTH: (1, 0)}
    dirConnectionsMap = {Direction.NORTH: "|7FS", Direction.SOUTH: "|LJS",
                         Direction.EAST: "-J7S", Direction.WEST: "-LFS"}
    nodeCharNeighborMap = {'|': (Direction.NORTH, Direction.SOUTH),
                           '-': (Direction.EAST, Direction.WEST),
                           'L': (Direction.NORTH, Direction.EAST),
                           'J': (Direction.NORTH, Direction.WEST),
                           '7': (Direction.SOUTH, Direction.WEST),
                           'F': (Direction.SOUTH, Direction.EAST),
                           'S': list(a for a in Direction)}

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            self.mazeNodeRowList = list(
                list(MazeNode((j, i), nodeChar)
                     for i, nodeChar in enumerate(row.strip()))
                for j, row in enumerate(reader))
            self.mazeNodeMap = {a.loc: a
                                for row in self.mazeNodeRowList
                                for a in row
                                if a.nodeChar != '.'}

        self.startNode = next(
            a for a in self.mazeNodeMap.values() if a.nodeChar == 'S')
        for loc, mazeNode in self.mazeNodeMap.items():
            for nextDir in self.nodeCharNeighborMap[mazeNode.nodeChar]:
                nextLocDelta = self.nextLocDeltaMap[nextDir]
                nextLoc = tuple(loc[a] + nextLocDelta[a] for a in range(2))
                nextNode = self.mazeNodeMap.get(nextLoc)
                if nextNode is not None and \
                        nextNode.nodeChar in self.dirConnectionsMap[nextDir]:
                    mazeNode.neighborMap[nextDir] = nextNode

    def findLoop(self):
        pathSet, currentNode = set([self.startNode]), self.startNode
        nextNeighborList = list(currentNode.neighborMap.values())
        while len(nextNeighborList) > 0:
            pathSet.add(nextNeighborList[0])
            currentNode = nextNeighborList[0]
            nextNeighborList = list(a for a in currentNode.neighborMap.values()
                                    if a not in pathSet)

        return pathSet

    def part1(self):
        pathSet = self.findLoop()
        return len(pathSet) // 2

    def part2(self):
        interiorNodeCount, pathSet = 0, self.findLoop()
        for node in list(a for row in self.mazeNodeRowList
                         for a in row if a not in pathSet):
            # Walk a path EAST starting at the WEST edge from the open node
            # and count the number of times a node on the path is found with
            # a NORTH or SOUTH connection.  Basically the same as the "am I
            # in a polygon" test
            northCrossings, southCrossings, (j, i) = 0, 0, node.loc
            for lNode in self.mazeNodeRowList[j][:i+1]:
                if lNode in pathSet:
                    if Direction.NORTH in lNode.neighborMap:
                        northCrossings += 1
                    if Direction.SOUTH in lNode.neighborMap:
                        southCrossings += 1
            if northCrossings % 2 == 1 and southCrossings % 2 == 1:
                interiorNodeCount += 1

        return interiorNodeCount


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example1.txt')
        result = impl.part1()
        self.assertEqual(result, 4)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 7005)

    def test_part2_ex2(self):
        impl = Implementation(f'2023/data/{__name__}_example2.txt')
        result = impl.part2()
        self.assertEqual(result, 4)

    def test_part2_ex3(self):
        impl = Implementation(f'2023/data/{__name__}_example3.txt')
        result = impl.part2()
        self.assertEqual(result, 8)

    def test_part2_ex4(self):
        impl = Implementation(f'2023/data/{__name__}_example4.txt')
        result = impl.part2()
        self.assertEqual(result, 10)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 417)
