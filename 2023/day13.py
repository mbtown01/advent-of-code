import unittest


class Pattern:

    def __init__(self, rows: list) -> None:
        self.width = len(rows[0])
        self.height = len(rows)
        self.rows = rows
        self.cols = list(''.join(r[a] for r in self.rows)
                         for a in range(self.width))

    def __repr__(self) -> str:
        return f"[Pattern height={self.height}, width={self.width}]"

    def perfect(self, fwdTest: list, bkwdTest: list):
        return fwdTest == bkwdTest

    def withSmudges(self, fwdTest: list, bkwdTest: list):
        fwdFlat = list(b for a in fwdTest for b in a)
        bkwdFlat = list(b for a in bkwdTest for b in a)
        return 1 == sum(1 if a != b else 0
                        for a, b in zip(fwdFlat, bkwdFlat))

    def findSymmetry(self, vList: list, comp):
        for i in range(len(vList)-1):
            testLen = min(i+1, len(vList)-i-1)
            fwdTest = vList[i-testLen+1:i+1]
            bkwdTest = vList[i+1:i+testLen+1][::-1]
            if comp(fwdTest, bkwdTest):
                return i+1
        return 0

    def score(self, compMethod):
        return self.findSymmetry(self.rows, compMethod) * 100 + \
            self.findSymmetry(self.cols, compMethod)


class Implementation:

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            allRows = list(a.strip() for a in reader.readlines())
            splits = list(i for i, a in enumerate(allRows) if len(a) == 0)
            self.patternList = list(Pattern(allRows[a+1:b])
                                    for a, b in zip(
                                        [-1]+splits, splits+[len(allRows)]))

    def part1(self):
        return sum(a.score(a.perfect) for a in self.patternList)

    def part2(self):
        return sum(a.score(a.withSmudges) for a in self.patternList)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 405)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 29165)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 400)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 32192)
