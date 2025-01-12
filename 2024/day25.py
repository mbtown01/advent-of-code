import unittest
from os import path

exHeight, exWidth = 7, 5


class Implementation:

    def __init__(self, dataPath: str):
        self.lockList, self.keyList = list(), list()

        with open(dataPath, encoding="utf8") as reader:
            lines = list(a.strip() for a in reader)
            exLine = '#' * exWidth
            for i in range(0, len(lines), exHeight+1):
                ex = lines[i:i+exHeight]
                destList = self.lockList if ex[0] == exLine else self.keyList
                destList.append(list(sum(l[c] == '#' for l in ex[1:-1])
                                     for c in range(exWidth)))

    def part1(self):
        return sum(0 if any(lockCode[i] + keyCode[i] > (exHeight-2)
                            for i in range(exWidth)) else 1
                   for lockCode in self.lockList
                   for keyCode in self.keyList)

    def part2(self):
        raise NotImplementedError()


class TestCase(unittest.TestCase):
    _filePrefix = path.basename(__file__).replace('.py', '')
    _pathPrefix = f"{path.dirname(__file__)}/data/{_filePrefix}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 3)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 3136)
