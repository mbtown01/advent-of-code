import unittest


class Implementation:

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            self.arrangementList = list()
            for line in reader:
                damageList, groupList = line.strip().split(' ')
                groupList = list(int(a) for a in groupList.split(','))
                self.arrangementList.append((damageList, groupList))

    def _calcPermutations(self,
                          origStr: str,
                          damageStr: str,
                          groupingsList: list,
                          finalStr: str,
                          resultCache: dict):
        # If there's nothing really left to do, or there's no way to spend
        # the rest of the groupings, stop this branch of the search
        if len(groupingsList) == 0:
            return 0 if '#' in damageStr else 1
        if sum(groupingsList) + len(groupingsList)-1 > len(damageStr):
            return 0

        # Use a dict to track situations that we've seen before and their
        # answers.  This is a huge perf savings for strings with very large
        # numbers of combinations!!
        resultCacheKey = tuple([damageStr, *groupingsList])
        previousResult = resultCache.get(resultCacheKey)
        if previousResult is not None:
            return previousResult

        # Can I apply the next grouping at this point?
        skipValue, applyValue, groupSize = 0, 0, groupingsList[0]
        damageSubStr = damageStr[:groupSize]
        if groupSize == sum(a in '?#' for a in damageSubStr):
            if len(damageSubStr) == len(damageStr):
                applyValue = self._calcPermutations(
                    origStr, damageStr[groupSize:], groupingsList[1:],
                    finalStr+'#'*groupSize, resultCache)
            elif damageStr[groupSize] in '.?':
                applyValue = self._calcPermutations(
                    origStr, damageStr[groupSize+1:], groupingsList[1:],
                    finalStr+'#'*groupSize + '.', resultCache)

        # We can only attempt to skip if the current damageSubStr doesn't
        # start with a '#' that needs to be honored...
        if not damageSubStr.startswith('#'):
            skipValue = self._calcPermutations(
                origStr, damageStr[1:], groupingsList,
                finalStr+'.', resultCache)

        result = applyValue + skipValue
        resultCache[resultCacheKey] = result
        return result

    def calcPermutations1(self, damageStr: str, groupingsList: list):
        return self._calcPermutations(
            damageStr, damageStr, groupingsList, '', dict())

    def calcPermutations2(self, damageStr: str, groupingsList: list):
        damageStr = '?'.join([damageStr]*5)
        return self._calcPermutations(
            damageStr, damageStr, groupingsList*5, '', dict())

    def part1(self):
        return sum(self.calcPermutations1(*a) for a in self.arrangementList)

    def part2(self):
        return sum(self.calcPermutations2(*a) for a in self.arrangementList)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 21)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 7843)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 525152)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 10153896718999)
