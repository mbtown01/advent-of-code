import unittest
import re
import math


class Implementation:

    def __init__(self, dataPath: str):
        pattern = re.compile(' +')
        with open(dataPath, encoding="utf8") as reader:
            self.times = re.sub(pattern, ' ', reader.readline().strip())
            self.times = list(int(a) for a in self.times.split(' ')[1:])
            self.distances = re.sub(pattern, ' ', reader.readline().strip())
            self.distances = list(
                int(a) for a in self.distances.split(' ')[1:])

    def part1(self):
        result = 1
        for time, distance in zip(self.times, self.distances):
            results = list((time - a)*a for a in range(time+1))
            result *= sum(1 if a > distance else 0 for a in results)
        return result

    def part2(self):
        # solve quadratic for distance = T_button * (T_race - T_button)
        time = int("".join(list(str(a) for a in self.times)))
        distance = int("".join(list(str(a) for a in self.distances)))
        minWin = math.ceil((time - math.sqrt(time*time - 4*distance))/2)
        maxWin = math.floor((time + math.sqrt(time*time - 4*distance))/2)
        return maxWin - minWin + 1


class TestCase(unittest.TestCase):

    def test_part1_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part1()
        self.assertEqual(result, 288)

    def test_part1_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part1()
        self.assertEqual(result, 227850)

    def test_part2_ex(self):
        impl = Implementation(f'2023/data/{__name__}_example.txt')
        result = impl.part2()
        self.assertEqual(result, 71503)

    def test_part2_real(self):
        impl = Implementation(f'2023/data/{__name__}_real.txt')
        result = impl.part2()
        self.assertEqual(result, 42948149)
