import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        self.equationList = list()
        self.fMap = {
            a: 10**(b+1) for b in range(3) for a in range(10**b, 10**(b+1))}

        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                lhs, rhs = line.strip().split(': ')
                lhs, rhs = int(lhs), list(int(a) for a in rhs.split(' '))
                self.equationList.append((lhs, rhs))

    def search(self, lhs: int, rhs: list, val: int, part2: bool = False):
        rhsNext, rVal = rhs[1:], rhs[0]
        v1, v2, v3 = val*rVal, val+rVal, val * \
            self.fMap[rVal]+rVal if part2 else None
        if lhs in (v1, v2, v3):
            return True
        if len(rhsNext) == 0:
            return False

        if part2 and v3 < lhs and self.search(lhs, rhsNext, v3, part2):
            return True
        if v2 < lhs and self.search(lhs, rhsNext, v2, part2):
            return True
        return v1 < lhs and self.search(lhs, rhsNext, v1, part2)

    def part1(self):
        return sum(lhs for lhs, rhs in self.equationList
                   if self.search(lhs, rhs[1:], rhs[0]))

    def part2(self):
        return sum(lhs for lhs, rhs in self.equationList
                   if self.search(lhs, rhs[1:], rhs[0], True))


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

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


if __name__ == '__main__':
    TestCase().test_part2_real()
