import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.gridMap = {(j, i): c
                            for j, line in enumerate(reader)
                            for i, c in enumerate(line)}

    def testStencil(self, stencilList: list, expected: tuple):
        return sum(
            tuple(self.gridMap.get((loc[0]+j, loc[1]+i))
                  for loc in stencil) == expected
            for stencil in stencilList
            for (j, i) in self.gridMap.keys())

    def part1(self):
        dirList = [(0, 1), (0, -1), (1, 0), (-1, 0),
                   (1, 1), (-1, -1), (1, -1), (-1, 1)]
        stencilList = list(list((i*d[0], i*d[1]) for i in range(4))
                           for d in dirList)
        expected = ('X', 'M', 'A', 'S')
        return self.testStencil(stencilList, expected)

    def part2(self):
        stencilList = [
            [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)],
            [(0, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)],
            [(0, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)],
            [(0, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)],
        ]
        expected = ('A', 'M', 'M', 'S', 'S')
        return self.testStencil(stencilList, expected)


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 18)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 2545)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 9)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1886)
