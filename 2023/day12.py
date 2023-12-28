import unittest


class Implementation:

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            self.arrangementList = list()
            for line in reader:
                damageList, groupList = line.strip().split(' ')
                self.arrangementList.append(
                    (damageList, list(int(a) for a in groupList.split(','))))

    def calcPermutations(self, damageList: str, groupingsList: list):
        maxlen = len(damageList)
        baseLen = sum(groupingsList) + len(groupingsList)-1

        return 10

    def part1(self):
        return sum(self.calcPermutations(a, b)
                   for a, b in self.arrangementList)

    def part2(self):
        return 0


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 21)

    # def test_part1_real(self):
    #     impl = Implementation(f'2023/data/{__name__}_real.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 10033566)

    # def test_part2_ex1(self):
    #     impl = Implementation(f'2023/data/{__name__}_example.txt')
    #     result = impl.calcExpansion(10)
    #     self.assertEqual(result, 1030)

    # def test_part2_ex2(self):
    #     impl = Implementation(f'2023/data/{__name__}_example.txt')
    #     result = impl.calcExpansion(100)
    #     self.assertEqual(result, 8410)

    # def test_part2_real(self):
    #     impl = Implementation(f'2023/data/{__name__}_real.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 560822911938)
