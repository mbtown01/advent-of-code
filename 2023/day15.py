import unittest
from collections import defaultdict, OrderedDict


class Implementation:

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            self.initSteps = reader.readline().strip().split(',')

    def hash(self, value: str):
        result = 0
        for char in value:
            result = (17*(result + ord(char))) % 256
        return result

    def part1(self):
        return sum(self.hash(a) for a in self.initSteps)

    def part2(self):
        boxMap = defaultdict(OrderedDict)
        for initStep in self.initSteps:
            if '=' in initStep:
                boxLabel = initStep[:-2]
                boxIndex = self.hash(boxLabel)
                boxMap[boxIndex][boxLabel] = int(initStep[-1])
            elif initStep.endswith('-'):
                boxLabel = initStep[:-1]
                boxIndex = self.hash(boxLabel)
                if boxLabel in boxMap[boxIndex]:
                    del boxMap[boxIndex][boxLabel]
            else:
                raise RuntimeError(f'Unknown operation in {initStep}')

        return sum((b+1) * (i+1) * value
                   for b, orderedMap in boxMap.items()
                   for i, value in enumerate(orderedMap.values()))


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 1320)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 501680)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 145)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 241094)
