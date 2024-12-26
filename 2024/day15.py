import unittest
from os import path


class Implementation:
    moveVectorMap = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            allLines = reader.readlines()
            gridLines = list(a for a in allLines if a[0] == '#')
            self.moveStr = ''.join(
                list(a.strip() for a in allLines if a[0] in '<>^v'))
            self.gridMap = {(j, i): c
                            for j, line in enumerate(gridLines)
                            for i, c in enumerate(line.strip())}

    def dumpGrid(self, gridMap: dict):
        extents = max(gridMap.keys())
        for j in range(extents[0]+1):
            print(''.join(gridMap.get((j, i)) for i in range(extents[1]+1)))

    def execMove(self, gridMap: dict, loc: tuple, vec: tuple, dryRun: bool):
        nextLoc = (loc[0] + vec[0], loc[1] + vec[1])
        nextGridVal = gridMap.get(nextLoc)
        if nextGridVal == '#':
            return loc
        if nextGridVal == 'O' or vec[0] == 0 and nextGridVal in '[]':
            if nextLoc == self.execMove(gridMap, nextLoc, vec, dryRun):
                return loc
            nextGridVal = gridMap.get(nextLoc)
        if vec[1] == 0 and nextGridVal in '[]':
            nextLoc2 = (nextLoc[0], nextLoc[1]+1) if nextGridVal == '[' else \
                (nextLoc[0], nextLoc[1]-1)
            if (not dryRun and
                    (nextLoc == self.execMove(gridMap, nextLoc, vec, True) or
                     nextLoc2 == self.execMove(gridMap, nextLoc2, vec, True))):
                return loc
            if (nextLoc == self.execMove(gridMap, nextLoc, vec, dryRun) or
                    nextLoc2 == self.execMove(gridMap, nextLoc2, vec, dryRun)):
                return loc
            if dryRun:
                return nextLoc
            nextGridVal = gridMap.get(nextLoc)
        if nextGridVal == '.':
            if not dryRun:
                gridMap[loc], gridMap[nextLoc] = gridMap[nextLoc], gridMap[loc]
            return nextLoc

        raise RuntimeError('panic')

    def part1(self):
        gridMap = self.gridMap.copy()
        loc = next(a[0] for a in gridMap.items() if a[1] == '@')
        for move in self.moveStr:
            loc = self.execMove(gridMap, loc, self.moveVectorMap[move], False)

        return sum(100*a[0][0]+a[0][1] for a in gridMap.items() if a[1] == 'O')

    def part2(self):
        gridMap, charMap = dict(), {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
        for loc, char in self.gridMap.items():
            gridMap[(loc[0], 2*loc[1]+0)] = charMap[char][0]
            gridMap[(loc[0], 2*loc[1]+1)] = charMap[char][1]

        loc = next(a[0] for a in gridMap.items() if a[1] == '@')
        for move in self.moveStr:
            loc = self.execMove(gridMap, loc, self.moveVectorMap[move], False)

        return sum(100*a[0][0]+a[0][1] for a in gridMap.items() if a[1] == '[')


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 10092)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 1430536)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 9021)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 1452348)
