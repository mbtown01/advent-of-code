import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.designList = list()
            for line in reader:
                if ',' in line:
                    self.patternList = line.strip().split(', ')
                elif len(line.strip()) > 0:
                    self.designList.append(line.strip())

    def validateDesign(self, design: str):
        if len(design) == 0:
            return True
        return any(design.startswith(p) and self.validateDesign(design[len(p):])
                   for p in self.patternList)

    def enumerateDesign(self, design: str, cache: dict):
        if len(design) == 0:
            return 1
        if design not in cache:
            cache[design] = sum(self.enumerateDesign(design[len(p):], cache)
                                for p in self.patternList
                                if design.startswith(p))
        return cache[design]

    def part1(self):
        return sum(1 if self.validateDesign(d) else 0 for d in self.designList)

    def part2(self):
        return sum(self.enumerateDesign(d, dict()) for d in self.designList)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 6)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 220)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 16)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 565600047715343)
