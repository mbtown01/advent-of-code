import unittest


class Implementation:
    digitWordMap = {str(a+1): b for (a, b) in enumerate(
        ['one', 'two', 'three', 'four', 'five', 'six',
            'seven', 'eight', 'nine'])}

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.allLines = list(a.strip() for a in reader)

    def part1(self):
        def valueForLine(line: str):
            digits = list(int(a) for a in line if a in self.digitWordMap)
            return 10*digits[0] + digits[-1] if len(digits) > 0 else 0

        return sum(valueForLine(line) for line in self.allLines)

    def part2(self):
        def valueForLine(line: str):
            findResults = \
                [(a, line.find(a)) for a in self.digitWordMap] + \
                [(a, line.find(b)) for a, b in self.digitWordMap.items()] + \
                [(a, line.rfind(a)) for a in self.digitWordMap] + \
                [(a, line.rfind(b)) for a, b in self.digitWordMap.items()]
            findResults = list(a for a in findResults if a[1] != -1)
            findResults = sorted(findResults, key=lambda a: a[1])
            if len(findResults) > 0:
                return 10*int(findResults[0][0]) + int(findResults[-1][0])
            return 0

        return sum(valueForLine(line) for line in self.allLines)


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example1.txt')
        result = impl.part1()
        self.assertEqual(result, 142)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 56465)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example2.txt')
        result = impl.part2()
        self.assertEqual(result, 281)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 55902)
