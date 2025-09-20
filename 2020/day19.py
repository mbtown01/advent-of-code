import unittest
from os import path
from collections import defaultdict
from itertools import product


class Implementation:

    def __init__(self, dataPath: str):
        self.ruleListMap = defaultdict(list)
        with open(dataPath, encoding="utf8") as reader:
            allLines = list(a.strip() for a in reader.readlines())
            for line in (a for a in allLines if ': ' in a):
                rule, subRules = line.split(': ')
                subRules = subRules.replace('"', '')
                for subRule in subRules.split(' | '):
                    self.ruleListMap[rule].append(
                        list(r for r in subRule.split(' ')))
            self.patternList = list(
                a for a in allLines if len(a) > 0 and ': ' not in a)

    def buildPatternSet(self, rule: str, cache: dict):
        cachedSet = cache.get(rule)
        if cachedSet is not None:
            return cachedSet

        ruleList = self.ruleListMap[rule]
        if len(ruleList) == 1 and ruleList[0][0] in "ab":
            cache[rule] = ruleList[0][0]
            return cache[rule]

        localPatternSet = set()
        for ruleList in self.ruleListMap[rule]:
            patternSetList = list(
                self.buildPatternSet(r, cache) for r in ruleList)
            for v in product(*patternSetList):
                localPatternSet.add(''.join(v))

        cache[rule] = localPatternSet
        return localPatternSet

    def part1(self):
        patternSet = self.buildPatternSet('0', dict())
        return sum(a in patternSet for a in self.patternList)

    def part2(self):
        return None


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 2)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 168)

    # def test_part2_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 693891)

    # def test_part2_real(self):
    #     impl = Implementation(f'{self._pathPrefix}_real.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 169899524778212)
