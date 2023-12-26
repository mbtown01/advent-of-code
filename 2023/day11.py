import unittest


class Implementation:

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            self.starGrid = list(
                list(a for a in row.strip()) for row in reader)

    def calcExpansion(self, expansion: int):
        offset = expansion - 1
        rowSeq = list(a for a in range(len(self.starGrid)))
        for j, row in enumerate(self.starGrid):
            if '#' not in row:
                rowSeq[j+1:] = list(a+offset for a in rowSeq[j+1:])

        colSeq = list(a for a in range(len(self.starGrid[0])))
        for i in range(len(self.starGrid[0])):
            if '#' not in (row[i] for row in self.starGrid):
                colSeq[i+1:] = list(a+offset for a in colSeq[i+1:])

        starList = list((rowSeq[j], colSeq[i])
                        for j, row in enumerate(self.starGrid)
                        for i, starChar in enumerate(row)
                        if starChar == '#')

        def distance(p1: tuple, p2: tuple):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        return sum(distance(starList[a], starList[b])
                   for a in range(len(starList))
                   for b in range(a, len(starList)))

    def part1(self):
        return self.calcExpansion(2)

    def part2(self):
        return self.calcExpansion(1000*1000)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 374)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 10033566)

    def test_part2_ex1(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.calcExpansion(10)
        self.assertEqual(result, 1030)

    def test_part2_ex2(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.calcExpansion(100)
        self.assertEqual(result, 8410)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 560822911938)
