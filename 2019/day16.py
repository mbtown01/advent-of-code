import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            for line in reader:
                pass

    def part1(self):
        pass

    def part2(self):
        return None


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    # def test_part1_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 9999999)

    # def test_part1_real(self):
    #     impl = Implementation(f'{self._pathPrefix}_real.txt')
    #     result = impl.part1()
    #     self.assertEqual(result, 9999999)

    # def test_part2_ex(self):
    #     impl = Implementation(f'{self._pathPrefix}_example.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 9999999)

    # def test_part2_real(self):
    #     impl = Implementation(f'{self._pathPrefix}_real.txt')
    #     result = impl.part2()
    #     self.assertEqual(result, 9999999)
