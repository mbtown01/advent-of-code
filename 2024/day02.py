import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.reportList = list(
                list(int(a) for a in line.split(' '))
                for line in reader)

    def isValid(self, report: list):
        d1 = list(a-b for a, b in zip(report[:-1], report[1:]))
        return all(a in (1, 2, 3) for a in d1) or \
            all(-a in (1, 2, 3) for a in d1)

    def isValidMinusOne(self, report: list, factor: int):
        d1 = list(a-b for a, b in zip(report[:-1], report[1:]))
        s1 = next((a, b) for a, b in enumerate(d1)
                  if factor*b not in (1, 2, 3))
        return len(s1) >= 1 and (
            self.isValid(report[:s1[0]] + report[s1[0]+1:]) or
            self.isValid(report[:s1[0]+1] + report[s1[0]+2:]))

    def part1(self):
        return sum(self.isValid(report)
                   for report in self.reportList)

    def part2(self):
        return sum(self.isValid(report) or
                   self.isValidMinusOne(report, 1) or
                   self.isValidMinusOne(report, -1)
                   for report in self.reportList)


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 2)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 269)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 4)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 337)
        # 321 is too low
