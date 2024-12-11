import unittest
import re
from os import path


class Implementation:

    def __init__(self, dataPath: str):
        with open(dataPath, encoding="utf8") as reader:
            self.allText = ''.join(a.strip() for a in reader.readlines())

    def part1(self):
        result = re.findall(r'mul\((\d\d?\d?),(\d\d?\d?)\)', self.allText)
        return sum(int(a)*int(b) for a, b in result)

    def part2(self):
        result, factor = 0, 1
        for match in re.finditer(
                r'mul\((\d\d?\d?),(\d\d?\d?)\)|do\(\)|don\'t\(\)', self.allText):
            if match.group(0).startswith('mul'):
                result += factor*int(match.group(1))*int(match.group(2))
            else:
                factor = 1 if match.group(0).startswith('do()') else 0

        return result


class TestCase(unittest.TestCase):
    _pathPrefix = f"{path.dirname(__file__)}/data/{__name__}"

    def test_part1_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 161)

    def test_part1_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 162813399)

    def test_part2_ex(self):
        impl = Implementation(f'{self._pathPrefix}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 48)

    def test_part2_real(self):
        impl = Implementation(f'{self._pathPrefix}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 53783319)
