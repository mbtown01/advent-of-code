import unittest
import numpy as np
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.recordList = [dict()]
            for line in reader:
                if ': ' in line:
                    info, params = line.strip().split(': ')
                    self.recordList[-1][info[-1]] = \
                        {val[0]: int(val[2:]) for val in params.split(', ')}
                else:
                    self.recordList.append(dict())

    def getCoinCount(self, recordList: list, maxPresses: int):
        coinCount = 0
        for record in recordList:
            try:
                matrix = [[record['A']['X'], record['B']['X']],
                          [record['A']['Y'], record['B']['Y']]]
                rhs = [record['e']['X'], record['e']['Y']]
                result = np.linalg.solve(matrix, rhs)
                aVal, bVal = round(result[0]), round(result[1])
                if aVal*matrix[0][0] + bVal*matrix[0][1] == rhs[0]:
                    if aVal*matrix[1][0] + bVal*matrix[1][1] == rhs[1]:
                        if aVal <= maxPresses and bVal <= maxPresses:
                            coinCount += 3*aVal + bVal
            except np.linalg.LinAlgError:
                pass

        return coinCount

    def part1(self):
        return self.getCoinCount(self.recordList, 100)

    def part2(self):
        recordList = list(a.copy() for a in self.recordList)
        for record in recordList:
            record['e']['X'] += 10000000000000
            record['e']['Y'] += 10000000000000
        return self.getCoinCount(recordList, 10000000000000)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 480)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        # 33370 is too high
        self.assertEqual(result, 33209)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 875318608908)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 83102355665474)
