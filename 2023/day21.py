import unittest


class Implementation:

    def __init__(self, dataPath: str):

        with open(dataPath, encoding="utf8") as reader:
            pass

    def part1(self):
        return 0

    def part2(self):
        return 0


# class TestCase(unittest.TestCase):

    # def test_part1_ex(self):
    #     impl = Implementation(f'2023/data/{__name__}_example.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 21)

    # def test_part1_real(self):
    #     impl = Implementation(f'2023/data/{__name__}_real.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 10033566)

    # def test_part2_ex(self):
    #     impl = Implementation(f'2023/data/{__name__}_example.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 1030)

    # def test_part2_real(self):
    #     impl = Implementation(f'2023/data/{__name__}_real.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 560822911938)
