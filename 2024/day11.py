import unittest
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.stones = reader.readline().strip().split(' ')

    def blink(self, stone: str, level: int, cache: dict):
        if level == 0:
            return 1
        cacheKey = (stone, level)
        result = cache.get(cacheKey)
        if result is not None:
            return result

        if stone == '0':
            result = self.blink('1', level-1, cache)
        elif len(stone) % 2 == 0:
            result = \
                self.blink(stone[:len(stone)//2], level-1, cache) + \
                self.blink(str(int(stone[len(stone)//2:])), level-1, cache)
        else:
            result = self.blink(str(int(stone)*2024), level-1, cache)

        cache[cacheKey] = result
        return result

    def part1(self):
        cache = dict()
        return sum(self.blink(a, 25, cache) for a in self.stones)

    def part2(self):
        cache = dict()
        return sum(self.blink(a, 75, cache) for a in self.stones)


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 55312)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 182081)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 216318908621637)
