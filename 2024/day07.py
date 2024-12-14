import unittest
from os import path
from itertools import product


class Implementation:

    operatorMethod = {
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
        '|': lambda a, b: int(f"{a}{b}")
    }

    def __init__(self, dataPath: str):
        self.equationList = list()
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                lhs, rhs = line.strip().split(': ')
                lhs, rhs = int(lhs), list(int(a) for a in rhs.split(' '))
                self.equationList.append((lhs, rhs))

    def hasSolutionTree(self, lhs: int, rhs: list, operators: str):
        def search(val: int, index: int):
            if index == len(rhs):
                return val == lhs
            if val > lhs:
                return False

            for op in operators:
                if search(self.operatorMethod[op](val, rhs[index]), index+1):
                    return True

            return False

        return search(rhs[0], 1)

    def part1(self):
        return sum(lhs for lhs, rhs in self.equationList
                   if self.hasSolutionTree(lhs, rhs, '+*'))

    def part2(self):
        return sum(lhs for lhs, rhs in self.equationList
                   if self.hasSolutionTree(lhs, rhs, '+*|'))


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 3749)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 5702958180383)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 11387)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 92612386119138)
