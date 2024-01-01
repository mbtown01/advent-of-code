import unittest


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.sequenceList = list(
                list(int(a) for a in line.strip().split(' '))
                for line in reader)

    def extrapolateRight(self, sequence: list):
        if any(a != 0 for a in sequence):
            diff = list(a-b for a, b in zip(sequence[1:], sequence[:-1]))
            return sequence[-1] + self.extrapolateRight(diff)
        return 0

    def extrapolateLeft(self, sequence: list):
        if any(a != 0 for a in sequence):
            diff = list(a-b for a, b in zip(sequence[1:], sequence[:-1]))
            return sequence[0] - self.extrapolateLeft(diff)
        return 0

    def part1(self):
        return sum(list(self.extrapolateRight(a) for a in self.sequenceList))

    def part2(self):
        return sum(list(self.extrapolateLeft(a) for a in self.sequenceList))


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 114)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 1834108701)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 2)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 993)
