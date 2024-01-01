import unittest
import numpy as np


class Implementation:

    def __init__(self, dataPath: str):
        self.nodeMap = dict()
        with open(dataPath, encoding="utf8") as reader:
            allLines = reader.readlines()
            self.directions = allLines[0].strip()
            for line in allLines[2:]:
                parts = line.strip().split(' = ')
                node, edges = parts[0], parts[-1]
                destinations = ''.join(edges[1:-1]).split(', ')
                self.nodeMap[node] = \
                    {'L': destinations[0], 'R': destinations[1]}

    def traverse(self, startNode: str, endNodeSet: set):
        moveCount, current = 0, startNode
        while current not in endNodeSet:
            for direction in self.directions:
                current = self.nodeMap[current][direction]
                moveCount += 1

        return moveCount

    def part1(self):
        return self.traverse('AAA', set(['ZZZ']))

    def part2(self):
        startNodes = list(a for a in self.nodeMap if a.endswith('A'))
        endNodeSet = set(list(a for a in self.nodeMap if a.endswith('Z')))
        moves = list(self.traverse(a, endNodeSet) for a in startNodes)

        # If we are tracking 3 ghosts, then then number of moves it takes for
        # them ALL to SIMULTANEOUSLY arrive at an end point is the lowest
        # common multiple of the moves it takes for them to do it individually
        return np.lcm.reduce(moves)


class TestCase(unittest.TestCase):

    def test_part1_ex1(self):
        impl = Implementation(f'2023/data/{__name__}_example1.txt')
        result = impl.part1()
        self.assertEqual(result, 2)

    def test_part1_ex2(self):
        impl = Implementation(f'2023/data/{__name__}_example2.txt')
        result = impl.part1()
        self.assertEqual(result, 6)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 20513)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example3.txt')
        result = impl.part2()
        self.assertEqual(result, 6)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 15995167053923)
