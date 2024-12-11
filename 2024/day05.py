import unittest
from os import path
from collections import defaultdict


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            allLines = list(a.strip() for a in reader if len(a) > 0)
            self.updateList = list(a.split(',') for a in allLines if ',' in a)
            self.ruleMap = defaultdict(list)
            for a, b in list(a.split('|') for a in allLines if '|' in a):
                self.ruleMap[a].append(b)

    def isValidUpdate(self, update: list):
        return all(b in self.ruleMap[a]
                   for a, b in zip(update[:-1], update[1:]))

    def resortUpdate(self, update: list):
        while not self.isValidUpdate(update):
            for i, (a, b) in enumerate(zip(update[:-1], update[1:])):
                if a in self.ruleMap[b]:
                    update[i], update[i+1] = update[i+1], update[i]
        return update

    def part1(self):
        return sum(int(update[len(update)//2])
                   for update in self.updateList
                   if self.isValidUpdate(update))

    def part2(self):
        invalidUpdateList = list(self.resortUpdate(a)
                                 for a in self.updateList
                                 if not self.isValidUpdate(a))
        return sum(int(update[len(update)//2])
                   for update in invalidUpdateList)


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 143)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 4689)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 123)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 6336)
